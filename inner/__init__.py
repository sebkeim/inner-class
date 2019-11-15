from functools import update_wrapper


def raw_inner(x):
    """do nothing decorator for future backward compatibility :
      this will preserve current behavior for inner-class if a future version
      of the language change the default semantic for inner classes"""
    return x


class static_inner:
    """decorator for outer attribute"""

    def __init__(self, cls):
        self.icls = cls
        self.__doc__ = cls.__doc__

    def __set_name__(self, owner, name):
        self.icls.outer = owner
        setattr(owner, name, self.icls)


class class_inner(static_inner):
    """decorator for outer attribute, inner derivation and carried inheritance"""

    def _innerbases(self, outercls, inherited):
        mro = self.icls.mro()
        name = self.name
        innerparents = []
        for parent in outercls.__bases__:
            try:
                innerparent = getattr(parent, name)
            except AttributeError:
                pass
            else:
                if innerparent not in mro:
                    innerparents.append(innerparent)
        if inherited:
            return (self.icls,) + tuple(innerparents)

        if innerparents:
            selfbases = self.icls.__bases__
            if selfbases == (object,):
                return tuple(innerparents)
            return selfbases + tuple(innerparents)
        return None

    def __set_name__(self, owner, name):
        # inner derivation
        self.name = name

        bases = self._innerbases(owner, False)
        if bases:
            self.icls = type(self.icls)(
                self.icls.__name__, bases, dict(self.icls.__dict__),
            )
        assert "outer" not in self.icls.__dict__
        self.icls.outer = owner

    def __get__(self, outerobj, outercls):
        # carried ineritence
        cls = self.icls
        if cls.outer != outercls:
            assert self.name not in outercls.__dict__

            bases = self._innerbases(outercls, True)
            cls = type(cls)(
                self.name,
                bases,
                {
                    "outer": outercls,
                    "__qualname__": outercls.__name__ + "." + self.name,
                    "__module__": cls.__module__,
                    "__doc__": cls.__doc__,  #'__annotations__':cls.__annotations__
                },
            )

            inner = type(self)(cls)
            inner.name = self.name
            setattr(outercls, self.name, inner)
        return cls


class inner(class_inner):
    """decorator for outer object attribute, inner derivation, carried inheritance
       and instance"""

    is_property = False
    is_cached = False

    @classmethod
    def property(cls, icls):
        """ replicate standard @property decorator """
        obj = cls(icls)
        obj.is_property = True
        return obj

    @classmethod
    def cached_property(cls, icls):
        """ replicate sdtlib @property decorator """
        obj = cls(icls)
        obj.is_property = True
        obj.is_cached = True
        return obj

    def __get__(self, outerobj, outercls):
        icls = class_inner.__get__(self, outerobj, outercls)
        if outerobj == None:
            return icls
        # properties
        if self.is_property:
            a = icls()
            a.outer = outerobj
            if self.is_cached:
                setattr(outerobj, self.name, a)
            return a
        # constructor
        def ctor(*args, **kw):
            a = icls.__new__(icls, *args, **kw)
            a.outer = outerobj
            a.__init__(*args, **kw)
            return a

        update_wrapper(ctor, icls.__init__)
        return ctor
