import sys
sys.path.append('../')

import struct
import binascii
from constants import DEX_MAGIC

buff = bytearray(100)

data = struct.pack('<s', DEX_MAGIC)

idx = 0
for c in DEX_MAGIC:
	buff[idx:idx+1] = c
	idx += 1

print binascii.hexlify(buff)