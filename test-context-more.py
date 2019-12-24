import sys

class Context:
    def __init__(self, *args):
        self.coord = args
        self.frame = sys._getframe(1)

    def __enter__(self):
        return Ellipsis

    def __exit__(self, type, value, traceback):
        return False



def fun(a, b):
    with Context(fun, a, b) as __retval__:
        if __retval__ is not Ellipsis:
            return __retval__

        __retval__ = a + b
        return __retval__


import dis
dis.dis(fun)

# OR

class Context:
    def __getitem__(self, key):
        return Ellipsis

    def __setitem__(self, key, value):
        pass

ctx = Context()

def fun(a, b):
    __coord__ = (fun, a, b)
    __retval__ = ctx[__coord__]

    if __retval__ is not Ellipsis:
        return __retval__

    # or embed the cache call on each return value, don't use a block?
    try:
        __retval__ = a + b; return __retval__
    finally:
        ctx[__coord__] = __retval__



