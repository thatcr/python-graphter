from bytecode import Bytecode
from .bytecode import (
	_store_key, _cache_return_value,
	_return_from_cache, _update_siblings,
	_update_stack
	)

class GraphDict(dict):
	def __hash__(self):
		return id(self)

def graph(f=None, cache=None):
	def _graph(f):
		code = Bytecode.from_code(f.__code__)
		
		if cache is not None:
			code[:] = _cache_return_value(code, cache)
			code[:0] = _return_from_cache(cache)
			code[:] = _update_stack(code)
			code[:0] = _update_siblings()
		code[:0] = _store_key(f, code)
	
		f.__code__ = code.to_code()
		f.ref = lambda *args : (f, ) + args	
		return f
		
	return _graph if f is None else _graph(f)

