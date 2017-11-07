from androguard.core.bytecodes.dvm import StringIdItem, TypeHIdItem, ProtoHIdItem, FieldHIdItem, MethodHIdItem, ClassHDefItem, StringDataItem, ClassDataItem, TypeList, MapList
#from utils import SectionWriter
from items import OffsettedItem
from utils import Data
from writer import SectionWriter


class Section(OffsettedItem):

    def __init__(self, typeid, name, alignment, data, andro_object, is_needed_in_header=False):

        OffsettedItem.__init__(self, alignment)
        self.name = name
        print 'Section name :> [{0}]'.format(self.name)
        # this is the raw data for sections which we dont change
        if data:
            self.data = data
        else:
            self.data = None
        """
        Object could be a list of Androguard's class (list of proto_ids) 
        or one class like the HeaderItem
        """
        self.object = andro_object
        # Check if modified.
        self.is_modified = False
        # Check if contributes to header's data
        self.is_needed_in_hd = is_needed_in_header
        # Experimental Implementation of a callback function to be used when we
        # are writing content in disk.
        self.callback = None
        # Expected a short number here.
        self.typeid = typeid


    def _placeItems(self):

        elem = Data.getInstance(self.object)
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
        that self.object is pointed to.
        """

        # TODO - Combine in an OR clause the items that have the same writesize
        # also use else if?
        if isinstance(elem, StringIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#29
            self.instance_write_size = 4
            # Assign array of Items to .data property
            self.data = self.object
            # Set write size
            self.write_size = self.instance_write_size * len(self.data)
            # set write callback
            self.callback = SectionWriter.writeStringIdSection

        if isinstance(elem, TypeHIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#29
            self.instance_write_size = 4
            # Assign array of Items to .data property
            self.data = self.object.get_type()
            self.write_size = self.instance_write_size * len(self.data)
            self.callback = SectionWriter.writeTypeIdSection

        if isinstance(elem, ProtoHIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#32
            self.instance_write_size = 12
            # Assign array of Items to .data property
            self.data = self.object.get_obj()
            self.write_size = self.instance_write_size * len(self.data)
            self.callback = SectionWriter.writeProtoIdSection

        if isinstance(elem, FieldHIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
            self.instance_write_size = 8
            # Assign array of Items to .data property
            self.data = self.object.get_obj()
            self.write_size = self.instance_write_size * len(self.data)
            self.callback = SectionWriter.writeFieldIdSection

        if isinstance(elem, MethodHIdItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#30
            self.instance_write_size = 8
            # Assign array of Items to .data property
            self.data = self.object.get_obj()
            self.write_size = self.instance_write_size * len(self.data)
            self.callback = SectionWriter.writeMethodIdSection

        if isinstance(elem, ClassHDefItem):
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#46
            self.instance_write_size = 32
            # Assign array of Items to .data property
            self.data = self.object.get_obj()
            self.write_size = self.instance_write_size * len(self.data)
            self.callback = SectionWriter.writeClassDefSection


    def addItem(self, obj):
        # We assume that, we have a list of same objects.
        if isinstance(self.data, list):
            self.data.append(obj)

    def getRawData(self):

        return self.data

    def getAndroguardObj(self):

        return self.callback

    def isModified(self):

        return self.is_modified

    def setModified(value):

        self.is_modified = value

    def getTypeId(self):

        return self.typeid

    def placeItems():
        pass

    def writeTo(self, dex):
        if self.callback:
            self.callback(self.data, self, dex)
        

    def prepareSection(self):
        self._placeItems()

    def writeHeaderPart(self, writer):
        pass

    def getName(self):

        return self.name

class MixedSection(Section):

    
    def __init__(self, typeid, name, alignment, data, andro_object, is_needed_in_header=False):

        super(MixedSection, self).__init__(typeid, name, alignment, data, andro_object, is_needed_in_header)
    

    def _placeItems(self):

        
        elem = Data.getInstance(self.getAndroguardObj())
        writer_offset = 0

        if isinstance(elem, StringDataItem):
            self.data = self.object
            self.callback = SectionWriter.writeStringDataSection
            # How convinient to have access to such great methods :)
            for item in self.object:
                # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1775
                off = Data.toAligned(self.__aligment, writer_offset)
                item.set_off(off)
                # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MixedItemSection.java#319
                writer_offset = off + \
                    (writeuleb128(item.get_utf16_size) + len(item.get_data()) + 1)

            # With a little luck, it might work ...
            self.callback = SectionWriter.writeStringDataSection

        elif isinstance(elem, ClassDataItem):
            self.data = self.object
            self.callback = SectionWriter.writeClassDataSection
            for item in self.object:
                off = Data.toAligned(self.__aligment, writer_offset)
                item.set_off(off)
                # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MixedItemSection.java#319
                # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L3167
                writer_offset = off + item.get_length()

        elif isinstance(elem, TypeList):
            self.data = self.object.get_list()
            self.callback = SectionWriter.writeTypeListSection
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#48
            self.instance_write_size = 2
            self.write_size = len(
                self.data * self.instance_write_size) + 4
            '''
            Androguard does not have at v2 functions or properties related
            to offsets.
            So, this :
            for item in self.object.get_list():
                off = Data.toAligned(writer_offset)
                item.off = off
                writer_offset = off + self.instance_write_size
            Is not necessary for now.
            '''

        elif isinstance(elem, MapList):
            self.data = self.object.map_item
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MapItem.java#32
            self.instance_write_size = 3 * 4
            self.callback = Section.writeMapItemSection
            self.write_size = len(
                self.object.get_obj()) * self.instance_write_size
            # Abuse of property - wish there was a function instead for optical
            # pleasure :/
            for item in self.data:
                off = Data.toAligned(self.__aligment, writer_offset)
                # Abuse of property again :/ :/
                item.off = off
                writer_offset = off + self.instance_write_size

        # Set  write size
        if self.write_size == 0:
            self.write_size = writer_offset

    def prepareSection(self):
        self._placeItems()

    def writeHeaderPart(self, writer):

        writer.writeSignedInt(len(self.data))
        writer.writeSignedInt(self.getFileOff())
