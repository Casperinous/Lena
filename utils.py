import struct
from androguard.core.bytecodes.dvm import writeuleb128, StringDataItem
from androguard.core import bytecode


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
    def toUnsignedInt(data):
        return struct.unpack('<I', data)

    @staticmethod
    def toSignedInt(data):
        return struct.unpack('<i', data)

    @staticmethod
    def toUnsignedShort(data):
        return struct.unpack('<H', data)

    @staticmethod
    def toSignedShort(data):
        return struct.unpack('<h', data)

    @staticmethod
    def toAligned(aligment, offset):
        mask = alignment - 1
        return (offset + mask) & ~mask

    @staticmethod
    def getInstance(obj):
        elem = None
        if isinstance(obj, list):
            elem = obj[0]
        else
            elem = obj
        return elem


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
    @staticmethod

    """
    Simplified creation of an instance of StringDataItem
    with just a custom buffer.
    """

    def StringDataItem(string):
        mut8_str = stringToMutf8(string)
        buff = bytecode._Bytecode(mut8_str)
        item = None
        if buff:
            item = StringDataItem(buff, None)

        return item
