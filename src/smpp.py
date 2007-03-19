# Copyright (c) 2004 by Stingray Software
# For license information, read file LICENSE in project top directory
#
# $Id: smpp.py 77 2005-01-03 17:58:53Z stingray $
#
# SMPP Protocol for Twisted framework

import struct, PDUDefs
from twisted.internet import protocol

class SMPPProtocol(protocol.Protocol):
    """Short Message Peer to Peer Protocol"""

    def __init__(self):
        self.__buffer = ""
        self.sequence = 1
        self.PDUS = {}
        self.Closed = False
        self._debug = False

    def connectionLost(self, reason):
        self.Closed = True
        protocol.Protocol.connectionLost(self, reason)

    def dataReceived(self, data):
        """ Looks for a full PDU (protocol data unit) and passes it from
        rawMessageReceived.
        """
        self.__buffer = self.__buffer + data

        while len(self.__buffer) > 3:
            (length,) = struct.unpack('!L', self.__buffer[:4])
            if len(self.__buffer) < length:
                break
            message = self.__buffer[:length]
            self.__buffer = self.__buffer[length:]
            self.rawMessageReceived(message)

    def rawMessageReceived(self, message):
        """Called once a PDU (protocol data unit) is identified.

        Creates an SMPP Message class from the data, and calls
        messageReceived with it.
        """
        header = message[0:struct.calcsize("!LLLL")]
        (l, ID, Status, Seq) = struct.unpack("!LLLL", header)
        data = message[struct.calcsize("!LLLL"):]
        x = PDUDefs.PDUS[ID]()
        x.decode(None, Status, Seq, data)
        return self.messageReceived(x)

    def sendMessage(self, pdu, callback = None):
        """Send a SMPP Message

        Argument is an SMPP PDU (protocol data unit).
        """
        if pdu.Seq == 0:
          pdu.setSequence(self.sequence)
          if self._debug:
            print "Assigned seq %d" % self.sequence
          self.sequence += 1

        p = pdu.packed()
        self.transport.write(p)
        if (pdu.PDUID & 0x80000000L) == 0:
          self.PDUS[pdu.Seq] = (pdu, callback)

    def messageReceived(self, message):
        """Called once a SMPP Message class is created

        Will call on_smpp_* based on the message type, or
        on_smpp_unhandled
        """
        method = getattr(self, "on_smpp_%s" % message.getMessageType(), None)
        if method is not None:
            method(message)
        else:
            self.on_smpp_unhandled(message)
        if message.PDUID & 0x80000000L:
          if self.PDUS.has_key(message.Seq):
            if not self.PDUS[message.Seq][1] is None:
              self.PDUS[message.Seq][1].callback((message, self.factory.SME))
            del self.PDUS[message.Seq]

    def on_smpp_unhandled(self, message):
        """By default, just print the message."""
        print "Unhandled message:"
        print message
