import threading
from bytecode import Instr, Label, Compare

LOCAL_KEY = '__graphter_key__'
LOCAL_VALUE = '__graphter_value__'
LOCAL_PARENT = '__graphter_parent__'
LOCAL_CHILDREN = '__graphter_children__'

ATTR_STACK = '__graphter_stack__'


# a thread local store - ATTR_STACK contains the graph building stack
# of (parent, siblings) that is used to build the parent/child graph

class GraphterLocal(threading.local):
	def __init__(self):
		self.__dict__[ATTR_STACK] = [(None, list())]
_local = GraphterLocal()
	
def _store_key(func, code):
	"""
	Store a tuple representing the current function call under
	a local name, that will be used to refer to this item in 
	the cache.
	"""
	yield Instr('LOAD_CONST', func)
	for name in code.argnames:
		yield Instr('LOAD_FAST', name)
	yield Instr('BUILD_TUPLE', code.argcount + 1)
	yield Instr('STORE_FAST', LOCAL_KEY)	

def _update_siblings():
	"""
	Get the head of the graph building stack and unpack it
	onto the intepreter stack such that 
		TOS   = parent : Ref
		TOS1  = siblings : Set[Ref]  
	then store the parent ref in a local, and add our ref to
	the list of siblings
	"""
	yield Instr('LOAD_CONST', _local)
	yield Instr('LOAD_ATTR', ATTR_STACK)
	yield Instr('LOAD_CONST', -1)
	yield Instr('BINARY_SUBSCR')
	yield Instr('UNPACK_SEQUENCE', 2)	
	yield Instr('STORE_FAST', LOCAL_PARENT)
	yield Instr('LOAD_ATTR', 'append')
	yield Instr('LOAD_FAST', LOCAL_KEY)	
	yield Instr('CALL_FUNCTION', 1)
	yield Instr('POP_TOP')
	
def _return_from_cache(cache):
	"""
	Check the cache for an entry for this function. If it
	exists then return the value store, otherwise carry on.
	"""
	
	# update the parent set in the cache here from the stack
	# cache must have tuple of value, children, parents
	
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


def _update_stack(code):
	yield Instr('LOAD_CONST', _local)
	yield Instr('LOAD_ATTR', ATTR_STACK)
	yield Instr('LOAD_ATTR', 'append')

	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('BUILD_LIST', 0)
	yield Instr('DUP_TOP')
	yield Instr('STORE_FAST', LOCAL_CHILDREN)
	
	yield Instr('BUILD_TUPLE', 2)
	
	yield Instr('CALL_FUNCTION', 1)
	yield Instr('POP_TOP')
	
	label = Label()
	yield Instr('SETUP_FINALLY', label)
	
	yield from code
	
	yield label
	
	yield Instr('LOAD_CONST', _local)
	yield Instr('LOAD_ATTR', ATTR_STACK)
	yield Instr('LOAD_ATTR', 'pop')
	yield Instr('CALL_FUNCTION', 0)
	yield Instr('POP_TOP')
	
	yield Instr('END_FINALLY')
	yield Instr('LOAD_CONST', None)
	yield Instr('RETURN_VALUE')
	
def _cache_return_value(code, cache):
	"""
	Store registered return value in the cache if it is present.
	"""
	
	label = Label()
	for instr in code:
		if getattr(instr, 'name', None) == 'RETURN_VALUE':
			yield Instr('JUMP_ABSOLUTE', label)
			continue
		yield instr
	
	yield from code
	yield label
	
	yield Instr('DUP_TOP')
	yield Instr('LOAD_FAST', LOCAL_CHILDREN)
	yield Instr('LOAD_FAST', LOCAL_PARENT)

	has_parent = Label()
	carry_on = Label()
	
	yield Instr('JUMP_IF_TRUE_OR_POP', has_parent)
	yield Instr('BUILD_LIST', 0)
	yield Instr('JUMP_ABSOLUTE', carry_on)
	
	yield has_parent
	yield Instr('BUILD_LIST', 1)
	yield carry_on
	
	yield Instr('BUILD_TUPLE', 3)
	
	# now get the children and parent from the cache to make the entry
	yield Instr('LOAD_CONST', cache)
	yield Instr('LOAD_FAST', LOCAL_KEY)
	yield Instr('STORE_SUBSCR')
	yield Instr('RETURN_VALUE')
