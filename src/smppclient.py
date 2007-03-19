import smpp, PDUDefs
import Queue, struct
from smpputil import *

from twisted.internet import protocol, reactor, defer
from twisted.application import service

class SMPPClientProtocol(smpp.SMPPProtocol):
    def connectionMade(self):
        self.sendMessage(self.getBindPDU())
        self._expiry = reactor.callLater(50, self.bindTimerExpired)

    def bindTimerExpired(self):
        print "EXPIRED bind timer, losing connection"
        self.transport.loseConnection()

    def restartEnquireLinkLoop(self):
        self._enquireLink = reactor.callLater(self.factory.SME.enquireLinkTimeout, self.sendEnquireLinkLoop)

    def sendEnquireLinkLoop(self):
        self.sendMessage(PDUDefs.EnquireLink(0))
        self.restartEnquireLinkLoop()

    def bindSuccessful(self):
        self._expiry.cancel()
        self.restartEnquireLinkLoop()

    def on_smpp_unbind_recv(self, message):
        self.transport.loseConnection()

    def on_smpp_enquire_link_recv(self, message):
        pass

    def on_smpp_unhandled(self, message):
        print "Unhandled message %s received:"% type(message)
        print message

    def sendUnbind(self):
        self.sendMessage(PDUDefs.Unbind(0))

    def connectionLost(self, reason):
        try:
            self._enquireLink.cancel()
            del self._enquireLink
        except:
            pass
        smpp.SMPPProtocol.connectionLost(self, reason)

    def sendMessage(self, message, callback = None):
        if self._debug:
            print "Sent %s message" % type(message)
            print "%s" % message
        smpp.SMPPProtocol.sendMessage(self, message, callback)

class SMPPTransmitterProtocol(SMPPClientProtocol):
  _waitCounter = 1

  def getBindPDU(self):
    return PDUDefs.BindTransmitter(
      0, 
      system_id = self.factory.SME.username, 
      password = self.factory.SME.password, 
      system_type = "", interface_version = 0x50
    )

  def on_smpp_bind_transmitter_recv(self, message):
    if message.Status == 0:
      print "[t] Bound"
      self.bindSuccessful()
      self.factory.SME.transmitterConnected = True
      self.factory.SME.transmitterReady = False
      self._shotAfter()
      print "[t] gm: %s" % self._waitMessage

  def on_smpp_submit_sm_recv(self, message):
    if message.Status == 0x14:
      print "[rcv] Congestion!"
      sq = message.Seq
      if self.PDUS.has_key(sq):
        msg, cb = self.PDUS[sq]
        del self.PDUS[sq]
        self._waitCounter = 5
        if self._waitMessage is not None:
          self._waitMessage.cancel()
          self._shotAfter()
        msg.Seq = 0
        self.factory.SME.SendQueue.putMessage(msg, cb)
        
    if self._debug:
      print message

  def __shotAfter(self):
    self._waitMessage = None
    self.factory.SME.transmitterReady = True
    self._getMessage = self.factory.SME.SendQueue.getMessage().addCallback(self.processNextMessage)

  def _shotAfter(self):
    self._waitMessage = reactor.callLater(self._waitCounter, self.__shotAfter)
    if self._waitCounter > 0.2:
      self._waitCounter -= 0.1

  def processNextMessage(self, pair):
    self.factory.SME.transmitterReady = False
    message, callback = pair
    print "[t] Processing next message"
    if not self.Closed:
      try:
        print "[t] Popped out message for %s" % message.kw["destination_addr"]
        self.sendMessage(message, callback)
      except e:
        print "[t] Error! Malformed message:", repr(message), "--", repr(callback)
        print e
      print "[t] Requeuing"
      self._shotAfter()
    else:
      print "[t] Putting back message!"
      self.factory.SME.SendQueue.putMessage(message, callback)

  def connectionLost(self, reason):
    self.factory.SME.transmitterReady = False
    self.factory.SME.transmitterConnected = False
    try:
      self.factory.SME.SendQueue.cb.remove(self._getMessage)
    except:
      pass
    for msg in self.PDUS.values():
      if msg[0].PDUID in [ 4, 0x103, 0x21 ]:
        print "[cl] Putting back data message ", msg
        self.factory.SME.SendQueue.putMessage(msg[0], msg[1])
    return SMPPClientProtocol.connectionLost(self, reason)

class SMPPReceiverProtocol(SMPPClientProtocol):
  def getBindPDU(self):
    return PDUDefs.BindReceiver(
      0, 
      system_id = self.factory.SME.username, 
      password = self.factory.SME.password, 
      system_type = "", interface_version = 0x50
    )

  def on_smpp_bind_receiver_recv(self, message):
    if message.Status == 0:
      print "[r] Bound"
      self.bindSuccessful()

  def on_smpp_deliver_sm(self, message):
    self.factory.SME.ReceiveQueue.putMessage(message)
    self.sendMessage(PDUDefs.DeliverSMRecv(message.Seq))

class SMPPClientQueue(object):
    def __init__(self):
        self._Q = []
        self.cb = []
    def putMessage(self, message, callback = None):
        if len(self.cb) == 0:
            self._Q.append((message, callback))
        else:
            d = self.cb[0]
            del self.cb[0]
            d.callback((message, callback))
    def getMessage(self):
        try:
            m = self._Q.pop(0)
            return defer.succeed(m)
        except IndexError:
            d = defer.Deferred()
            self.cb.append(d)
            return d

class SMPPClientFactory(protocol.ReconnectingClientFactory):
    def __init__(self, SME, proto):
        self.SME = SME
        self.pInstance = None
        self.protocol = proto

    def startedConnecting(self, connector):
        print '(%s) Started to connect.' % self.SME.id, connector
                                                                                                                                                            
    def buildProtocol(self, addr):
        print '(%s) Connected.' % self.SME.id, addr
        self.resetDelay()
        if self.pInstance:
           self.pInstance.loseConnection()
        self.pInstance = protocol.ReconnectingClientFactory.buildProtocol(self, addr)
        return self.pInstance
                                                                                                                                                            
    def clientConnectionLost(self, connector, reason):
        print '(%s) Lost connection.' % self.SME.id, connector, reason
        self.pInstance = None
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
                                                                                                                                                            
    def clientConnectionFailed(self, connector, reason):
        print '(%s) Connection failed. ' % self.SME.id, connector, reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self,
                connector, reason)

class SMPPSME(service.Service):
  def __init__(self, id, username, password):
    self.SendQueue, self.ReceiveQueue = SMPPClientQueue(), SMPPClientQueue()
    self.username = username
    self.password = password
    self.id = id
    self.enquireLinkTimeout = 120
    self.transmitterReady, self.receiverReady = False, False
    self.transmitterConnected = False

  def getFactoryList(self):
    return [ SMPPClientFactory(self, SMPPTransmitterProtocol), SMPPClientFactory(self, SMPPReceiverProtocol) ]

  def getFactoryList2(self):
    return [ SMPPClientFactory(self, SMPPTransceiverProtocol) ]

  def _send(self, src, dst, kw):
    if not isinstance(src, tuple):
      src = ffNumber(src)
    if not isinstance(dst, tuple):
      dst = ffNumber(dst)
    kw['source_addr_npi'], kw['source_addr_ton'], kw['source_addr'] = src
    kw['dest_addr_npi'], kw['dest_addr_ton'], kw['destination_addr'] = dst
    kw['registered_delivery'] = 1

    d = defer.Deferred()
    self.SendQueue.putMessage(PDUDefs.SubmitSM(0, **kw), d)
    return d

  def sendText(self, src, dst, msg, flash = None):
    kw = {}
    dcs = 8
    s = unicodify(msg)
    if flash:
      dcs |= 16
    kw['data_coding'] = dcs
    if len(s) <= 140:
      kw['sm_length'] = len(s)
      kw['short_message'] = s
    else:
      kw['sm_length'] = 0
      kw['message_payload'] = s
    return self._send(src, dst, kw)

  def sendData(self, src, dst, msg):
    kw = {}
    kw['esm_class'] = 0x43
    kw['data_coding'] = 0xf5 
    if len(msg) <= 140:
      kw['sm_length'] = len(msg)
      kw['short_message'] = msg
    else:
      raise ValueError()
    return self._send(src, dst, kw)

  def sendData2(self, src, dst, msg):
    kw = {}
    kw['esm_class'] = 0x43
    kw['data_coding'] = 8 # 0xf5
    if len(msg) <= 140:
      kw['sm_length'] = len(msg)
      kw['short_message'] = msg
    else:
      raise ValueError()
    return self._send(src, dst, kw)

