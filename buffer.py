'''
Code originally used by Androguard in https://github.com/androguard/androguard/blob/master/androguard/core/bytecode.py#L714
representing a different entity. Due to our simplier logic, we combine these 3 classes into one
'''


class Buffer:
    def __init__(self, buff):
        """
        Badly, the stable version of Androguard is v2.0 which was
        published 2-3 years ago. That being said, the source code
        of the stable version is different of the one in the master
        branch.
        ---------------------------------------------------------
        if isinstance(buff,bytearray):
            self.__buff = buff
        else:
            self.__buff = bytearray(buff)
        """
        self.__buff = buff
        self.__idx = 0

    def __getitem__(self, item):
        return self.__buff[item]

    def __len__(self):
        return len(self.__buff)

    def read(self, size):
        buff = self.__buff[self.__idx:self.__idx + size]
        self.__idx += size

        return buff

    def readat(self, off):
        return self.__buff[off:]

    def read_b(self, size):
        return self.__buff[self.__idx:self.__idx + size]

    def set_idx(self, idx):
        self.__idx = idx

    def get_idx(self):
        return self.__idx

    def add_idx(self, idx):
        self.__idx += idx

    def get_buff(self):
        return self.__buff

    def length_buff(self):
        return len(self.__buff)

    def set_buff(self, buff):
        self.__buff = buff

    def save(self, filename):
        buff = self._save()
        with open(filename, "wb") as fd:
            fd.write(buff)
