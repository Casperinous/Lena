"""
The concept here is, that we want a generic like Dictionary,
based on a type of an object, which will define it's association.
"""
class TypeDictionary(object):

    def __init__(self, instance_type):

    	print instance_type

        self.instance_type = instance_type
        self.dict = dict()

    def addPair(self, key, value):

        rkey = ''
        if not isinstance(key, basestring):
            rkey = str(key)

        if self._keyExists(rkey):
            print '[-] Duplicate key {0} found for instance {1}'.format(rkey, str(self.instance_type))
        self.dict[rkey] = value

    def removePair(self, key):
        return self.dict.pop(key, 0)

    def getValue(self, key):

        value = None
        try:
            value = self.dict[key]
        except KeyError:
            value = None
            pass
        return value

    def getKey(self, value):

        for key in self.dict:
            if self.dict[key] == value:
                return key
        return None

    def getType(self):

        return self.instance_type

    def _keyExists(self, key):

        for _key in self.dict:
            if key == _key:
                return true

        return False


"""
Here, we will have a typical Cached Dictionary, holding the changes
between various items which, their operations are based on indexes
( stringids, methodids etc etc). It would be nice to have a custom
Item object as a value, holding the old and the new values without
depending on the type of object the values are referring to. ( Dict
type is responsible for holding that kind of information.)
"""
class CachedItemDictionary():


	def __init__(self):

		self.dicts = []

	def createTypeDictionary(self, instance_type):

		dic = self.getDictFromType(instance_type)
		if not dic:
			dct = TypeDictionary(instance_type)
			if dct:
				self.dicts.append(dct)


	def addPairToDict(self, instance_type, key, value):
		dic = self.getDictFromType(instance_type)
		if dic:
			dic.addPair(key, value)

	def removePairFromDict(self, instance_type, key):

		dic = self.getDictFromType(instance_type)
		if dic:
			dic.removePair(key)


	def fillPairsDict(self, instance_type, array, callback=None):

		idx = 0
		dic = self.getDictFromType(instance_type)
		if dic:
			for item in array:
				if callback:
					item = callback(item)
				dic.addPair(item.getOldValue(), item)
				idx += 1

		print '[+] Succesfully filled {0} items in {1} dictionary.'.format(idx, instance_type)

	def getDictFromType(self, instance_type):

		for dic in self.dicts:
			if dic.getType() == instance_type:
				return dic

		return None