from graphter import graph
from inspect import signature

def test_identical_signature():
	def funk(a, b):
		return a + b
	assert signature(funk) == signature(graph(funk))

def test_ref():
	@graph
	def funk(a, b):
		return locals()
	
	assert tuple(funk.ref(1, 2)) == (funk, 1, 2)
	
	
		
	
