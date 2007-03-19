# -*- coding: utf-8 -*-

import codecs
import re
from smpputil import *
dlr_re = re.compile("(\d+),(\d+)")
dlr2_re = re.compile("^id:(\d+) sub:\d+ dlvrd:\d+ submit date:\d+ done date:\d+ stat:.+ err:(\d+) .*", re.I)

deco = codecs.getdecoder('utf-8')

omap = {
  11 : ("Nokia OTA", "CSD"),
  12 : ("Nokia OTA", "GPRS"),
  13 : ("Nokia OTA", "MMS-GPRS"),
  21 : ("Siemens Openwave", "CSD"),
  31 : ("Motorola OMA OTA", "CSD+GPRS+MMS"),
}

class SMPPOrderProtocol(object):
  def __init__(self, SME, OTA):
    self.SME = SME
    self.OTA = OTA
    self.SME.ReceiveQueue.getMessage().addCallback(self.processNextMessage)

  def getMessageTextUni(self, msg):
    dc = msg.kw['data_coding']
    if "message_payload" in msg.kw:
      text = str(msg.kw["message_payload"])
    else:
      text = str(msg.kw["short_message"])
    if dc == 8:
      try:
        text = unicode("".join(["".join(x) for x in zip(text[1::2], text[::2])]), 'utf-16')
      except UnicodeDecodeError:
        text = "UnicodeDecodeError"
    return text

  def processNextMessage(self, pair):
    sme, message = pair
    mc = message.kw['esm_class']
    text = self.getMessageTextUni(message)
    src = (message.kw['source_addr_npi'], message.kw['source_addr_ton'], message.kw['source_addr'])
    dst = (message.kw['dest_addr_npi'], message.kw['dest_addr_ton'], message.kw['destination_addr'])

    if (mc & 60) == 0:
      print "[order] Received order request from %s" % nnNumber(src)
      try:
        id = int(text)
      except ValueError:
        id = 0
      if id in omap.keys():
        self.OTA.unisend(self.SME, "-- SMS", omap[id][0], omap[id][1], src)
      else:
        self.OTA.unisend(self.SME, "-- SMS", "SMS Help Text", "Text", src)
    else:
      print "[dlr?] %s" % text
      m = dlr_re.match(text)
      if m:
        self.OTA.recordDlr(sme, str(m.group(1)), int(m.group(2)))
      else:
        print "[dlr2] %s" % text
        m = dlr2_re.match(text)
        if m:
          self.OTA.recordDlr(sme, hex(int(m.group(1))).lower()[2:], int(m.group(2)))
        else:
          print "[!] Unmatched dlr: %s" % text
    self.SME.ReceiveQueue.getMessage().addCallback(self.processNextMessage)
    return pair

def addControlProtocol(r, *args):
  global _p
  _p = SMPPOrderProtocol(*args)
