import sys

class Fields(list):

    def __getitem__(self, i):
        if isinstance(i, int):
            if sys.version_info >= (3, 0):
                return super().__getitem__(i) if len(self) > i else ''
            else:
                return super(Fields, self).__getitem__(i) if len(self) > i else ''
        else:
            if sys.version_info >= (3, 0):
                return super().__getitem__(i)
            else:
                return super(Fields, self).__getitem__(i)