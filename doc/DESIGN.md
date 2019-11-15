# Inner class design issues
 

A few notes about various implementation considerations  

## Rejected alternatives

### using base classes

We could replace decorator by a base class 

 ```python

 class A:
    class b(innner):
        pass
```

This would need a custom metaclass (for set_name and __get__)


### stacking @property and @cached_property

```python

 class A:
    @property
    @inner
    class b:
        pass
```

Current standard library implementation of @property and @cached_property are only method decorators .
A fix that extend usage on arbitrary callable would not be that easy.
 

