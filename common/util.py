import copy
import json
import logging


logger = logging.getLogger(__name__)


class DictModel(dict):

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(self, '__key', kwargs.pop('__key', None))
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    self[key] = self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                self[arg[0]] = self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    self[key] = self._hook(val)

        for key, val in kwargs.items():
            self[key] = self._hook(val)

    def __setattr__(self, name, value):
        prop = getattr(self.__class__, name, None)
        if prop and isinstance(prop, property):
            return prop.__set__(self, value)
        else:
            self[name] = value

    def __setitem__(self, name, value):
        super().__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, name):
        prop = getattr(self.__class__, name, None)
        if prop and isinstance(prop, property):
            return prop.__get__(self)
        return self.__getitem__(name)

    def __missing__(self, name):
        raise AttributeError(name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
