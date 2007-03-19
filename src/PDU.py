# Copyright (c) 2004 by Stingray Software
# For license information, read file LICENSE in project top directory
#
# $Id: PDU.py 77 2005-01-03 17:58:53Z stingray $
#
# SMPP Protocol parser and encoder library
# PDU Field definitions

import StringIO, struct, types

class PDUField(object):
    def __init__(self, val = None, parent = None):
        if val:
            self.value = val
        self.parent = parent
    def _encode(self, x):
        raise
    _encode = classmethod(_encode)
    def encode(self):
        if not hasattr(self, 'value') or self.value == None:
            return self._encode(self._NULL)
        else:
            return self._encode(self.value)
    def decode(self, stream):
        self.value = self._decode(self, stream)
    def __str__(self):
        return str(self.value)

class TLV(PDUField):
    def encode(self):
        if hasattr(self, 'value') and self.value != None:
            x = self._encode(self.value)
            return struct.pack("!HH", self.Tag, len(x)) + x
        else:
            return ""

    def decode(self, length, data):
        self.value = self._decode(length, data)

class TLVInteger(TLV):
    fmt = { 1 : "!B", 2 : "!H", 4 : "!L" }
    def _encode(self, value):
        return struct.pack(self.fmt[self.length], value)
    def _decode(self, length, data):
        return struct.unpack(self.fmt[length], data)[0]

class TLVInteger2(TLVInteger):
    length = 2

class TLVOctetString(TLV):
    def _encode(self, x):
        return x
    _encode = classmethod(_encode)
    def _decode(self, length, data):
        return data

class COctetString(PDUField):
    _NULL = ""
    def decode(self, stream):
        self.value = ""
        while 1:
            c = stream.read(1)
            if c == '\0' or c == '':
                break
            self.value += c
    def _encode(self, x):
        return x + '\0'
    _encode = classmethod(_encode)

class OctetString(PDUField):
    _NULL = ""
    def _encode(self, x):
        return x
    _encode = classmethod(_encode)
    def decode(self, stream):
        r = ""
        while 1:
            c = stream.read(1)
            if c == '\0':
                break
            r += c
        self.value = r

class Integer4(PDUField):
    fmt = { 1 : "!B", 2 : "!H", 4 : "!L" }
    length = 4
    _NULL = 0
    def _encode(self, x):
        return struct.pack(self.fmt[self.length], x)
    _encode = classmethod(_encode)
    def decode(self, stream):
        self.value = struct.unpack(self.fmt[self.length], stream.read(self.length))[0]

class Integer1(Integer4):
    length = 1

class Integer2(Integer4):
    length = 2

class MultiRecipients(PDUField):
    def _encode(self, x):
        r = struct.pack("!B", len(x))
        for u in x:
            if len(u) == 3:
                r += Integer1(1).encode() + Integer1(u[0]).encode() + Integer1(u[1]).encode() + COctetString(u[2]).encode()
        return r

class PDU(object):
    def __init__(self, num = None, **kwargs):
        if isinstance(num, types.IntType) or isinstance(num, types.LongType):
            self.ID = self.PDUID
            self.Status = 0
            self.Seq = num
            self._init(**kwargs)
    def _init(self, **kwargs):
        self.kw = kwargs
    def _encode(self):
        r = ""
        for name, cls in self.defs:
            if self.kw.has_key(name):
                r = r + cls(self.kw[name]).encode()
            else:
                r = r + cls().encode()
        if hasattr(self, 'tlvs'):
            for name, cls in self.tlvs:
                if self.kw.has_key(name):
                    r = r + cls(self.kw[name]).encode()
        return r

    def encode(self):
        body = self._encode()
        return struct.pack("!LLLL", len(body) + 16, self.ID, self.Status, self.Seq) + body
    def __repr__(self):
        r = "ID: %d, Seq: %d, Status: %d\n" % (self.PDUID, self.Seq, self.Status)
        for x in self.kw.items():
            r += "%s: %s\n" % x
        return r
    def _decode(self, stream):
        self.kw = {}
        for name, cls in self.defs:
            x = cls(parent = self)
            x.decode(stream)
            self.kw[name] = x.value
        while 1:
            lx = stream.read(4)
            if len(lx) < 4:
                break
            (t, l) = struct.unpack("!HH", lx)
            v = stream.read(l)
            for name, cls in self.tlvs:
                if cls.Tag == t:
                    x = cls()
                    x.decode(l, v)
                    self.kw[name] = x
                    break

    def decode(self, orig, status, seq, data):
        self.Status = status
        self.Seq = seq
        self._decode(StringIO.StringIO(data))

    # Twisted client compatibility wrapper
    packed = encode
    def setSequence(self, x):
        self.Seq = x
    def getMessageType(self):
        return self.message_type
