from utils import Data


"""
Experimental implementation of a dict with functions
associated with the kind of class the __object prope-
rty is pointed to in the Section class. It is kind 
like reflection, but it is not.
Any other suggestion would be considered a gift.
"""

def writeStringIdItem(self,writer,item):


def writeStringDataItem(self, writer, item):
	"""
	ByteArray bytes = value.getBytes();
	int utf16Size = value.getUtf16Size();
	.....
	out.writeUnsignedLeb128(utf16Size);
	out.write(bytes);
	out.writeByte(0);
    """
    writer.writeBytes(writeuleb128(item.get_utf16_size()))
    writer.writeBytes(item.get_data())
    writer.writeZeroes(1)


dispatcher = {
	'StringDataItem': writeStringDataItem
}





class Writer():


	def __init__(size=None):
		
		if size:
			self._array = bytearray(size)
		else
			self._array = bytearray()


	def writeUnsignedInt(self, data, packed=False):
		if packed:
			data = Data.toUnsignedInt(data)

		self._array.extend(data)

	def writeSignedInt(self, data, packed=False):
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

	def writeZeroes(self, num):
		for i in range(0,num):
			self._array.extend('\0')

	def finalize(self, filename):
		with open(filename, 'wb') as f:
			f.write(self._array)


