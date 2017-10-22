from buffer import Buffer
from androguard.core.bytecodes.dvm import StringDataItem, writeuleb128


class DexOperation:

	'''
		It should be noted that for now, we are using
		the data structures from the Androguard project.
		Maybe later on we may write our own parser.
	'''
	@staticmethod
	'''
		@string -> simple UTF string to be added
		@cm -> Class Manager ( it is passed on the original definition but it is not used)
	'''
	def create_string_data_item(string,cm):

		'''
			Reverse logic here. We do not care about the original offset,
			as we will perform again a sort operation after adding our string.
			First, we call writeuleb128 on our string and the result is 
			passed to the Buffer object
		'''
		item = None
		encoded_str = writeuleb128(string)
		if encoded_str:
			# Index is set to zero, but we do not really care.
			buff = Buffer(encoded_str)
			item = StringDataItem(buff,cm)
			if item:
				print "[+] Succesfully created StringDataItem!"

		return item



