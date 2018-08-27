from graphter import graph
from inspect import signature

def test_identical_signature():
	def funk(a, b):
		return a + b
	assert signature(funk) == signature(graph(funk))

def test_create_ref():
	@graph
	def funk(a, b):
		return a + b
	
	assert tuple(funk.ref(a, b)) == (funk, a, b)
		
	
