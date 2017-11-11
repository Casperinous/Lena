from androguard.core.bytecodes.dvm import TYPE_MAP_ITEM
from section import Section, MixedSection
from writer import BufferWriter
import copy

"""
Original structure of the Dex file after being generated:

---------------
|  header     | 
|  stringIds  | 
|  typeIds    | 
|  protoIds   | 
|  fieldIds   | 
|  methodIds  |
|  classDefs  | 
|  wordData   | 
|  typeLists  | 
|  stringData | 
|  byteData   |
|  classData  | 
|     map     |
---------------


Before writing to disk, a check is being performed
so as to verify and add all the data to the custom
defined structures. Notice that, header is called 
last, because it is depending heavily on other se-
ctions.

--------------------------------------------------
classDefs.prepare();
classData.prepare();
wordData.prepare();
byteData.prepare();
methodIds.prepare();
fieldIds.prepare();
protoIds.prepare();
typeLists.prepare();
typeIds.prepare();
stringIds.prepare(); <--- Here we set the relative offsets of the strings, which will be later added to the file relative index.
stringData.prepare();
header.prepare();

"""


class Dex:

    def __init__(self, sections_map):

        if sections_map is None:
            raise ValueError("Section's map should not be None.")
        self.__map = sections_map

        self.__writer = None

        self.__size = 0
        """
        In order to build the Dex succesfully, we must follow the 
        original order of the sections as it is used in Android's
        source code:
        https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#126
        P.S We do not care about word_data.
        ^
        |
        |
        --------- Shame on me. Shame. I did not correctly understand the Dex Layout, excluding from code section, the
                   most important one. How did i manage to do this. How.
        """

    def initSections(self):
        self._parseSections()
        self.sections = [
            self.header,
            self.strings_ids,
            self.type_ids,
            self.proto_ids,
            self.field_ids,
            self.method_ids,
            self.classes_def,
            self.word_data,
            self.type_list,
            self.string_data_items,
            self.class_data_items,
            self.sec_map
        ]

    def _parseSections(self):

        self.header = self.__map.get_item_type("TYPE_HEADER_ITEM")
        if self.header:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/HeaderSection.java#38
            self.header = Section(0x00, 'header', 4, None, self.header)
        else:
            raise ValueError("Header section should not be None.")

        self.strings_ids = self.__map.get_item_type("TYPE_STRING_ID_ITEM")
        if self.strings_ids:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdsSection.java#46
            self.strings_ids = Section(0x01,
                                       'strings_ids', 4, None, self.strings_ids, True)
        else:
            raise ValueError("StringIds section should not be None.")

        self.type_ids = self.__map.get_item_type("TYPE_TYPE_ID_ITEM")
        if self.type_ids:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdsSection.java#43
            self.type_ids = Section(
                0x02, 'type_ids', 4, None, self.type_ids, True)
        else:
            raise ValueError("TypeIds section should not be None.")

        self.proto_ids = self.__map.get_item_type("TYPE_PROTO_ID_ITEM")
        if self.proto_ids:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdsSection.java#43
            self.proto_ids = Section(0x03,
                                     'proto_ids', 4, None, self.proto_ids, True)
        else:
            raise ValueError("ProtoIds section should not be None.")

        self.field_ids = self.__map.get_item_type("TYPE_FIELD_ID_ITEM")
        if self.field_ids:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdsSection.java#31
            self.field_ids = Section(0x04,
                                     'field_ids', 4, None, self.field_ids, True)
        else:
            raise ValueError("FieldIds section should not be None.")

        self.method_ids = self.__map.get_item_type("TYPE_METHOD_ID_ITEM")
        if self.method_ids:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdsSection.java#31
            self.method_ids = Section(0x05,
                                      'method_ids', 4, None, self.method_ids, True)
        else:
            raise ValueError("MethodIds section should not be None.")

        self.classes_def = self.__map.get_item_type("TYPE_CLASS_DEF_ITEM")
        if self.classes_def:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefsSection.java#49
            self.classes_def = Section(0x06,
                                       'classes_def', 4, None, self.classes_def, True)
        else:
            raise ValueError("ClassDef section should not be None.")

        
        self.word_data = self.__map.get_item_type( "TYPE_CODE_ITEM" )
        if self.word_data:
            self.word_data = MixedSection(0x2001, 'code_section', 4, None, self.word_data, False)
        else:
            raise ValueError("Code section should not be None.")

        self.type_list = self.__map.get_item_type("TYPE_TYPE_LIST")
        if self.type_list:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#108
            self.type_list = MixedSection(
                0x1001, 'type_list', 4, None, self.type_list)
        else:
            raise ValueError("TypeList section should not be None.")

        self.string_data_items = self.__map.get_item_type(
            "TYPE_STRING_DATA_ITEM")
        if self.string_data_items:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#111
            self.string_data_items = MixedSection(0x2002,
                                                  'string_data_items', 1, None, self.string_data_items)
        else:
            raise ValueError("StringData section should not be None.")

        self.class_data_items = self.__map.get_item_type(
            "TYPE_CLASS_DATA_ITEM")
        if self.class_data_items:
            # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#112
            self.class_data_items = MixedSection(0x2000,
                                                 'class_data_items', 1, None, self.class_data_items)
        else:
            raise ValueError("ClassData section should not be None.")

        self.sec_map = MixedSection(0x2001, 'map', 4, None, self.__map)

        # The most important piece of the building process.
        # Must be initialized after all the items have been finalized in other sections.
        # self.sec_map = MixedSection('map', 4, None, self.__map)

    def writeToDisk(self):
        for section in self.sections:
            section.writeTo(self)

        self.__writer.finalize('classes.dex')

    def saveSectionChanges(self, section):

        andro_obj = section.getAndroguardObj()
        if andro_obj:
            mapped_obj = Data.getInstance(andro_obj)
            if mapped_obj:
                # Really, what i am thinking.
                # Maybe the slowest, but i think it is unavoidable?
                # self.__map.get_item_type(TYPE_MAP_ITEM[mapped_obj.get_type()])
                # = copy.deepcopy(andro_obj)
                pass

    def addItemToSection(self, section, item):

        # TODO - Must.check.for.None.Rly.
        section.setModified(True)
        section.addItem(item)

    def prepareSections(self):
        """
        Well, being a noob in python and juding from
        the fact that we have multiple and different
        classes as sections, i will probably go with
        isinstance and implement the aproppriate ac-
        tions.
        Dont.Judge.Me.
        I dont like it either.

        Also, all sections must have their items:
        - placed
        - saved in the original Androguard's map object
        - have their offsets set.
        """

        # https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#501
        offset = 0
        for section in self.sections:
            if section.isModified():
                # Well must be done.
                self.saveSectionChanges(section)
            placedAt = section.setFileOff(offset)
            # There should be a lot of error checking, but it is late you know.
            # Later.
            section.prepareSection()
            # Well size is defined now so get it.
            offset = placedAt + section.getWriteSize()

        if offset > 0:
            self.__size = offset
            print "Dex's size {0}".format(offset)
            self.__writer = BufferWriter(offset)

    def __sortStringDataItems(self, arr):
        if arr:
            arr = sorted(arr, key=lambda item: item.data)
        return arr

    def getWriter(self):

        return self.__writer

    def getStringIdsSection(self):

        return self.strings_ids

    def getTypeIdsSection(self):

        return self.type_ids

    def getProtoIdsSection(self):

        return self.proto_ids

    def getFieldIdsSection(self):

        return self.field_ids

    def getMethodIdsSection(self):

        return self.method_ids

    def getClassesSection(self):

        return self.classes_def

    def getMap(self):

        return self.sec_map

    def getSectionArr(self):

        return self.sections

    def getDexSize(self):

        return self.__size

