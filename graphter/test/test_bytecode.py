import dis

from graphter import graph, GraphDict
from graphter.bytecode import LOCAL_KEY, LOCAL_VALUE
	
def test_key():
	@graph
	def funk(a, b):
		return locals()
		
	result = funk(1, 2)
	assert result[LOCAL_KEY] == funk.ref(1,2)


def test_cache():
	cache = GraphDict()
	counter = 0

	@graph(cache=cache)
	def funk(a, b):
		nonlocal counter
		counter = counter + 1
		return a + b
	
	funk(1, 2)
	assert counter == 1
	assert funk.ref(1, 2) in cache
	
	funk(1, 2)
	import pprint; pprint.pprint(cache)
	dis.dis(funk.__code__)
	assert counter == 1
	
	funk(1, 3)
	assert funk.ref(1, 3) in cache
	assert counter == 2



