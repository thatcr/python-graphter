from graphter import graph
from inspect import signature

def test_identical_signature():
	def funk(a, b): pass
	assert signature(funk) == signature(graph(funk))

def test_ref():
	@graph
	def funk(a, b): pass
	assert tuple(funk.ref(1, 2)) == (funk, 1, 2)
	
	
		
	
