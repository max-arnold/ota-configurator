import sys, PDUDefs, struct

def deco(message):
   header = message[0:struct.calcsize("!LLLL")]
   (l, ID, Status, Seq) = struct.unpack("!LLLL", header)
   data = message[struct.calcsize("!LLLL"):]
   x = PDUDefs.PDUS[ID]()
   x.decode(None, Status, Seq, data)
   return x


b = file(sys.argv[1], 'rb').read()
x = deco(b)

print x