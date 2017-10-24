from androguard.core.bytecodes.dvm import StringIdItem, TypeIdItem, ProtoIdItem, FieldIdItem, MethodIdItem, ClassDefItem
from writer import dispatcher
class Section():

	def __init__(self,name,alignment,data,andro_object, is_needed_in_header = False):
		
		self.__name = name
		self.__alignment = alignment
		#this is the raw data for sections which we dont change
		if data:
			self.__data = data
		else 
			self.__data = None
		"""
		Object could be a list of Androguard's class (list of proto_ids) 
		or one class like the HeaderItem
		"""
		self.__object = andro_object
		#should be set later on during the write process
		self.__file_off = 0
		#Should be computed based on the available data
		self.__write_size = 0
		#Check if modified.
		self.__is_modified = False
		#Check if contributes to header's data
		self.__is_needed_in_hd = is_needed_in_header
		#Experimental Implementation of a callback function to be used when we are writing content in disk.
		self.__callback = None


	def _calculateWriteSize(self):

		elem = None
		if isinstance(self.__object, list):
			elem = self.__object[0]
		else
			elem = self.__object

		"""
		According to source code we have that sections:
		- header
		- stringids
		- typeids
		- protoids
		- fieldids
		- methodids
		- classdefs
		are extending UniformItemSection which has the following
		implementation to calculate WriteSize:
		(It is a constant independed number instead on relying on
		 the class value like StringDataItem)

		public final int writeSize() {
	        Collection<? extends Item> items = items();
	        int sz = items.size();
	        if (sz == 0) {
	            return 0;
	        }
	        // Since each item has to be the same size, we can pick any.
	        return sz * items.iterator().next().writeSize();
    	}
    	We can easily point out now that, in order to calculate the
    	writesize of our section, we must first check what kind of
    	class we are holding on and then, calculate the data size with
    	the help of Androguard's functions.
    	It is possible, due to being CPU-consuming, to perform some
    	other calculations here too which are based on the kind of instance
    	that self.__object is pointed to.
    	"""

    	#TODO - Combine in an OR clause the items that have the same writesize also use else if?
		if isinstance(elem, StringIdItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#29
			self.__write_size = 4

		if isinstance(elem, TypeIdItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#29
			self.__write_size = 4

		if isinstance(elem, ProtoIdItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#32
			self.__write_size = 12

		if isinstance(elem, FieldIdItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
			self.__write_size = 8

		if isinstance(elem, MethodIdItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
			self.__write_size = 8

		if isinstance(elem, ClassDefItem)
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#46
			self.__write_size = 32

		if isinstance(elem, StringDataItem):
			#With a little luck, it might work ...
			self.__callback = dispatcher['StringDataItem']





	def setFileOff(self,file_off):

		'''
		Straight from the Android's source code, mapping one to one
		the java code to the python one.
		-----------------------------------------------------------


		if (fileOffset < 0) {
            throw new IllegalArgumentException("fileOffset < 0");
        }
        if (this.fileOffset >= 0) {
            throw new RuntimeException("fileOffset already set");
        }
        int mask = alignment - 1;
        fileOffset = (fileOffset + mask) & ~mask;
        this.fileOffset = fileOffset;
        '''

		mask = self.__alignment - 1
		file_off = ( file_off + mask ) & ~mask
		self.__file_off = file_off

	def getFileOff(self):

		return self.__file_off

	def getAbsFileOff(relative):

		return self.__file_off + relative

	def addItem(self,obj):
		#We assume that, we have a list of same objects.
		if isinstance(self.__object, list):
			self.__object.append(obj)

	def getRawData(self):
		
		return self.data

	def getAndroguardObj(self):

		return self.__object

	def isModified():

		return self.__is_modified

	def writeTo(self):
		#To be implemented
		pass

