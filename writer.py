#from utils import Data, ItemIndexer, DexUtils

from utils import Data
from dexutils import DexUtils
from constants import DEX_MAGIC, HEADER_SIZE, ENDIAN_TAG
from androguard.core.bytecodes.dvm import writeuleb128

class ItemWriter:

    @staticmethod
    def writeHeaderItem(dex, item):
        #https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/HeaderItem.java#66
        """
        int mapOff = file.getMap().getFileOffset();
            Section firstDataSection = file.getFirstDataSection();
            Section lastDataSection = file.getLastDataSection();
            int dataOff = firstDataSection.getFileOffset();
            int dataSize = lastDataSection.getFileOffset() +
                lastDataSection.writeSize() - dataOff;
        """
        mapOff = dex.getMap().getFileOff()
        dataOff = mapOff
        dataSize = dex.getMap().getFileOff() + dex.getMap().getWriteSize()


        """
        // Write the magic number.
            for (int i = 0; i < 8; i++) {
                out.writeByte(MAGIC.charAt(i));
            }
            // Leave space for the checksum and signature.
            out.writeZeroes(24);
            out.writeInt(file.getFileSize());
            out.writeInt(HEADER_SIZE);
            out.writeInt(ENDIAN_TAG);
        """
        writer = dex.getWriter()
        writer.writeBytes(DEX_MAGIC)
        writer.writeZeroes(24)
        writer.writeSignedInt(dex.getDexSize(), True)
        writer.writeSignedInt(HEADER_SIZE, True)
        writer.writeSignedInt(ENDIAN_TAG, True)

        """
            out.writeZeroes(8);
            out.writeInt(mapOff);
            // Write out each section's respective header part.
            file.getStringIds().writeHeaderPart(out);
            file.getTypeIds().writeHeaderPart(out);
            file.getProtoIds().writeHeaderPart(out);
            file.getFieldIds().writeHeaderPart(out);
            file.getMethodIds().writeHeaderPart(out);
            file.getClassDefs().writeHeaderPart(out);
        """
        writer.writeZeroes(8)
        writer.writeSignedInt(mapOff, True)
        dex.getStringIdsSection().writeHeaderPart(writer)
        dex.getTypeIdsSection().writeHeaderPart(writer)
        dex.getProtoIdsSection().writeHeaderPart(writer)
        dex.getFieldIdsSection().writeHeaderPart(writer)
        dex.getMethodIdsSection().writeHeaderPart(writer)
        dex.getClassesSection().writeHeaderPart(writer)

        """
        out.writeInt(dataSize);
        out.writeInt(dataOff);
        """
        writer.writeSignedInt(dataSize, True)
        writer.writeSignedInt(dataOff, True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdItem.java#99
    def writeStringIdItem(dex, item):
        # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1826
        dex.getWriter().writeSignedInt(item.get_string_data_off(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdItem.java#60
    def writeTypeIdItem(dex, item):
        # https://github.com/androguard/androguard/blob/v2.0/androguard/core/bytecodes/dvm.py#L1864
        dex.getWriter().writeSignedInt(item.get_descriptor_idx(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdItem.java#129
    def writeProtoIdItem(dex, item):
        # shortyIdx = file.getStringIds().indexOf(shortForm);
        # shortyIdx = ItemIndexer.indexOfStrData(item.get_shorty_idx_value())
        # int returnIdx = file.getTypeIds().indexOf(prototype.getReturnType());
        # int paramsOff = OffsettedItem.getAbsoluteOffsetOr0(parameterTypes);

        dex.getWriter().writeSignedInt(item.get_shorty_idx(), True)
        dex.getWriter().writeSignedInt(item.get_return_type_idx(), True)
        dex.getWriter().writeSignedInt(item.get_parameters_off(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
    def writeFieldIdItem(dex, item):
        dex.getWriter().writeSignedShort(item.get_class_idx(), True)
        dex.getWriter().writeSignedShort(item.get_type_idx(), True)
        dex.getWriter().writeSignedInt(item.get_name_idx(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdItem.java#63
    def writeMethodIdItem(dex, item):
        dex.getWriter().writeSignedShort(item.get_class_idx(), True)
        dex.getWriter().writeSignedShort(item.get_proto_idx(), True)
        dex.getWriter().writeSignedInt(item.get_name_idx(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefItem.java#187
    def writeClassDefItem(dex, item):
        dex.getWriter().writeSignedInt(item.get_class_idx(), True)
        dex.getWriter().writeSignedInt(item.get_access_flags(), True)
        dex.getWriter().writeSignedInt(item.get_superclass_idx(), True)
        dex.getWriter().writeSignedInt(item.get_interfaces_off(), True)
        dex.getWriter().writeSignedInt(item.get_source_file_idx(), True)
        dex.getWriter().writeSignedInt(item.get_annotations_off(), True)
        dex.getWriter().writeSignedInt(item.get_class_data_off(), True)
        dex.getWriter().writeSignedInt(item.get_static_values_off(), True)

    @staticmethod
    # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeListItem.java#110
    def writeTypeItem(dex, item):
        dex.getWriter().writeSignedShort(item.get_type_idx(), True)

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
            offset = item.getSection().getAbsFileOff(fitem.offset)
        else:
            offset = item.getSection().getFileOff()

        # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MapItem.java#210
        dex.getWriter().writeSignedShort(item.getSection().getTypeId(), True)
        dex.getWriter().writeSignedShort(0, True)
        dex.getWriter().writeSignedInt(item.getItemCount(), True)
        dex.getWriter().writeSignedInt(offset, True)

    @staticmethod
    def writeDalvikCodeItem(dex, item):
        #https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/CodeItem.java#233
        """
        out.writeShort(regSz);
        out.writeShort(insSz);
        out.writeShort(outsSz);
        out.writeShort(triesSz);
        out.writeInt(debugOff);
        out.writeInt(insnsSz);
        """
        dex.getWriter().writeSignedShort(item.get_registers_size(), True)
        dex.getWriter().writeSignedShort(item.get_ins_size(), True)
        dex.getWriter().writeSignedShort(item.get_outs_size(), True)
        dex.getWriter().writeSignedShort(item.get_tries_size(), True)
        dex.getWriter().writeSignedInt(item.get_debug_info_off(), True)
        dex.getWriter().writeSignedInt(item.get_insns_size(), True)

class SectionWriter:

    @staticmethod
    def checkWriterValidity(dex, section):
        writer = dex.getWriter()
        writer.alignTo(section.getAligment())
        Data.checkAligmentValidity(writer.getCursor(), section.getFileOff(), section.getName())

    @staticmethod
    def writeHeaderSection(item, section, dex):
        SectionWriter.checkWriterValidity(dex, section)
        ItemWriter.writeHeaderItem(dex,item)

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
        # dex.getWriter().writeSignedInt(len(items), True)
        for item in items:
            its = item.get_list()
            dex.getWriter().writeSignedInt(len(its), True)
            for it in its: 
                ItemWriter.writeTypeItem(dex, it)

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
            dex.getWriter().writeSignedInt(len(items), True)
            for item in items:
                ItemWriter.writeMapItem(dex, item)


class Buffer:

    def __init__(self, size):

        self.buffer = bytearray(size)

        self.size = size

        self.idx = 0

    def alignToOff(self, aligment, offset):

        self.idx = Data.toAligned(aligment, offset)

    def alignTo(self, aligment):

        self.idx = Data.toAligned(aligment, self.idx)

    def setCursor(self, offset):

        if offset > self.size:
            raise Exception("Offset bigger than buffer's size")
        self.idx = offset

    def getCursor(self):

        return self.idx


class BufferWriter(Buffer):

    def __init__(self, size):

        Buffer.__init__(self, size)

    def writeUnsignedInt(self, data, packed=False):
        if packed:
            data = Data.toUnsignedInt(data)

        self.buffer[self.idx: self.idx + 4] = data
        self.idx += len(data)

    def writeSignedInt(self, data, packed=False):
        if packed:
            data = Data.toSignedInt(data)

        self.buffer[self.idx: self.idx + 4] = data
        self.idx += len(data)

    def writeUnsignedShort(self, data, packed=False):
        if packed:
            data = Data.toUnsignedShort(data)

        self.buffer[self.idx: self.idx + 2] = data
        self.idx += len(data)

    def writeSignedShort(self, data, packed=False):
        if packed:
            data = Data.toSignedShort(packed)

        self.buffer[self.idx: self.idx + 2] = data
        self.idx += len(data)

    def writeBytes(self, data):

        for c in data:
            self.buffer[self.idx: self.idx + 1] = c
            self.idx += 1

    def writeZeroes(self, num):
        for i in range(1, num + 1):
            self.buffer[self.idx: self.idx + i] = '\0'
        self.idx += num

    def finalize(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.buffer)
