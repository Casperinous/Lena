from androguard.core.bytecodes.dvm import StringIdItem, TypeIdItem, ProtoIdItem, FieldIdItem, MethodIdItem, ClassDefItem
from utils import SectionWriter
from writer import dispatcher
from items import OffsettedItem


class Section(OffsettedItem):
    def __init__(self, name, alignment, data, andro_object, is_needed_in_header=False):

        super().__init__(alignment)
        self.__name = name
        # this is the raw data for sections which we dont change
        if data:
            self.__data = data
        else
            self.__data = None
        """
        Object could be a list of Androguard's class (list of proto_ids) 
        or one class like the HeaderItem
        """
        self.__object = andro_object
        # Check if modified.
        self.__is_modified = False
        # Check if contributes to header's data
        self.__is_needed_in_hd = is_needed_in_header
        # Experimental Implementation of a callback function to be used when we are writing content in disk.
        self.__callback = None

    def _calculateWriteSize(self):

        elem = Data.getInstance(self.__object)

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

        # TODO - Combine in an OR clause the items that have the same writesize also use else if?
        if isinstance(elem, StringIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#29
            self.__instance_write_size = 4
            # Assign array of Items to .__data property
            self.__data = self.__object
            # Set write size
            self.__write_size = self.__instance_write_size * len(self.__data)
            # set write callback
            self.__callback = SectionWriter.writeStringIdSection

        if isinstance(elem, TypeIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#29
            self.__instance_write_size = 4
            # Assign array of Items to .__data property
            self.__data = self.__object
            self.__write_size = self.__instance_write_size * len(self.__data)
            self.__callback = SectionWriter.writeTypeIdSection

        if isinstance(elem, ProtoIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#32
            self.__instance_write_size = 12
            # Assign array of Items to .__data property
            self.__data = self.__object
            self.__write_size = self.__instance_write_size * len(self.__data)
            self.__callback = SectionWriter.writeProtoIdSection

        if isinstance(elem, FieldIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
            self.__instance_write_size = 8
            # Assign array of Items to .__data property
            self.__data = self.__object
            self.__write_size = self.__instance_write_size * len(self.__data)
            self.__callback = SectionWriter.writeFieldIdSection

        if isinstance(elem, MethodIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
            self.__instance_write_size = 8
            # Assign array of Items to .__data property
            self.__data = self.__object
            self.__write_size = self.__instance_write_size * len(self.__data)
            self.__callback = SectionWriter.writeMethodIdSection

        if isinstance(elem, ClassDefItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#46
            self.__instance_write_size = 32
            # Assign array of Items to .__data property
            self.__data = self.__object
            self.__write_size = self.__instance_write_size * len(self.__data)
            self.__callback = SectionWriter.writeClassDefSection

    def addItem(self, obj):
        # We assume that, we have a list of same objects.
        if isinstance(self.__object, list):
            self.__object.append(obj)

    def getRawData(self):

        return self.__data

    def getAndroguardObj(self):

        return self.__object

    def isModified():

        return self.__is_modified

    def setModified(value):

        return self.__is_modified = value

    def placeItems():
        pass

    def writeTo(self):
        # To be implemented
        pass

    def prepareSection(self):
        pass

    def writeHeaderPart(self, writer):

        writer.writeSignedInt(len(self.__data))
        writer.writeSignedInt(self.getFileOff())


class MixedSection(Section):
    def __init__(self, self, name, alignment, data, andro_object, is_needed_in_header=False):

        super().__init__(name, alignment, data, andro_object, is_needed_in_header)

    def placeItems(self):

        elem = Data.getInstance(self.__object)
        writer_offset = 0

        if isinstance(elem, StringDataItem):
            self.__data = self.__object
            self.__callback = SectionWriter.writeStringDataSection
            # How convinient to have access to such great methods :)
            for item in self.__object:
                # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1775
                off = Data.toAligned(writer_offset)
                item.set_off(off)
                # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MixedItemSection.java#319
                writer_offset = off + (writeuleb128(item.get_utf16_size) + len(item.get_data()) + 1)

            # With a little luck, it might work ...
            self.__callback = dispatcher['StringDataItem']

        elif isinstance(elem, ClassDataItem):
            self.__data = self.__object
            self.__callback = SectionWriter.writeClassDataSection
            for item in self.__object:
                off = Data.toAligned(writer_offset)
                item.set_off(off)
                # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MixedItemSection.java#319
                # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L3167
                writer_offset = off + item.get_length()

        elif isinstance(elem, TypeList):
            self.__data = self.__object.get_list()
            self.__callback = SectionWriter.writeTypeListSection
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#48
            self.__instance_write_size = 2
            self.__write_size = len(self.__data * self.__instance_write_size) + 4
            '''
            Androguard does not have at v2 functions or properties related
            to offsets.
            So, this :
            for item in self.__object.get_list():
                off = Data.toAligned(writer_offset)
                item.off = off
                writer_offset = off + self.__instance_write_size
            Is not necessary for now.
            '''

        elif isinstance(elem, MapList):
            self.__data = self.__object.map_item
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MapItem.java#32
            self.__instance_write_size = 3 * 4
            self.__write_size = len(self.__object.get_obj()) * self.__instance_write_size
            # Abuse of property - wish there was a function instead for optical pleasure :/
            for item in self.__data:
                off = Data.toAligned(writer_offset)
                # Abuse of property again :/ :/
                item.off = off
                writer_offset = off + self.__instance_write_size

        # Set  write size
        if self.__write_size == 0:
            self.__write_size = writer_offset

    def prepareSection(self):
        self.placeItems()
