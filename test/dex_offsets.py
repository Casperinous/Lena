import sys
from androguard.core.bytecodes import dvm
from androguard.core.bytecodes import apk
from androguard.core.bytecodes.dvm import TYPE_MAP_ITEM

sys.path.append('../')
from dex import Dex

FILENAME_INPUT = "../app-debug.apk"

print '[*] Getting map_list ....'
a = apk.APK(FILENAME_INPUT)
vm = dvm.DalvikVMFormat(a.get_dex())

print len(vm.get_all_fields())
print len(vm.map_list.get_item_type("TYPE_FIELD_ID_ITEM").get_obj())