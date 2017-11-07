from utils import Data


class OffsettedItem(object):

	def __init__(self, alignment):

		#super(OffsettedItem, self).__init__()
		self.alignment = alignment
		# should be set later on during the write process
		self.file_off = 0
		# Should be computed based on the available data
		self.write_size = 0
		# Check the instance write size in disk
		self.instance_write_size = 0

	def setFileOff(self, file_off):
		"""
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

		mask = self.alignment - 1
		file_off = ( file_off + mask ) & ~mask
		"""
		res = Data.toAligned(self.alignment, file_off)

		self.file_off = res

		return res

	def getFileOff(self):

		return self.file_off

	def getAbsFileOff(relative):

		return self.file_off + relative

	def getWriteSize(self):

		return self.write_size

	def getAligment(self):

		return self.alignment


class MapItem(OffsettedItem):

    def __init__(self, name_type, section, first_item, last_item, item_count):

        super(MapItem, self).__init__(3 * 4)
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

    def getItemCount(self):

        return self.__item_count

    def getFirstItem(self):

        return self.__first_item

    def getLastItem(self):

        return self.__last_item

    def getSection(self):

        return self.__section

    def writeTo(writer):
        # For now pass, later will be assigned the SectionWriter.method
        pass
