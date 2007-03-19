# Copyright (c) 2004 by Stingray Software
# For license information, read file LICENSE in project top directory
#
# $Id: PDU.py 63 2004-12-30 22:02:55Z stingray $
#
# SMPP Protocol parser and encoder library
# Misc utilities

import struct

def ffNumber(x):
  """Convert freeform number to tuple"""
  if not isinstance(x, tuple):
    ton = 0
    tpi = 1
    if x[0] == "+":
      ton = 1
      x = x[1:]
    return (tpi, ton, x)
  else:
    return x

def nnNumber(x):
  if isinstance(x, tuple):
    r = ""
    if x[1] == 1:
      r = "+"
    r += str(x[2])
    return r
  else:
    return x

def unicodify(msg):
  s = ""
  for m in msg:
    s += struct.pack("!H", ord(m))
  return s
