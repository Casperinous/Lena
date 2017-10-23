from utils import Data


class Writer():


	def __init__(size=None):
		
		if size:
			self._array = bytearray(size)
		else
			self._array = bytearray()


	def writeUnsignedLong(self, data, packed=False):
		if packed:
			data = Data.toUnsignedInt(data)

		self._array.extend(data)

	def writeSignedLong(self, data, packed=False):
		if packed:
			data = Data.toSignedInt(data)

		self._array.extend(data)

	def writeUnsignedShort(self, data, packed=False):
		if packed:
			data = Data.toUnsignedShort(data)

		self._array.extend(data)

	def writeSignedShort(self, data, packed=False):
		if packed:
			data = Data.toSignedShort(packed)

		self._array.extend(data)

	def writeBytes(self, data):

		self._array.extend(data)

	def writeZeroes(self, data, num):
		for i in range(0,num):
			self._array.extend('\0')

	def finalize(self, filename):
		with open(filename, 'wb') as f:
			f.write(self._array)


