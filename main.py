import argparse

from androguard.misc import AnalyzeAPK 
from androguard.core.bytecodes.apk import APK 
from androguard.core.bytecodes.dvm import DalvikVMFormat


def parseArgs():      
	parser = argparse.ArgumentParser(description='A program modifying an APK to load Ronin shared library.')     
	parser.add_argument('-apk', dest = 'apk', required = True, help = 'Path to the APK file to be analysed.')     
	parser.add_argument('-out', '--output', dest = 'out', required = True, help = 'Destination of the modified files to be saved.')     
	return parser.parse_args()


if __name__ == "__main__":

	args = parseArgs()
	a, d, dx = AnalyzeAPK(args.apk)

	'''
	First let's check that we have access to the map file in order to properly extract
	the sections we want.
	'''
	
	dex_map = d.map_list
	print dex_map

	#strings = d.get_strings()
	#for i in strings:
		#print i

	string_ids = d.map_list.get_item_type('TYPE_STRING_ID_ITEM')
	for str_id in string_ids:
		print str_id.get_string_data_off() 
