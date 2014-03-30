# -*- coding: utf-8 -*-
"""
    controlbeast.utils.singleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


class CbSingleton:
    """
    Auxiliary class to ease implementing lazy singletons.
    This class must be applied as a decorator instead of inheriting from this class. Example::

       @CbSingleton
       class MyClass(object)

           def __init__(self):
               self._foo = 'bar'

           @property
           def foo(self):
               return self._foo

           @foo.setter
           def foo(self, value):
               self._foo = value

       instance_1 = MyClass.get_instance()
       instance_2 = MyClass.get_instance()

       id(instance_1) == id(instance_2)   # True
       instance_1.foo                     # 'bar'
       instance_2.foo = 'baz'
       instance_1.foo                     # 'baz'


    **Restrictions**

    * The decorated class can define one ``__init__`` function, but this constructor
      is restricted to the ``self`` argument.
    * To get the singleton instance, the :py:meth:`~controlbeast.utils.singleton.CbSingleton.get_instance`
      method has to be used. Trying to use ``__call__`` will result in a :py:exc:`TypeError` being raised.
    * The actual instance will not be created before :py:meth:`~controlbeast.utils.singleton.CbSingleton.get_instance`
      has been called (lazy behaviour).
    * The decorated class cannot be inherited from. Therefore, this decorator can only be applied to final classes.
    * This decorator shows good manners and takes care of ``__doc__``, ``__module__``, ``__name__``, ``__annotations__``
      and ``__qualname__`` context of the decorated class. This allows care-free handling in conjunction with
      automated documentation extraction tools such as Sphinx autodoc or similar.
    """

    _instance = None

    def __init__(self, decorated):
        self._decorated = decorated
        if hasattr(decorated, '__doc__'):
            self.__doc__ = decorated.__doc__
        if hasattr(decorated, '__module__'):
            self.__module__ = decorated.__module__
        if hasattr(decorated, '__name__'):
            self.__name__ = decorated.__name__
        if hasattr(decorated, '__annotations__'):
            self.__annotations__ = decorated.__annotations__
        if hasattr(decorated, '__qualname__'):
            self.__qualname__ = decorated.__qualname__
        if hasattr(decorated, '__mro__'):
            self.__mro__ = decorated.__mro__

    def get_instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its ``__init__`` method.
        On all subsequent calls, the already created instance is returned.
        """
        if not self._instance:
            self._instance = self._decorated()
        return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
