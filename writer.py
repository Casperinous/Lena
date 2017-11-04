from utils import Data, ItemIndexer, DexUtils

"""
Experimental implementation of a dict with functions
associated with the kind of class the __object prope-
rty is pointed to in the Section class. It is kind
like reflection, but it is not.
Any other suggestion would be considered a gift.
"""


class ItemWriter:

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#99
    def writeStringIdItem(dex, item):
        # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1826
        dex.getWriter().writeSignedInt(item.get_off())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#60
    def writeTypeIdItem(dex, item):
        # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1864
        dex.getWriter().writeSignedInt(item.get_descriptor_idx())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#129
    def writeProtoIdItem(dex, item):
        # shortyIdx = file.getStringIds().indexOf(shortForm);
        # shortyIdx = ItemIndexer.indexOfStrData(item.get_shorty_idx_value())
        # int returnIdx = file.getTypeIds().indexOf(prototype.getReturnType());
        # int paramsOff = OffsettedItem.getAbsoluteOffsetOr0(parameterTypes);

        dex.getWriter().writeSignedInt(item.get_shorty_idx())
        dex.getWriter().writeSignedInt(item.get_return_type_idx())
        dex.getWriter().writeSignedInt(item.get_parameters_off())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
    def writeFieldIdItem(dex, item):
        dex.getWriter().writeSignedInt(item.get_class_idx())
        dex.getWriter().writeSignedInt(item.get_type_idx())
        dex.getWriter().writeSignedInt(item.get_name_idx())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
    def writeMethodIdItem(dex, item):
        dex.getWriter().writeSignedInt(item.get_class_idx())
        dex.getWriter().writeSignedInt(item.get_type_idx())
        dex.getWriter().writeSignedInt(item.get_name_idx())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#187
    def writeClassDefItem(dex, item):
        dex.getWriter().writeSignedInt(item.get_class_idx())
        dex.getWriter().writeSignedInt(item.get_access_flags())
        dex.getWriter().writeSignedInt(item.get_superclass_idx())
        dex.getWriter().writeSignedInt(item.get_interfaces_off())
        dex.getWriter().writeSignedInt(item.get_source_file_idx())
        dex.getWriter().writeSignedInt(item.get_annotations_off())
        dex.getWriter().writeSignedInt(item.get_class_data_off())
        dex.getWriter().writeSignedInt(item.get_static_values_off())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#110
    def writeTypeItem(dex, item):
        dex.getWriter().writeSignedShort(item.get_type_idx())

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDataItem.java#343
    def writeClassDataItem(dex, item):
        # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L3155
        dex.getWriter().writeBytes(item.get_raw())

    @staticmethod
    def writeStringDataItem(dex, item):
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

    @staticmethod
    def writeMapItem(dex, item):
        # Have to implement google's logic here
        # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MapItem.java#80
        offset = 0
        fitem = item.getFirstItem()
        if fitem:
            offset = item.getSection().getAbsFileOff(fitem.get_off())
        else:
            offset = item.getSection().getFileOff()

        # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MapItem.java#210
        dex.getWriter().writeSignedShort(item.getSection().getTypeId(), True)
        dex.getWriter().writeSignedShort(0, True)
        dex.getWriter().writeSignedInt(item.getItemCount(), True)
        dex.getWriter().writeSignedInt(offset, True)


class SectionWriter:

    @classmethod
    def checkWriterValidity(dex, section):
        writer = dex.getWriter()
        writer.alignTo(section.getAligment())
        Data.checkAligmentValidity(writer.getCursor(), section.getFileOff())


    @staticmethod
    def writeStringIdSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeStringIdItem(dex, item)

    @staticmethod
    def writeTypeIdSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeTypeIdItem(dex, item)

    @staticmethod
    def writeProtoIdSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeProtoIdItem(dex, item)

    @staticmethod
    def writeFieldIdSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeFieldIdItem(dex, item)

    @staticmethod
    def writeMethodIdSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeMethodIdItem(dex, item)

    @staticmethod
    def writeClassDefSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeClassDefItem(dex, item)

    @staticmethod
    def writeTypeListSection(items, section, dex):
        # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#107
        SectionWriter.checkWriterValidity(dex, section)
        dex.getWriter().writeSignedInt(len(items))
        for item in items:
            ItemWriter.writeTypeItem(dex, item)

    @staticmethod
    def writeStringDataSection(items, section, dex):

        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeStringDataItem(dex, item)

    @staticmethod
    def writeClassDataSection(items, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        for item in items:
            ItemWriter.writeClassDataItem(dex, item)

    @staticmethod
    def writeMapItemSection(map_sec, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        # If we passed, we are Jedi Knights !
        items = DexUtils.groupMapSections(dex)
        if items and len(items) > 0:
            writer.writeSignedInt(len(items), True)
            for item in items:
                ItemWriter.writeMapItem(dex, item)


class Buffer:

    def __init__(size):

        self.__buffer = bytearray(size)

        self.__size = size

        self.__idx = 0

    def alignToOff(self, aligment, offset):

        self.__idx = Data.toAligned(aligment, offset)

    def alignTo(self, aligment):

        self.__idx = Data.toAligned(aligment, self.__idx)

    def setCursor(self, offset):

        if offset > self.__size:
            raise Exception("Offset bigger than buffer's size")
        self.__idx = offset

    def getCursor(self):

        return self.__idx


class BufferWriter(Buffer):

    def __init__(size):

        super().__init__(size)

    def writeUnsignedInt(self, data, packed=False):
        if packed:
            data = Data.toUnsignedInt(data)

        self.__buffer[self.__idx: self.__idx + len(data)] = data
        self.__idx += len(data)

    def writeSignedInt(self, data, packed=False):
        if packed:
            data = Data.toSignedInt(data)

        self.__buffer[self.__idx: self.__idx + len(data)] = data
        self.__idx += len(data)

    def writeUnsignedShort(self, data, packed=False):
        if packed:
            data = Data.toUnsignedShort(data)

        self.__buffer[self.__idx: self.__idx + len(data)] = data
        self.__idx += len(data)

    def writeSignedShort(self, data, packed=False):
        if packed:
            data = Data.toSignedShort(packed)

        self.__buffer[self.__idx: self.__idx + len(data)] = data
        self.__idx += len(data)

    def writeBytes(self, data):

        self.__buffer[self.__idx: self.__idx + len(data)] = data
        self.__idx += len(data)

    def writeZeroes(self, num):
        for i in range(0, num):
            self._array.extend('\0')

    def finalize(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.__buffer)
