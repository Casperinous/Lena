

class Section():

	def __init__(self,name,alignment,data,andro_object):
		
		self.__name = name
		self.__alignment = alignment
		#this is the raw data for sections which we dont change
		if data:
			self.__data = data
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

