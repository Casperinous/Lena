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


class Test:

	def __init__(self, arr):
		self.arr = arr


	def getArr(self):
		return self.arr




test = Test([0,1,2,3])

n_arr = test.getArr()
n_arr.append(4)

print test.getArr()