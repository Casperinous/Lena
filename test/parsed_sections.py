from androguard.core.bytecodes import dvm
from androguard.core.bytecodes import apk
from androguard.core.bytecodes.dvm import TYPE_MAP_ITEM

FILENAME_INPUT = "../app-debug.apk"


a = apk.APK(FILENAME_INPUT)
vm = dvm.DalvikVMFormat(a.get_dex())

map_items = vm.map_list.map_item

for i in map_items:

	msg = 'Type : [{0}] > code : {1}'.format(TYPE_MAP_ITEM[i.get_type()], format(i.get_type(), '#04x'))
	print  msg