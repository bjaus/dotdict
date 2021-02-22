import re
from pprint import pformat


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        for arg in args:
            self.update(arg)
        for key, value in kwargs.items():
            self[key] = value

    def __call__(self):
        return self.to_dict()

    def __contains__(self, key):
        return key in self.keys()

    def __delattr__(self, key):
        del self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __eq__(self, other):
        other = self.__ensure_dict(other)
        return self.__dict__ == other

    def __getattr__(self, key):
        try:
            self.__getitem__(key)
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return pformat(self.to_dict())

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.__dict__[key] = self.__traverse(value)

    def __str__(self):
        return self.__repr__()

    def clear(self):
        for key in self.keys():
            self.__delitem__(key)

    def copy(self):
        return self.__class__(**self.__dict__)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return list(self.__dict__.items())

    def keys(self):
        return list(self.__dict__.keys())

    def merge(self, data=None, **kwargs):
        if data is None:
            data = {}
        else:
            data = self.__ensure_dict(data)
        data.update(kwargs)
        for k, v in data.items():
            if k in self:
                if isinstance(self[k], list) and isinstance(v, list):
                    self[k] = self[k] + v
                elif isinstance(self[k], dict) and isinstance(v, dict):
                    self[k].update(v)
                else:
                    self[k] = v
            else:
                self[k] = v

    def pop(self, key, default=None):
        return self.__dict__.pop(key, default)

    def popitem(self):
        return self.__dict__.popitem()

    def set(self, key, value):
        self[key] = value
        return self[key]

    def setdefault(self, key, value):
        if key not in self:
            self.__dict__.setdefault(key, value)
        return self[key]

    def to_dict(self):
        return self.__dict__

    def values(self):
        return list(self.__dict__.values())

    def update(self, data=None, **kwargs):
        if data is None:
            data = {}
        else:
            data = self.__ensure_dict(data)
        data.update(kwargs)
        for k, v in data.items():
            self[k] = v

    @classmethod
    def __traverse(cls, value):
        if not isinstance(value, cls) and hasattr(value, 'to_dict'):
            value = value.to_dict()
        if isinstance(value, dict):
            value = cls(value)
        elif isinstance(value, (list, tuple, set)):
            v = [cls.__traverse(v) for v in value]
            if isinstance(value, tuple):
                value = tuple(v)
            elif isinstance(value, set):
                value = set(v)
            else:
                value = v
        return value

    @classmethod
    def __ensure_dict(cls, obj):
        if isinstance(obj, cls):
            return obj.__dict__
        elif isinstance(obj, dict):
            return obj
        cls.__raise_not_supported(obj)

    @classmethod
    def __raise_not_supported(cls, value):
        t = cls._pretty_type(value)
        raise TypeError(f"{t} is not supported")

    @staticmethod
    def __pretty_type(value):
        t = re.search(r"'(.*?)'", str(type(value)))
        return t.group() if t else type(value)
