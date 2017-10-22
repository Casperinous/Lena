from buffer import Buffer
from androguard.core.bytecodes.dvm import StringDataItem, writeuleb128


def _decode(b):
    # decode arbitrary utf8 codepoints, tolerating surrogate pairs, nonstandard encodings, etc.
    for x in b:
        if x < 128:
            yield x
        else:
            # figure out how many bytes
            extra = 0
            for i in range(6, 0, -1):
                if x & (1<<i):
                    extra += 1
                else:
                    break

            bits = x % (1 << 6-extra)
            for _ in range(extra):
                bits = (bits << 6) ^ (next(b) & 63)
            yield bits

def _fixPairs(codes):
    # convert surrogate pairs to single code points
    for x in codes:
        if 0xD800 <= x < 0xDC00:
            high = x - 0xD800
            low = next(codes) - 0xDC00
            yield 0x10000 + (high << 10) + (low & 1023)
        else:
            yield x


def decode(b):
	return ''.join(map(chr, _fixPairs(_decode(iter(b)))))

class DexOperation:

	"""
	It should be noted that for now, we are using
	the data structures from the Androguard project.
	Maybe later on we may write our own parser.
	"""
	
	"""
	@string -> simple UTF string to be added
	@cm -> Class Manager ( it is passed on the original definition but it is not used)
	"""
	@staticmethod
	def create_string_data_item(string,cm):

		"""
			Reverse logic here. We do not care about the original offset,
			as we will perform again a sort operation after adding our string.
			First, we call writeuleb128 on our string and the result is 
			passed to the Buffer object
		"""

		print 
		item = None
		#encoded_str = writeuleb128(int(string))
		encoded_str = string.encode('utf-8')
		s = bytearray(encoded_str)
		print s[0:len(s)]
		if encoded_str:
			# Index is set to zero, but we do not really care.
			buff = Buffer(encoded_str)
			print '[{0}]'.format(buff.read(1))
			print ord(buff.read(1))
			item = StringDataItem(buff,cm)
			if item:
				print "[+] Succesfully created StringDataItem!"

		return item



