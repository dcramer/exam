from mock import patch, MagicMock
from functools import partial
import types


class fixture(object):

    def __init__(self, thing, *args, **kwargs):
        self.thing = thing
        self.args = args
        self.kwargs = kwargs

    def __get__(self, instance, type=None):
        if not self.thing in instance.__dict__:
            applied = self.__apply(instance)(*self.args, **self.kwargs)
            instance.__dict__[self.thing] = applied

        return instance.__dict__[self.thing]

    def __apply(self, instance):
        if type(self.thing) in (type, types.MethodType):
            return self.thing
        else:
            return partial(self.thing, instance)


class before(object):

    def __init__(self, thing):
        self.thing = thing

    def __call__(self, instance):
        self.thing(instance)


class after(object):

    def __init__(self, thing):
        self.thing = thing

    def __call__(self, instance):
        self.thing(instance)


class around(object):

    def __init__(self, thing):
        self.thing = thing

    def __call__(self, instance):
        return self.thing(instance)


class patcher(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = None

    def __call__(self, func):
        self.func = func
        return self

    def build_patch(self, instance):
        if self.func:
            self.kwargs['new'] = self.func(instance)

        return patch(*self.args, **self.kwargs)
