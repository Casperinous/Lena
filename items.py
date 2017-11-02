from utils import Data


class OffsettedItem:

	def __init__(self, alignment):

		self.__alignment = alignment
		# should be set later on during the write process
        self.__file_off = 0
        # Should be computed based on the available data
        self.__write_size = 0
        # Check the instance write size in disk
        self.__instance_write_size = 0

    def setFileOff(self, file_off):

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

        mask = self.__alignment - 1
        file_off = ( file_off + mask ) & ~mask
        '''
        res = Data.toAligned(self.__alignment, file_off)
        self.__file_off = res
        return res

    def getFileOff(self):

        return self.__file_off

    def getAbsFileOff(relative):

        return self.__file_off + relative

    def getWriteSize(self):

        return self.__write_size


class MapItem(OffsettedItem):

	def __init__(self, name_type, section, first_item, last_item, item_count ):

		super().__init__(3*4)
		'''
		private final ItemType type;
		/** {@code non-null;} section this instance covers */
		private final Section section;
		/**
		* {@code null-ok;} first item covered or {@code null} if this is
		* a self-reference
		*/
		private final Item firstItem;
		/**
		* {@code null-ok;} last item covered or {@code null} if this is
		* a self-reference
		*/
		private final Item lastItem;
		/**
		* {@code > 0;} count of items covered; {@code 1} if this
		* is a self-reference
		*/
		private final int itemCount;
		'''
		self.__type = name_type
		self.__section = section
		self.__first_item = first_item
		self.__last_item = last_item
		self.__item_count = item_count



