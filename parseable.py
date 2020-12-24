"""Base class and decorators for parsing objects from strings."""


__all__ = [
    "ParseError",
    "Parseable",
    "parse_from_literal",
    "parse_from_regex",
    "parse_from_any",
    "parse_from_sequence",
    "parse_from_subclasses",
    "parseable_decorator",
    "parse_and_append",
]


import re


class ParseError(Exception):
    pass


class Parseable:
    """Represent objects that can be parsed from a string.

    Instances of this class form the nodes of a syntax tree.
    """
    def __init__(self, match):
        """Initialize an object instance from the match object.

        The type of the match object is determined by the implementation
        of parse_of. Raise ParseError if the object instance cannot be
        initialized from the match object.
        """
        self.value = type(self).compute_value(match)

    @classmethod
    def parse_from(cls, string, index):
        """Parse an instance of this class from an index in a string.

        Return a tuple (instance, new_index), or raise ParseError if the
        object could not be parsed.
        """
        raise NotImplementedError

    @classmethod
    def parse(cls, string):
        """Parse an instance of this class from a complete string.

        Return the new instance. Raise ParseError if the object could
        not be parsed, or if the string was not completely parsed.
        """
        instance, index = cls.parse_from(string, 0)
        if index == len(string):
            return instance
        else:
            raise ParseError

    @staticmethod
    def compute_value(match):
        """Compute the parsed value of this node.

        Raise ParseError if the match cannot be parsed.
        """
        return None


def parseable_decorator(class_decorator):
    """Meta-decorator for Parseable class decorators.

    Return a modified decorator which creates a new Parseable subclass
    if one is not specified, and raises TypeError if its argument is not
    a subclass of Parseable.
    """
    def wrapper(cls=None):
        if cls is None:
            cls = type("AnonymousParseable", (Parseable,), {})
        elif not issubclass(cls, Parseable):
            raise TypeError(f"{cls} is not a subclass of Parseable.")
        return class_decorator(cls)
    return wrapper


def parse_from_literal(literal, value=NotImplemented):
    """Decorator for parsing class instances from a literal string.

    If the second argument is provided, it will be used as the return
    value for the compute_value method of the class.
    """
    @parseable_decorator
    def decorator(cls):
        @staticmethod
        def parse_from(string, index):
            if string[index : index + len(literal)] == literal:
                return cls(literal), index + len(literal)
            else:
                raise ParseError
        cls.parse_from = parse_from

        if value is not NotImplemented:
            @staticmethod
            def compute_value(match):
                return value
            cls.compute_value = compute_value

        return cls
    return decorator


def parse_from_regex(regex, group=None):
    """Decorator for parsing class instances from a regex.

    If the second argument is provided, the regex group with that name
    or index will be returned by the compute_value method of the class.
    """
    pattern = re.compile(regex)

    @parseable_decorator
    def decorator(cls):
        @staticmethod
        def parse_from(string, index):
            match = pattern.match(string, index)
            if match:
                return cls(match), index + len(match.group())
            else:
                raise ParseError
        cls.parse_from = parse_from

        if group is not None:
            @staticmethod
            def compute_value(match):
                return match[group]
            cls.compute_value = compute_value

        return cls
    return decorator


def parse_from_any(*classes):
    """Decorator for parsing a variably-typed class instance.

    Attempt to parse the input as each of the provided classes, passing
    the first successfully parsed class instance to the constructor of
    this class. This operation is short-circuiting. Raise ParseError if
    none of the classes are parseable from the input.
    """
    @parseable_decorator
    def decorator(cls):
        @staticmethod
        def parse_from(string, index):
            for wrapped_class in classes:
                try:
                    instance, index = wrapped_class.parse_from(string, index)
                    return cls(instance), index
                except ParseError:
                    pass
            raise ParseError
        cls.parse_from = parse_from
        return cls
    return decorator


def parse_and_append(cls, string, index, match):
    """Utility function which wraps a call to parse_from.

    Call parse_from on the specified class, append the new instance to
    the match list, and return the original return value of parse_from.
    This can be used in complex parse_from implementations to avoid
    writing repetitive list append statements for each parsed child.
    """
    instance, index = cls.parse_from(string, index)
    match.append(instance)
    return instance, index


def parse_from_sequence(*classes):
    """Decorator for parsing a fixed sequence of class instances.

    Parse an instance of each class in the given order, and pass the
    list of instances to the constructor of this class.
    """
    @parseable_decorator
    def decorator(cls):
        @staticmethod
        def parse_from(string, index):
            match = []
            for inner_class in classes:
                _, index = parse_and_append(inner_class, string, index, match)
            return cls(match), index
        cls.parse_from = parse_from
        return cls
    return decorator


@parseable_decorator
def parse_from_subclasses(cls):
    """Decorator for parsing this class' first parseable subclass.

    Equivalent to calling parse_from_any with the direct subclasses of
    this class.
    """
    @staticmethod
    def parse_from(string, index):
        match = []
        for subclass in cls.__subclasses__():
            try:
                return subclass.parse_from(string, index)
            except ParseError:
                pass
        raise ParseError
    cls.parse_from = parse_from
    return cls
