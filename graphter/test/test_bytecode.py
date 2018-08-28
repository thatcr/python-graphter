from graphter import graph, GraphDict
from graphter.bytecode import LOCAL_KEY, LOCAL_VALUE
import dis

def test_key():
	@graph
	def funk(a, b):
		return locals()
		
	result = funk(1, 2)
	assert result[LOCAL_KEY] == funk.ref(1,2)

def test_cache():
	cache = GraphDict()

	@graph(cache=cache)
	def funk(a, b):
		return a + b
	dis.dis(funk.__code__)
	funk(1,2)
	print(cache)
	assert funk.ref(1, 2) in cache
	
	

