import struct, os.path
from twisted.enterprise import adbapi
from twisted.internet import defer
import hmac, sha
from smpputil import *
import codecs, re

deco = codecs.getdecoder('utf-8')

# UDH - User Data Header
# Consists of 1-byte header length + TLV fields
# We will use this header:
#   0b - length
#     05 - UserPorts TAG
#       04 - UserPorts len
#       xxxx xxxx - Destination & Source port
#     00 - Segmented TAG
#       03 - Segmented len
#       04 - ??? id
#       xx - total fragments
#       xx - current fragment
#
# Second TLV field (segmentation info) can be omitted if we have only 1 segment,
# but if exist, it MUST BE second! Order is critical for many phones, along with
# port numbers.

def MakeUDH(Total, Current, SPort = 49154, DPort = 49999):
  if Total == 1:
    return '\x06\x05\x04' + struct.pack("!HH", DPort, SPort)
  else:
    return '\x0b\x05\x04' + struct.pack("!HH", DPort, SPort) + '\x00\x03\x04' + struct.pack("!BB", Total, Current)

def MakeUDH2(Total, Current):
    return '\x05\x00\x03\x04' + struct.pack("!BB", Total, Current)

# TODO: Write doc on this one

def MakeOMAWsp(key, data):
  mac = hmac.new(key, data, sha)
  d = '\x01\x06\x2f\x1f\x2d\xb6\x91\x81\x92' + mac.hexdigest().upper() + '\x00'
  return d

# Send data automation functions

def sendBatch(sender, src, dst, data):
  dl = []
  for x in data:
    dl.append(sender.sendData(src, dst, x))
  return dl

def sendBatch2(sender, src, dst, data):
  dl = []
  for x in data:
    dl.append(sender.sendData2(src, dst, x))
  return dl


def splitBinary(data, L):
  d = []
  n, r = divmod(len(data), L)
  if r > 0: n = n + 1
  for x in range(1, n + 1):
    d.append(data[(x - 1)*L:x*L])
  return d

def sendBinary(sender, src, dst, data):
  return sendBatch(sender, src, dst, splitBinary(data, 140))

def sendWithUDH(sender, src, dst, data, SPort, DPort):
  d = splitBinary(data, 119)
  d2 = []
  l = len(d)
  for n, x in enumerate(d):
    d2.append(MakeUDH(l, n+1, SPort, DPort) + x)
  return sendBatch(sender, src, dst, d2)

def sendWithUDH2(sender, src, dst, data):
  d = splitBinary(data, 120)
  d2 = []
  l = len(d)
  for n, x in enumerate(d):
    d2.append(MakeUDH2(l, n+1) + x)
  return sendBatch2(sender, src, dst, d2)

# Main OTA class

regions = [
  (re.compile("^\+7917(1[01234568]|81|82|9[4-6]|60|62)"), "samara"),
  (re.compile("^\+7917(20|21|3[012])"), "saratov"),
  (re.compile("^\+791(0(91|51|52|54|59|60|70[5-9])|586)"), "klg"),
  (re.compile("^\+7917(34|36|40|49|75|79)"), "ufa"),
]

class OTA:
  def trn(self, n, x):
    _n = nnNumber(n)
    for reg in regions:
      m = reg[0].match(_n)
      if m:
        print "[ota] Region: %s" % reg[1]
        if os.path.isfile(os.path.join(self.ddir, reg[1], x)):
          return os.path.join(self.ddir, reg[1], x)
    return os.path.join(self.ddir, "generic", x)

  def __init__(self, src, ddir):
    self.ddir = ddir
    self.src = src
    self.dbpool = adbapi.ConnectionPool("MySQLdb", user = "smpp", passwd = "smpp", db = "smpp", host = '127.0.0.1')

  def recordSend(self, datas, dst, **kw):
    ids = []
    if isinstance(datas, list):
      for i in datas:
        msg, sme = i[1]
        ids.append((sme.id, msg.kw['message_id']))
    else:
      msg, sme = datas
      ids.append((sme.id, msg.kw['message_id']))
    def _recordSend(txn):
      txn.execute("insert into delivered (Num, mo, t) values (%(Num)s, %(mo)s, %(t)s)", { "Num" : nnNumber(dst) , "mo" : kw["mo"], "t" : kw["t"] } )
      oid = txn.lastrowid
      _n = 1
      for smeid, i in ids:
        # megahack
        print "[dlri] %s, %s, %s" % (oid, smeid, i)
        txn.execute("insert into delivered_parts (OTAID, SMSCID, MSGID) values (%s, %s, %s)", (oid, smeid, i))
      print "[ota] Message with oid %s (%s %s) sent to %s (in %d parts)" % (oid, kw["mo"], kw["t"], nnNumber(dst), len(ids))
      return (oid, datas)
    return self.dbpool.runInteraction(_recordSend)  

  def recordDlr(self, sme, id, code):
    print "[dlr] Msg: %s, Code: %s" % (id, code)
    self.dbpool.runQuery("insert into dlr (SMSCID, ID, Code) values (%(SMSCID)s, %(ID)s, %(Code)s)", { "SMSCID" : sme.id, "ID" : id, "Code" : code })

  def getOtaStatus(self, id):
    return self.dbpool.runQuery("SELECT MSGID, Code, tm FROM delivered_parts left join dlr on MSGID = ID and delivered_parts.SMSCID = dlr.SMSCID WHERE OTAID = %s", id)

  def getCodes(self):
    return self.dbpool.runQuery("SELECT Manufacturers.Name, Models.Model, otatypes.Name  FROM Manufacturers, Models, otagroups, otatypes WHERE Manufacturers.ID = Models.MID and Models.OTACode = otagroups.ID and otagroups.t = otatypes.id order by Manufacturers.Name, Models.Model, otatypes.Name")

  def unisend(self, sender, mn, mo, t, dst):
    def dosend(r):
      if len(r) > 0:
        ff, fn, id, tt = r[0]
        fff = getattr(self, ff)
        return fff(sender, dst, fn, mo = id, t = tt)
      return []
    d = self.dbpool.runQuery("select otagroups.ff, otagroups.fn, Models.ID, otatypes.id from Manufacturers, Models, otagroups, otatypes WHERE Manufacturers.ID = Models.MID and Models.OTACode = otagroups.ID and otagroups.t = otatypes.id and Manufacturers.Name = %(mn)s and Models.Model = %(mo)s and otatypes.Name = %(t)s", { "mn" : mn, "mo" : mo, "t" : t })
    d.addCallback(dosend)
    return d

  def send(self, sender, dst, kind):
    sendermap = {
      1 : self.sendNokia,
      2 : self.sendOMA,
      3 : self.sendSiemens,
      99: self.sendTest,
    }

    return sendermap[kind](sender, dst)

  def sendNokia(self, sender, dst, fn = "Nokia-csd.bin", **kw):
    t = 'application/x-wap-prov.browser-settings'
    WSP = '\x01\x06' + struct.pack('B', len(t)+5) + '\x1F' + struct.pack('B', len(t)+3) + t + '\x00\x81\xEA'
    ppload = file(self.trn(dst, fn), "rb").read()

    pload = WSP + ppload

    dl = defer.DeferredList(sendWithUDH(sender, self.src, dst, pload, SPort = 49154, DPort = 49999))
    dl.addCallback(self.recordSend, dst = dst, **kw )
    return dl


  def sendOMA(self, sender, dst, fn = "motorola-gsm.bin", **kw):
    data = file(self.trn(dst, fn), "rb").read()
    wsp = MakeOMAWsp('1234', data)
    pload = wsp + data

    dl = defer.DeferredList(sendWithUDH(sender, self.src, dst, pload, SPort = 9200, DPort = 2948))
    dl.addCallback(self.recordSend, dst = dst, **kw)
    return dl

  def _sendText(self, sender, dst, data):
    return defer.DeferredList(sendWithUDH2(sender, self.src, dst, unicodify(data)))
    
  def sendSiemens(self, sender, dst, fn = "siemens.txt", **kw):
    data = file(self.trn(dst, fn), "rb").read()
    return sender.sendText(self.src, dst, data).addCallback(self.recordSend, dst = dst, **kw)

  def sendText(self, sender, src, dst, data):
    return sender.sendText(src, dst, data).addCallback(self.recordSend, dst = dst[2])

  def sendHelpText(self, sender, dst, fn="smshelp.txt", **kw):
    #return sender.sendText(self.src, dst, deco(file(self.trn(dst, fn), "rb").read())[0]).addCallback(self.recordSend, dst = dst, **kw)
    return self._sendText(sender, dst, deco(file(self.trn(dst, fn), "rb").read())[0]).addCallback(self.recordSend, dst = dst, **kw)

