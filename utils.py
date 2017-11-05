import struct
from androguard.core.bytecodes.dvm import writeuleb128, StringDataItem
from androguard.core import bytecode
#from items import MapItem


def stringToMutf8(string):
    """
       After many hours studying, testing and trying to understand Android's code,
       and in conjuction with the Android's docs, in order one to build a StringDataItem
       needs to parse:
       - the string's size in UnsignedLeb128 encoding
       - the bytes of the string
       - one last byte with filled with one zero.

       Based on this, https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringDataItem.java
       of course the fastest way was a bytearray and the use of the 'extend' method.
       Believe me, this took ages.

       out.writeUnsignedLeb128(utf16Size);
       out.write(bytes);
       out.writeByte(0);
   """
    str_length = len(string)
    arr.extend(writeuleb128(str_length))
    arr.extend(string)
    arr.extend('\0')
    return str(arr)


class Data:

    @staticmethod
    def fromUnsignedInt(data):
        return struct.unpack('<I', data)

    @staticmethod
    def fromSignedInt(data):
        return struct.unpack('<i', data)

    @staticmethod
    def fromUnsignedShort(data):
        return struct.unpack('<H', data)

    @staticmethod
    def fromSignedShort(data):
        return struct.unpack('<h', data)

    def toUnsignedInt(data):
        return struct.pack('<I', data)

    @staticmethod
    def toSignedInt(data):
        return struct.pack('<i', data)

    @staticmethod
    def toUnsignedShort(data):
        return struct.pack('<H', data)

    @staticmethod
    def toSignedShort(data):
        return struct.pack('<h', data)

    @staticmethod
    def toAligned(aligment, offset):
        mask = aligment - 1
        return (offset + mask) & ~mask

    @staticmethod
    def getInstance(obj):
        elem = None
        if isinstance(obj, list):
            elem = obj[0]
        else:
            elem = obj
        return elem

    @staticmethod
    def checkAligmentValidity(cursor, offset, name):

        if cursor != offset:
            raise Exception("Oh my god! Aligment mismatching {0} at {1} expecting {2}".format(
                name, cursor, offset))


class ItemsIndexer:

    @staticmethod
    def indexOfStrData(arr, data):
        idx = 0
        for item in arr:
            if item.get_data() == data:
                break
            idx = idx + 1

        if idx == (len(arr) - 1):
            idx = -1

        return idx


class Generator:

    """
    Simplified creation of an instance of StringDataItem
    with just a custom buffer.
    """
    @staticmethod
    def StringDataItem(string):
        mut8_str = stringToMutf8(string)
        buff = bytecode._Bytecode(mut8_str)
        item = None
        if buff:
            item = StringDataItem(buff, None)

        return item


class DexUtils:

    @staticmethod
    def groupMapSections(dex):

        items = []
        for section in dex.getSectionArr():
            if not isinstance(section, MapList):
                arr = section.getRawData()
                item = None
                if isinstance(arr, list):

                    size = len(arr)
                    item = MapItem(section, arr[0], arr[-1], size)
                else:

                    item = MapItem(section, arr, arr, 1)
                items.append(item)
        return items
