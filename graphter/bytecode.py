from bytecode import Instr, Label, Compare

LOCAL_KEY = '__graphter_key__'
LOCAL_VALUE = '__graphter_value__'

def _store_key(func, code):
	yield Instr('LOAD_CONST', func)
	for name in code.argnames:
		yield Instr('LOAD_FAST', name)
	yield Instr('BUILD_TUPLE', code.argcount + 1)
	yield Instr('STORE_FAST', LOCAL_KEY)	

def _return_from_cache(func, code, cache):
	label = Label()
	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('LOAD_CONST', cache)
	yield Instr('COMPARE_OP', Compare.IN)
	yield Instr('POP_JUMP_IF_FALSE', label)
	
	yield Instr('LOAD_CONST', cache)
	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('BINARY_SUBSCR')
	yield Instr('RETURN_VALUE')
	
	yield label

def _store_return_value(func, code):
	for instr in code:
		if getattr(instr, 'name', None) =='RETURN_VALUE':
			yield Instr('DUP_TOP')
			yield Instr('STORE_FAST', LOCAL_VALUE)
		yield instr

def _cache_return_value(func, code, cache):
	label = Label()
	yield Instr('LOAD_CONST', Ellipsis)
	yield Instr('STORE_FAST', LOCAL_VALUE)
	
	yield Instr('SETUP_FINALLY', label)
	yield from code
	yield label
	yield Instr('LOAD_FAST', LOCAL_VALUE)
	yield Instr('LOAD_CONST', cache)
	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('STORE_SUBSCR')
	yield Instr('END_FINALLY')
