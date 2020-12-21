class Rule:

    nullable = False

    def __init__(self, parent):
        self.parent = parent
        self.production = None
        if self.nullable:
            self.null = False

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}{" (c)" if self.complete else ""}: '
            f'{self.production}>'
        )

    @property
    def complete(self):
        if self.nullable and self.null:
            return True
        else:
            return (
                self.production is not None
                and all(rule.complete for rule in self.production)
            )

    def consume(self, token):
        if self.production is None:
            for prod in self.productions_list():
                if prod[0].accepts(token):
                    self.production = [rule(self) for rule in prod]
                    break
            else:
                if self.nullable:
                    self.null = True
                else:
                    raise ValueError(f'Unexpected token: {token}')
        if self.complete:
            return self.parent.consume(token)
        child_rule = next(rule for rule in self.production if not rule.complete)
        return child_rule.consume(token)

    @classmethod
    def accepts(cls, token):
        return any(prod[0].accepts(token) for prod in cls.productions_list())

    def close(self):
        if self.production is not None:
            for rule in self.production:
                rule.close()
        elif self.nullable:
            self.null = True
        if not self.complete:
            raise ValueError(f'Unexpected EOF')

    @classmethod
    def productions_list(cls):
        raise NotImplementedError()

    def emit(self):
        raise NotImplementedError()


class Token:

    valid_tokens = None

    def __init__(self, parent):
        self.parent = parent
        self.value = None

    def __repr__(self):
        return f'<{self.__class__.__name__}: [{self.value}]>'

    def consume(self, token):
        if token not in self.productions_list():
            raise ValueError(
                f'Unexpected token: {token}. '
                f'Expected one of: {self.productions_list}'
            )
        self.value = token

    @property
    def complete(self):
        return self.value is not None

    @classmethod
    def accepts(cls, token):
        return token in cls.productions_list()

    @classmethod
    def productions_list(cls):
        if cls.valid_tokens is None:
            raise NotImplementedError()
        return cls.valid_tokens

    def emit(self):
        raise NotImplementedError()

    def close(self):
        if self.value is None:
            raise ValueError(
                f'Unexpected EOF while awaiting one of: '
                f'{self.productions_list()}'
            )


class RuleSet:

    def __init__(self):
        self.rules = {}

    def add_rule(self, name, productions, emit, nullable=False):
        if name in self.rules:
            raise ValueError(f'Rule with name {name} already defined.')
        def productions_list(cls):
            return [
                [self.rules[rule_name] for rule_name in production]
                for production in productions
            ]
        attrs = {
            'emit': lambda self: emit(self),
            'nullable': nullable,
            'productions_list': classmethod(productions_list),
        }
        for attr_name, attr in attrs.items():
            if callable(attr):
                attr.__name__ = attr_name
                attr.__qualname__ = f'{name}.{attr_name}'
        NewRule = type.__new__(type, name, (Rule,), attrs)
        self.rules[name] = NewRule

    def add_token(self, name, valid_tokens, emit):
        if name in self.rules:
            raise ValueError(f'Rule with name {name} already defined.')
        attrs = {
            'emit': lambda self: emit(self),
            'valid_tokens': valid_tokens,
        }
        for attr_name, attr in attrs.items():
            if callable(attr):
                attr.__name__ = attr_name
                attr.__qualname__ = f'{name}.{attr_name}'
        NewToken = type.__new__(type, name, (Token,), attrs)
        self.rules[name] = NewToken

    def compile(self, input_, entry_rule_name):
        rule = self.rules[entry_rule_name](None)
        for token in input_:
            rule.consume(token)
        rule.close()
        return rule.emit()
