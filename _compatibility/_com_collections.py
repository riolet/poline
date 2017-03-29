from abc import ABCMeta, abstractmethod
from collections import Iterator

def _check_methods(C, *methods):
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True
generator = type((lambda: (yield))())

class Generator(Iterator):

    __slots__ = ()

    def __next__(self):
        """Return the next item from the generator.
        When exhausted, raise StopIteration.
        """
        return self.send(None)

    @abstractmethod
    def send(self, value):
        """Send a value into the generator.
        Return next yielded value or raise StopIteration.
        """
        raise StopIteration

    @abstractmethod
    def throw(self, typ, val=None, tb=None):
        """Raise an exception in the generator.
        Return next yielded value or raise StopIteration.
        """
        if val is None:
            if tb is None:
                raise typ
            val = typ()
        if tb is not None:
            val = val.with_traceback(tb)
        raise val

    def close(self):
        """Raise GeneratorExit inside generator.
        """
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Generator:
            return _check_methods(C, '__iter__', '__next__',
                                  'send', 'throw', 'close')
        return NotImplemented

Generator.register(generator)