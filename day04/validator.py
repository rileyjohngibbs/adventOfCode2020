import re
from typing import Callable


class ValidatorMeta(type):

    def __new__(cls, name, bases, attrs):
        new_attrs = {
            attr_name: (
                attr_val
                if type(attr_val) != Field
                else attr_val.make_validator(attr_name)
            )
            for attr_name, attr_val in attrs.items()
        }
        new_attrs['_validators'] = tuple(
            new_attrs[attr_name]
            for attr_name, attr_val in attrs.items()
            if type(attr_val) == Field
        )
        new_attrs['_required'] = {
            attr_name for attr_name, attr_val in attrs.items()
            if type(attr_val) == Field
        }

        def validate(self) -> bool:
            return all(validator(self) for validator in self._validators)

        new_attrs['validate'] = validate
        return super().__new__(cls, name, bases, new_attrs)


class Field:

    METHODS = {
        'length': lambda v, n: len(v) == n,
        'in_': lambda v, args: args[0] <= int(v) <= args[1],
        'regex': lambda v, args: (
            re.match(args[0], v)
            and (args[1] if len(args) > 1 else lambda *a: True)(
                *re.match(args[0], v).groups()
            )
        ),
    }

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', 'new_field')
        for method in self.METHODS:
            if method in kwargs:
                setattr(self, method, kwargs[method])

    def make_validator(field, name=None) -> Callable:
        name = name or field._name
        def validator(self) -> bool:
            return all(
                self.passport.get(name) is not None
                and method_func(
                    self.passport.get(name),
                    getattr(field, method, None),
                )
                for method, method_func in field.METHODS.items()
                if getattr(field, method, None) is not None
            )
        validator.__name__ = name
        return validator


class Validator(metaclass=ValidatorMeta):

    pass


