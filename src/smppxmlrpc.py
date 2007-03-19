from twisted.web import xmlrpc, server
from twisted.internet import defer
from twisted.application import internet
from twisted.protocols import http

class SMPPControl(xmlrpc.XMLRPC):
  def __init__(self, SME, OTA):
    self.SME = SME
    self.OTA = OTA
    xmlrpc.XMLRPC.__init__(self)

  # TODO: Insert full-blown auth implementation here
  #       Useful only when external parties are going to use our sender
  #def render(self, request):
  #  headers = request.getAllHeaders()
  #  if headers.has_key("authorization"):
  #    if request.getUser() == 'botva' and request.getPassword() == 'botva':
  #      return xmlrpc.XMLRPC.render(self, request)
  #  request.setResponseCode(http.UNAUTHORIZED)
  #  return ''

  def cvtList(self, m):
    oid, data = m
    ids = []
    if isinstance(data, list):
      for i in data:
        msg, sme = i[1]
        ids.append(msg.kw['message_id'])
    else:
      msg, sme = data
      ids.append(msg.kw['message_id'])
    return { "oid" : oid, "ids" : ids }

  def xmlrpc_serverstatus(self):
    r = []
    for _, sme in self.SME.servers.values():
      r.append((sme.id, sme.transmitterConnected, sme.transmitterReady))
    return r

  def xmlrpc_ota(self, number, type):
    print "[xmlrpc] ota request"
    d = self.OTA.send(self.SME, number, type)
    d.addCallback(self.cvtList)
    return d

  def xmlrpc_uota(self, number, mn, mo, t):
    print "[xmlrpc] uota request"
    d = self.OTA.unisend(self.SME, mn, mo, t, number)
    d.addCallback(self.cvtList)
    return d

  def cvtStatus(self, data):
    r = []
    for x in data:
      id = str(x[0])
      code = x[1]
      if code is None:
        code = -1
      else:
        code = int(code)
      tm = x[2]
      if tm is None:
        tm = ""
      else:
        tm = str(tm)
      r.append({ "id" : id, "code" : code, "tm" : tm })
    return r

  def xmlrpc_status(self, oid):
    d = self.OTA.getOtaStatus(oid)
    d.addCallback(self.cvtStatus)
    return d

  def cvtCodes(self, data):
    r1, r2, r3 = [], [], []
    for a, b, c in data:
      if len(r1) and r1[-1] == a:
        if len(r2[-1]) and r2[-1][-1] == b:
          r3[-1][-1].append(c)
        else:
          r2[-1].append(b)
          r3[-1].append([c])
      else:
        r1.append(a)
        r2.append([b])
        r3.append([[c]])
    return r1, r2, r3

  def xmlrpc_codes(self):
    return self.OTA.getCodes().addCallback(self.cvtCodes)

  def xmlrpc_text(self, src, dst, txt):
    s_npi = 1
    if src[0] == "+":
      s_ton = 1
      src = src[1:]
    else:
       s_ton = 0
    d_npi = 1
    if dst[0] == "+":
      d_ton = 1
      dst = dst[1:]
    else:
      d_ton = 0
    print "[xmlrpc] text request"
    d = self.OTA.sendText(self.SME, (s_npi, s_ton, src), (d_npi, d_ton, dst), txt)
    d.addCallback(self.cvtList)
    return d

def addControlProtocol(sc, *args):
  p = SMPPControl(*args)
  internet.TCPServer(7080, server.Site(p)).setServiceParent(sc)
