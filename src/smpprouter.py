# not working yet

# 

from smppclient import SMPPClientQueue
from smpputil import *
import random

class SMSRouter(object):
  def __init__(self):
    self.servers = {}
    self.ReceiveQueue = SMPPClientQueue()

  def addServer(self, dst_re, sme):
    self.servers[sme.id] = (dst_re, sme)
    sme.ReceiveQueue.getMessage().addCallback(self.processNextMessage, sme = sme)

  def findSME(self, dst):
    _dst = nnNumber(dst)
    _r = []
    _d = []
    for x in self.servers.values():
      if x[0] is None:
        _d.append(x[1])
      elif isinstance(x[0], bool):
        pass
      else:
        m = x[0].match(_dst)
        if m:
          _r.append(x[1])
    if len(_r) > 0:
      return random.choice(_r)
    else:
      return random.choice(_d)

  def send(self, src, dst, data):
    d = self.findSME(dst)
    return d.send(src, dst, data)

  def processNextMessage(self, pair, sme):
    message, callback = pair
    self.ReceiveQueue.putMessage(sme, message)
    sme.ReceiveQueue.getMessage().addCallback(self.processNextMessage, sme = sme)

  def sendText(self, src, dst, msg, flash = None):
    d = self.findSME(dst)
    return d.sendText(src, dst, msg, flash)

  def sendData(self, src, dst, msg):
    d = self.findSME(dst)
    return d.sendData(src, dst, msg)

  def sendData2(self, src, dst, msg):
    d = self.findSME(dst)
    return d.sendData2(src, dst, msg)


