from bytecode import Instr, Label

LOCAL_KEY = '__graphter_key__'
LOCAL_VALUE = '__graphter_value__'

def _store_key(func, code):
	yield Instr('LOAD_CONST', func)
	for name in code.argnames:
		yield Instr('LOAD_FAST', name)
	yield Instr('BUILD_TUPLE', code.argcount + 1)
	yield Instr('STORE_FAST', "__graphter_key__")	

def _store_return_value(func, code):
	for instr in code:
		if getattr(instr, 'name', None) =='RETURN_VALUE':
			yield Instr('DUP_TOP')
			yield Instr('STORE_FAST', LOCAL_VALUE)
		yield instr

def _cache_return_value(func, code, cache):
	label = Label()
	yield Instr('SETUP_FINALLY', label)
	yield from code
	yield label
	yield Instr('LOAD_FAST', LOCAL_VALUE)
	yield Instr('LOAD_CONST', cache)
	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('STORE_SUBSCR')
	yield Instr('END_FINALLY')
	yield Instr('LOAD_CONST', None)
	yield Instr('RETURN_VALUE')
