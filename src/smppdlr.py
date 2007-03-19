class DLRStorage(object):
  def __init__(self):
    self.dbpool = adbapi.ConnectionPool("MySQLdb", user = "smpp", passwd = "smpp", db = "smpp4", host = '10.82.4.8')

  def recordSend(self, tid, smscid, msgid):
    self.dbpool.runQuery("insert into sent_part (TID, SMSCID, MSGID) values (%(TID)s, %(SMSCID)s, %(MSGID)s)", { "TID" : tid, "SMSCID" : smscid, "MSGID" : msgid })
    pass

  def recordDlr(self, smscid, msgid, code):
    pass

  def getStatus(self, tid):
    pass
