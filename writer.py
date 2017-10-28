from utils import Data, ItemIndexer



"""
Experimental implementation of a dict with functions
associated with the kind of class the __object prope-
rty is pointed to in the Section class. It is kind 
like reflection, but it is not.
Any other suggestion would be considered a gift.
"""


#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#99
def writeStringIdItem(self, dex, item):
	#https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1826
	dex.getWriter().writeSignedInt(item.get_off())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#60
def writeTypeIdItem(self, dex, item):
	#https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1864
	dex.getWriter().writeSignedInt(item.get_descriptor_idx())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#129
def writeProtoIdItem(self, dex, item):
	#shortyIdx = file.getStringIds().indexOf(shortForm);
	#shortyIdx = ItemIndexer.indexOfStrData(item.get_shorty_idx_value())
	#int returnIdx = file.getTypeIds().indexOf(prototype.getReturnType());
    #int paramsOff = OffsettedItem.getAbsoluteOffsetOr0(parameterTypes);

    dex.getWriter().writeSignedInt(item.get_shorty_idx())
    dex.getWriter().writeSignedInt(item.get_return_type_idx())
    dex.getWriter().writeSignedInt(item.get_parameters_off())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
def writeFieldIdItem(self, dex, item):

	dex.getWriter().writeSignedInt(item.get_class_idx())
	dex.getWriter().writeSignedInt(item.get_type_idx())
	dex.getWriter().writeSignedInt(item.get_name_idx())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
def writeMethodIdItem(self, dex, item):

	dex.getWriter().writeSignedInt(item.get_class_idx())
	dex.getWriter().writeSignedInt(item.get_type_idx())
	dex.getWriter().writeSignedInt(item.get_name_idx())


#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#187
def writeClassDefItem(self, dex, item):

	dex.getWriter().writeSignedInt(item.get_class_idx())
	dex.getWriter().writeSignedInt(item.get_access_flags())
	dex.getWriter().writeSignedInt(item.get_superclass_idx())
	dex.getWriter().writeSignedInt(item.get_interfaces_off())
	dex.getWriter().writeSignedInt(item.get_source_file_idx())
	dex.getWriter().writeSignedInt(item.get_annotations_off())
	dex.getWriter().writeSignedInt(item.get_class_data_off())
	dex.getWriter().writeSignedInt(item.get_static_values_off())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#110
def writeTypeItem(self, dex, item):

	dex.getWriter().writeSignedShort(item.get_type_idx())

#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDataItem.java#343
def writeClassDataItem(self, dex, item):
	#https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L3155
	dex.getWriter().writeBytes(item.get_raw())


def writeStringDataItem(self, dex, item):
	"""
	ByteArray bytes = value.getBytes();
	int utf16Size = value.getUtf16Size();
	.....
	out.writeUnsignedLeb128(utf16Size);
	out.write(bytes);
	out.writeByte(0);
    """
    dex.getWriter().writeBytes(writeuleb128(item.get_utf16_size()))
    dex.getWriter().writeBytes(item.get_data())
    dex.getWriter().writeZeroes(1)



def writeStringIdSection(self, dex):

	items = dex.getStringIdsSection().getRawData()
	for item in items:
		writeStringIdItem(dex, item)


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


