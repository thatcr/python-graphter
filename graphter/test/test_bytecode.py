import dis

from graphter import graph, GraphDict
from graphter.bytecode import LOCAL_KEY, LOCAL_VALUE, _local, ATTR_STACK

def test_key():
	@graph
	def funk(a, b):
		return locals()
		
	result = funk(1, 2)
	assert result[LOCAL_KEY] == funk.ref(1, 2)

def test_cache():
	cache = GraphDict()
	counter = 0

	@graph(cache=cache)
	def funk(a, b):
		nonlocal counter
		import pprint; pprint.pprint(getattr(_local, ATTR_STACK))
		counter = counter + 1
		return a + b
	
	funk(1, 2)
	assert counter == 1
	assert cache[funk.ref(1, 2)] == (3, [], [])
	
	funk(1, 2)
	assert counter == 1
	assert cache[funk.ref(1, 2)] == (3, [], [])
	
	funk(1, 3)
	assert funk.ref(1, 3) in cache
	assert counter == 2
	assert cache[funk.ref(1, 3)] == (4, [], [])
	
def test_parent_child():
	cache = GraphDict()
	@graph(cache=cache)
	def child(x):
		return x
		
	@graph(cache=cache)
	def parent(x, y):
		return child(x) + child(y)
		
	parent(1, 2)

	assert cache[parent.ref(1, 2)] == (3, [child.ref(1), child.ref(2)], [])
	assert cache[child.ref(1)] == (1, [], [parent.ref(1, 2)])
	assert cache[child.ref(2)] == (2, [], [parent.ref(1, 2)])
	

