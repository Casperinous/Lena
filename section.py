

class Section():

	def __init__(self,name,alignment,data):
		self.__name = name
		self.__alignment = alignment
		self.__data = data
		#should be set later on during the write process
		self.__file_off = 0
		#Should be computed based on the available data
		self.__write_size = 0


	def set_file_off(self,file_off):

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

	def get_file_off(self):

		return self.__file_off

	def get_abs_file_off(relative):

		return self.__file_off + relative

