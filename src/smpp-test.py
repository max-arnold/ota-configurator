# -*- coding: utf-8 -*-

from twisted.application import internet, service
from smppclient import SMPPSME
import smppota, smppxmlrpc, smpporder, smpprouter
import re

application = service.Application('ota')
sc = service.IServiceCollection(application)
router = smpprouter.SMSRouter()

#sme = SMPPSME(0, username = 'wap', password = '')
#for f in sme.getFactoryList():
#  internet.TCPClient("10.82.16.68", 5555, f).setServiceParent(sc)

#router.addServer(False, sme)

#sme = SMPPSME(10, username = 'ota', password = 'rn48fks91')
#for f in sme.getFactoryList():
#  internet.TCPClient("10.2.131.24", 5001, f).setServiceParent(sc)

#91091
#91051
#91052
#91054
#91059
#91060
#91089
#91586
#910705-910709
# -- re.compile("^\+791(0(91|51|52|54|59|60|70[5-9])|586)")
#router.addServer(False, sme)


sme = SMPPSME(11, username = 'ota', password = '')
for f in sme.getFactoryList():
  internet.TCPClient("10.84.1.14", 5001, f).setServiceParent(sc)

# -- re.compile("^\+7917(1[01234568]|81|82|9[4-6]|60|62)")

router.addServer(False, sme)

#sme = SMPPSME(12, username = 'ota', password = '')
#for f in sme.getFactoryList():
#  internet.TCPClient("10.102.12.1", 5001, f).setServiceParent(sc)

#router.addServer(False, sme)

sme = SMPPSME(13, username = 'OTA', password = '')
for f in sme.getFactoryList():
  internet.TCPClient("10.84.116.158", 5000, f).setServiceParent(sc)

router.addServer(None, sme)

MyOTA = smppota.OTA('9900', r'../wbin')
smppxmlrpc.addControlProtocol(sc, router, MyOTA)
smpporder.addControlProtocol(sc, router, MyOTA)
