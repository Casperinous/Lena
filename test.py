import struct
import binascii
"""
string = 'Lola'

buff = bytearray(string)
print '[*] Length of bytearray : {0}'.format(len(buff))
buff[1:2] = '?'
print buff[0:len(buff)]

buff.extend('Lola?')
print '[*] Length of bytearray after extending it : {0}'.format(len(buff))
"""

# integer = struct.pack('<i', 'Lola')
print ord('\0')


class Test:

    def __init__(self, arr):
        self.arr = arr

    def getArr(self):
        return self.arr
    @classmethod
    def rand_arr(self):
        return [1, 2, 3, 4]

    @staticmethod
    def lel(num):

        arr = Test.rand_arr()
        arr.append(num)
        print arr


class Yolo:

    def __init__(self):
    	pass

    def test(self, arr_):

        self.arr = []

        for i in arr_:
            self.arr.append(i + 3)


'''
test = Test([0, 1, 2, 3])

n_arr = test.getArr()
n_arr.append(4)

print test.getArr()
'''

string = 'Test String'
buff = bytearray(string)
num = 0x911
packed_num = struct.pack('<i', num)

'''
buff[2] = packed_num[0]
buff[3] = packed_num[1]
'''
buff[0:4] = packed_num

print '{0} :> {1}'.format(len(string), len(buff))
print binascii.hexlify(packed_num)
print binascii.hexlify(string)
print binascii.hexlify(buff)


Test.lel(6)
print Test.rand_arr()