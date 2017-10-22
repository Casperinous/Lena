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
	# Lets try to create a StringDataItem

	item = DexOperation.create_string_data_item("Tsipikao",d.get_class_manager())
	if item:
		# We have succesfully created on StringDataItem. Now we must append it to the array.
		d.strings.append(item)
		"""
		Again, based on the Android's source code, we must sort the strings and
		return a new list of StringItemIds based on the newly sorted strings.One
		small difficulty is that, we must perform a special comparison as the data
		of a StringDataItem is modification of a UTF8 string.
		"""
		#For testing purposes, lets do it fast.
		sorted_strings = sorted(d.strings, key=lambda item: item.data)
		"""
		Used for evaluation.
		----------------------
		for item in sorted_strings:
			print item.get_data()
		"""

		#Now, based on these sorted strings, we must generate the offsets on the fly while writing the contents.
