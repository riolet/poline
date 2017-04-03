import sys
import poline.utilfuncs

class Field(str):
    def h(self, **kwargs):
        return  poline.utilfuncs.bytesize(self, **kwargs)
    def i(self, **kwargs):
        return int(self, **kwargs)
    def f(self):
        return float(self)


class Fields(list):

    def __getitem__(self, i):
        if isinstance(i, int):
            if sys.version_info >= (3, 0):
                return Field(super().__getitem__(i) if len(self) > i else '')
            else:
                return Field(super(Fields, self).__getitem__(i) if len(self) > i else '')
        else:
            if sys.version_info >= (3, 0):
                return Field(super().__getitem__(i))
            else:
                return Field(super(Fields, self).__getitem__(i))