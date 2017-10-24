from section import Section
from writer import Writer

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

	def __init__(self,sections_map):

		if sections_map is None:
			raise ValueError("Section's map should not be None.")
		self.__map = sections_map;

		self.writer = Writer()
		"""
		In order to build the Dex succesfully, we must follow the 
		original order of the sections as it is used in Android's
		source code:
		https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#126
		P.S We do not care about word_data.
		"""

	def __initSections(self):
		self.__parseSections()
		self.sections = [
			self.header,
			self.strings_ids,
			self.type_ids,
			self.proto_ids,
			self.field_ids,
			self.method_ids,
			self.classes_def,
			self.type_list,
			self.string_data_items,
			self.class_data_items,
			self.sec_map
		]
	def __parseSections(self):

		self.header = self.__map.get_item_type( "TYPE_HEADER_ITEM" )
		if self.header:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/HeaderSection.java#38
			self.header = Section('header',4, None, self.header)
		else:
			raise ValueError("Header section should not be None.")


		self.strings_ids = self.__map.get_item_type("TYPE_STRING_ID_ITEM")
		if self.strings_ids:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/StringIdsSection.java#46
			self.strings_ids = Section('strings_ids', 4, None, self.strings_ids)
		else:
			raise ValueError("StringIds section should not be None.")

		self.type_ids = self.__map.get_item_type("TYPE_TYPE_ID_ITEM")
		if self.type_ids:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/TypeIdsSection.java#43
			self.type_ids = Section('type_ids', 4, None, self.type_ids)
		else:
			raise ValueError("TypeIds section should not be None.")

		self.proto_ids = self.__map.get_item_type("TYPE_PROTO_ID_ITEM")
		if self.proto_ids:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ProtoIdsSection.java#43
			self.proto_ids = Section('proto_ids', 4, None, self.proto_ids)
		else:
			raise ValueError("ProtoIds section should not be None.")

		self.field_ids = self.__map.get_item_type( "TYPE_FIELD_ID_ITEM" )
		if self.field_ids:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdsSection.java#31
			self.field_ids = Section('field_ids', 4, None, self.field_ids)
		else:
			raise ValueError("FieldIds section should not be None.")

		self.method_ids = self.__map.get_item_type( "TYPE_METHOD_ID_ITEM" )
		if self.method_ids:
			##https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/MemberIdsSection.java#31
			self.method_ids = Section('method_ids', 4, None, self.method_ids)
		else:
			raise ValueError("MethodIds section should not be None.")

		self.classes_def = self.__map.get_item_type( "TYPE_CLASS_DEF_ITEM" )
		if self.classes_def:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/ClassDefsSection.java#49
			self.classes_def = Section('classes_def', 4, None, self.classes_def)
		else:
			raise ValueError("ClassDef section should not be None.")

		self.type_list = self.__map.get_item_type("TYPE_TYPE_LIST")
		if self.type_list:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#108
			self.type_list = Section('type_list', 4, None, self.type_list )
		else:
			raise ValueError("TypeList section should not be None.")

		self.string_data_items = self.__map.get_item_type("TYPE_STRING_DATA_ITEM")
		if self.string_data_items:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#111
			self.string_data_items = Section('string_data_items', 1, None, self.string_data_items)
		else:
			raise ValueError("StringData section should not be None.")

		self.class_data_items = self.__map.get_item_type("TYPE_CLASS_DATA_ITEM")
		if self.class_data_items:
			#https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen/dex/file/DexFile.java#112
			self.class_data_items = Section('class_data_items', 1, None, self.class_data_items)
		else:
			raise ValueError("ClassData section should not be None.")
		

		# The most important piece of the building process.
		self.sec_map = Section('map', 4, None, self.__map)
		

	def prepareSections(self):
		"""
		Well, being a noob in python and juding from
		the fact that we have multiple and different
		classes as sections, i will probably go with
		isinstance and implement the aproppriate ac-
		tions.
		Dont.Judge.Me.
		I dont like it either.
		"""

		for section in self.sections:
		#Limit actions to sections that are modified
		elem = None
		if section.isModified():
			if isinstance(sections.getAndroguardObj(), list):
				elem = sections.getAndroguardObj()[0]
				# It should not be empty, like really.
			elem = sections.getAndroguardObj()
			if isinstance(elem, StringDataItem ):
				strings = sections.getAndroguardObj()
				strings = self.__sortStringDataItems(strings)




	def __sortStringDataItems(self,arr):
		if arr:
			arr = sorted(arr, key=lambda item: item.data)
		return arr