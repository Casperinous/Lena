import struct

"""
string = 'Lola'

buff = bytearray(string)
print '[*] Length of bytearray : {0}'.format(len(buff))
buff[1:2] = '?'
print buff[0:len(buff)]

buff.extend('Lola?')
print '[*] Length of bytearray after extending it : {0}'.format(len(buff))
"""


#integer = struct.pack('<i', 'Lola')
print ord('\0')