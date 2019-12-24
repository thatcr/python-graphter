# python-graphter
Dynamic DAG generation from function calls without changing your code. 


# TODO

 [ ] refactor back - just gather the edges, and make caching a re-writing thing.
 [ ] implement both bytecode and wrapper approaches. 
 [ ] test the proxy/node approach... 
 [ ] how to do it in rust? 


 ## RUST nodess

- lifecycle of enclosing request is the cache...
- somehow needs to be added to all functions, passed in
- return value can come from the cache. 
- need some representation of the function call - the node descriptor
- generate a struct of the args? 
- how to represent the edges, since they are polymorphic by definition...
- cache is not - each function can have it's own cache... but should it.
- signature abstraction is the hard part - worst case polymorphism.
- need to define an enum out of line (can't)
- defer to rust's polymorphism - dyn traits.

- edge gathering - can it be thread safe, no caching/recalc issue

- once we cache we have a concurrency issue - need to block other requests 
  for the same node, so that we wait... check out the rust !cached stuff.

- how to link with the edges, to provide dynamic invalidation when set...
- 