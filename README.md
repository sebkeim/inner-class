# inner-class
Advanced inner classes for Python

An [inner or  nested class](https://en.wikipedia.org/wiki/Inner_class)  is a class declared entirely within the body of another class or interface

## The four features

Python does have built-in support for nested or inner classes. Theses classes [can be used](https://www.novixys.com/blog/nested-inner-classes-python)
when you do not want to expose the class, and it is closely related to another class.

Unfortunately this support is rather minimalistic and lack some useful features :


```python
 class MyOuter:
    class MyInner:
       def hello(self):
           print('Hello')
```

### outer attribute

The inner class gain an 'outer' attribute that reference its outer class.

```python
  MyOuter.MyInner.outer == MyOuter
```

### inner derivation
 

When the outer class is derived, the inner class is also derived in order
to point at the derived outer class.


```python
 class MyChildOuter(MyOuter):
    pass

 MyChildOuter.MyInner.outer == MyChildOuter
```

### carried inheritance

When the inner class is redefined in an outer subclass, it will automatically
derivate from the inner class of the outer superclass.

```python
  class MyChildOuter(MyOuter):
     class MyInner:
       pass

  MyChildOuter.MyInner().hello()
  >>>"Hello"
```


This may seem a bit implicit but is desirable for type conformance
(code must continue to work when the parent class is replaced by a child class),
particularly with mix-in classes.



###  inner instantiation
 

the outer attribute of an inner instance store it's outer instance

```python
  outer = MyOuter()
  outer.MyInner() == outer
```

This attribute is already available into inner __init__ constructor.

If the inner object  is created directly from the outer  outer class (and not an instance), it will still store the outer class.


usage
=====

callback, delegate...


###  Implementation
 
This module provide 6 decorators :

**@inner** : support the 4 features

**@class_inner** : remove inner instantiation feature

**@static_inner** : only keep outer attribute feature

**@raw_inner** : a do nothing, useful if we wan't one day to change the language and make @inner the default behavior of inner class in python

**@inner.property** : access to target from outer instance automatically create an instance of the inner class

**@inner.cached_property** :  the  inner instance is only created once and then cached in the __dict__ of the outer instance




###  install

The module have been tested on Python 3.7

python3 setup.py test
python3 setup.py install 

