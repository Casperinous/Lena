from androguard.core.bytecodes.dvm import writeuleb128
import sys
import struct
import binascii

num_1 = 0
num_2 = 10
num_3 = 1111


oleb_num_1 = writeuleb128(num_1)
oleb_num_2 = writeuleb128(num_2)
oleb_num_3 = writeuleb128(num_3)

print len(oleb_num_3)

print binascii.hexlify(oleb_num_1)
print binascii.hexlify(oleb_num_2)
print binascii.hexlify(oleb_num_3)

print ":".join("{:02x}".format(ord(c)) for c in oleb_num_2)



for c in oleb_num_3:
	print '[{0}]'.format(struct.unpack('=c', c))


parse_num = int(binascii.hexlify(oleb_num_3), 16)
print parse_num