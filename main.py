import argparse

from androguard.misc import AnalyzeAPK 
from androguard.core.bytecodes.apk import APK 
from androguard.core.bytecodes.dvm import DalvikVMFormat
from operations import DexOperation


def parseArgs():      
	parser = argparse.ArgumentParser(description='A program modifying an APK to load Ronin shared library.')     
	parser.add_argument('-apk', dest = 'apk', required = True, help = 'Path to the APK file to be analysed.')     
	parser.add_argument('-out', '--output', dest = 'out', required = True, help = 'Destination of the modified files to be saved.')     
	return parser.parse_args()


if __name__ == "__main__":


	args = parseArgs()
	a, d, dx = AnalyzeAPK(args.apk)

	"""
	First let's check that we have access to the map file in order to properly extract
	the sections we want.
	"""
	
	dex_map = d.map_list
	print dex_map

	# Lets try to create a StringDataItem

	item = DexOperation.create_string_data_item("Lola",d.get_class_manager())
	if item:
		print item.show()
