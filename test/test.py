import sys
from androguard.core.bytecodes import dvm
from androguard.core.bytecodes import apk
from androguard.core.bytecodes.dvm import TYPE_MAP_ITEM

sys.path.append('../')
from dex import Dex

FILENAME_INPUT = "../app-debug.apk"


a = apk.APK(FILENAME_INPUT)
vm = dvm.DalvikVMFormat(a.get_dex())


dex = Dex(vm.map_list)

if dex:
	dex.initSections()
	dex.prepareSections()
	dex.writeToDisk()
