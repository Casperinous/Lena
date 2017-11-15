import sys
from androguard.core.bytecodes import dvm
from androguard.core.bytecodes import apk
from androguard.core.bytecodes.dvm import TYPE_MAP_ITEM, DCode

sys.path.append('../')
from dex import Dex

FILENAME_INPUT = "../app-debug.apk"


a = apk.APK(FILENAME_INPUT)
vm = dvm.DalvikVMFormat(a.get_dex())



codes = vm.map_list.get_item_type( "TYPE_CODE_ITEM" )
for code in codes.get_obj():
	dcode = code.get_bc()
	instructions = dcode.get_instructions()
	for instr in instructions:
		ids = instr.get_literals()
		if ids:
			print ' '.join(str(n) for n in ids)