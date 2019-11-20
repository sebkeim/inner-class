import unittest
from inner import raw_inner, static_inner, class_inner, inner


class TestBase(unittest.TestCase):
    def setUp(self):
        class Base1:
            @self.inner_mode
            class inner1:
                def method1(self):
                    return "method1"

                def method5(self):
                    return "will be overided by Outer.inner1"

            @self.inner_mode
            class inner2:
                def method2(self):
                    return "method2"

            @self.inner_mode
            class inner3:
                def method6(self):
                    return "will be overided by Outer.inner1"

        self.Base1 = Base1

        class Base2:
            @self.inner_mode
            class inner1:
                def method1(self):
                    return "will be overided by Base1.inner1"

                def method3(self):
                    return "method3"

                def method5(self):
                    return "will be overided by Outer and Base1"

            @self.inner_mode
            class inner2:
                def method4(self):
                    return "method4"

        self.Base2 = Base2

        class Outer(Base1, Base2):
            @self.inner_mode
            class inner1:
                def method5(self):
                    return "method5"

            @self.inner_mode
            class inner3(Base1.inner3):
                # explicit inheritence
                def method6(self):
                    return "method6"

        self.Outer = Outer


class TestRaw(TestBase):
    inner_mode = staticmethod(raw_inner)

    def test_outer_attr_cls(self):
        # outer attribute is not set
        Outer = self.Outer
        Base1 = self.Base1
        Base2 = self.Base2
        self.assertFalse(hasattr(Outer.inner1, "outer"))

    def test_outer_attr_obj(self):
        # outer attribute is not set
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertFalse(hasattr(outer.inner1, "outer"))

    def test_inheritance_cls(self):
        # no inheritence except if explicit
        Outer = self.Outer
        Base1 = self.Base1
        Base2 = self.Base2
        self.assertFalse(issubclass(Outer.inner1, Base1.inner1))
        self.assertFalse(issubclass(Outer.inner1, Base2.inner1))
        self.assertTrue(issubclass(Outer.inner3, Base1.inner3))
        self.assertTrue(Outer.inner2 is Base1.inner2)

    def test_inheritance_obj(self):
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertFalse(issubclass(outer.inner1, base1.inner1))
        self.assertFalse(issubclass(outer.inner1, base2.inner1))
        self.assertTrue(issubclass(outer.inner3, base1.inner3))
        self.assertTrue(outer.inner2 is base1.inner2)
    
    # static_inner allow descriptors but class_inner raise an exception
    def _inner_get(self):
        class Outer:
            @self.inner_mode
            class inner1:
                def __get__(self, outerobj, outercls):
                    pass
    def _inner_set(self):
        class Outer:
            @self.inner_mode
            class inner1:
                def __get__(self, outerobj, value):
                    pass
    def test_descriptor(self):
        self._inner_get()
        self._inner_set()    

class TestStatic(TestRaw):
    inner_mode = staticmethod(static_inner)

    def test_outer_attr_cls(self):
        # outer attr is set  at class definition time
        Outer = self.Outer
        Base1 = self.Base1
        Base2 = self.Base2
        self.assertEqual(Outer.inner1.outer, Outer)
        self.assertEqual(Base1.inner1.outer, Base1)
        self.assertEqual(Base2.inner1.outer, Base2)
        self.assertEqual(Outer.inner2.outer, Base1)
        self.assertEqual(Outer.inner3.outer, Outer)
        self.assertEqual(Base1.inner3.outer, Base1)

    def test_outer_attr_obj(self):
        # outer attr is set at class definition time
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertEqual(outer.inner1.outer, type(outer))
        self.assertEqual(base1.inner1.outer, type(base1))
        self.assertEqual(base2.inner1.outer, type(base2))
        self.assertEqual(outer.inner2.outer, type(base1))
        self.assertEqual(outer.inner3.outer, type(outer))
        self.assertEqual(base1.inner3.outer, type(base1))


class TestClass(TestStatic):
    inner_mode = staticmethod(class_inner)

    def test_outer_attr_cls(self):
        # outer attr dynamically map to class
        Outer = self.Outer
        Base1 = self.Base1
        Base2 = self.Base2
        self.assertEqual(Outer.inner1.outer, Outer)
        self.assertEqual(Base1.inner1.outer, Base1)
        self.assertEqual(Base2.inner1.outer, Base2)
        self.assertEqual(Outer.inner2.outer, Outer)
        self.assertEqual(Outer.inner3.outer, Outer)
        self.assertEqual(Base1.inner3.outer, Base1)

    def test_outer_attr_obj(self):
        # outer attr still map to class
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertEqual(outer.inner1.outer, type(outer))
        self.assertEqual(outer.inner2.outer, type(outer))
        self.assertEqual(outer.inner3.outer, type(outer))
        self.assertEqual(base1.inner1.outer, type(base1))
        self.assertEqual(base1.inner3.outer, type(base1))
        self.assertEqual(base2.inner1.outer, type(base2))

    def test_inheritance_cls(self):
        Outer = self.Outer
        Base1 = self.Base1
        Base2 = self.Base2
        # carried inheritance
        self.assertTrue(issubclass(Outer.inner1, Base1.inner1))
        self.assertTrue(issubclass(Outer.inner1, Base2.inner1))
        # inner derivation
        self.assertFalse(Outer.inner2 is Base1.inner2)
        self.assertTrue(issubclass(Outer.inner2, Base1.inner2))
        self.assertTrue(issubclass(Outer.inner2, Base2.inner2))

    def test_inheritance_obj(self):
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertTrue(issubclass(outer.inner1, base1.inner1))
        self.assertTrue(issubclass(outer.inner1, base2.inner1))
        self.assertFalse(outer.inner2 is base1.inner2)
        self.assertTrue(issubclass(outer.inner2, base1.inner2))
        self.assertTrue(issubclass(outer.inner2, base2.inner2))

    def test_descriptor(self):
        self.assertRaises(ValueError, self._inner_get)
        self.assertRaises(ValueError, self._inner_set)

class TestInner(TestClass):
    inner_mode = staticmethod(inner)

    def test_outer_attr_obj(self):
        # outer attr map to object
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertEqual(outer.inner1().outer, outer)
        self.assertEqual(outer.inner2().outer, outer)
        self.assertEqual(outer.inner3().outer, outer)
        self.assertEqual(base1.inner1().outer, base1)
        self.assertEqual(base1.inner3().outer, base1)
        self.assertEqual(base2.inner1().outer, base2)

    def test_outer_attr_cls_obj(self):
        # acces to iner object from outer class : outer attr map to class
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertEqual(outer.inner1().outer, outer)

    def test_inheritance_obj(self):
        outer = self.Outer()
        inner1 = outer.inner1()
        self.assertEqual(inner1.method1(), "method1")
        self.assertEqual(inner1.method3(), "method3")
        self.assertEqual(inner1.method5(), "method5")
        inner2 = outer.inner2()
        self.assertEqual(inner2.method2(), "method2")
        self.assertEqual(inner2.method4(), "method4")
        inner3 = outer.inner3()
        self.assertEqual(inner3.method6(), "method6")


class TestProperty(TestClass):
    inner_mode = staticmethod(inner.property)

    def test_outer_attr_obj(self):
        # outer attr map to object
        outer = self.Outer()
        base1 = self.Base1()
        base2 = self.Base2()
        self.assertEqual(outer.inner1.outer, outer)
        self.assertEqual(outer.inner2.outer, outer)
        self.assertEqual(outer.inner3.outer, outer)
        self.assertEqual(base1.inner1.outer, base1)
        self.assertEqual(base1.inner3.outer, base1)
        self.assertEqual(base2.inner1.outer, base2)

    def test_inheritance_obj(self):
        outer = self.Outer()
        inner1 = outer.inner1
        self.assertEqual(inner1.method1(), "method1")
        self.assertEqual(inner1.method3(), "method3")
        self.assertEqual(inner1.method5(), "method5")
        inner2 = outer.inner2
        self.assertEqual(inner2.method2(), "method2")
        self.assertEqual(inner2.method4(), "method4")
        inner3 = outer.inner3
        self.assertEqual(inner3.method6(), "method6")

    def test_property(self):
        # a new object is created
        outer = self.Outer()
        inner1a = outer.inner1
        inner1b = outer.inner1
        self.assertFalse(inner1a is inner1b)


class TestCachedProperty(TestProperty):
    inner_mode = staticmethod(inner.cached_property)

    def test_property(self):
        #  object is cached
        outer = self.Outer()
        inner1a = outer.inner1
        inner1b = outer.inner1
        self.assertTrue(inner1a is inner1b)


if __name__ == "__main__":
    unittest.main()
