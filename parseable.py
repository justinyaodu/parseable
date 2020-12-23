"""Base class and decorators for parsing objects from strings."""


__all__ = [
    "ParseError",
    "Parseable",
    "parse_from_literal",
    "parse_from_regex",
]


import re


class ParseError(Exception):
    pass


class Parseable:
    def __init__(self, match):
        self.match = match

    @staticmethod
    def parse_from(string, index):
        """Parse an object instance from the string at the given index.

        Return a tuple (instance, new_index), or raise a ParseError if
        the object could not be parsed.
        """
        raise NotImplementedError

    def __str__(self):
        if isinstance(self.match, re.Match):
            group = self.match[0]
            try:
                group = self.match[1]
                group = self.match["str"]
            except IndexError:
                pass
            return group
        else:
            return str(self.match)


def parse_from_literal(literal):
    """Decorator for parsing class instances from a literal string."""
    def decorator(cls):
        def parse_from(string, index):
            if string[index : index + len(literal)] == literal:
                return cls(literal), index + len(literal)
            else:
                raise ParseError
        cls.parse_from = parse_from
        return cls
    return decorator


def parse_from_regex(regex):
    """Decorator for parsing class instances from a regex."""
    pattern = re.compile(regex)
    def decorator(cls):
        def parse_from(string, index):
            match = pattern.match(string, index)
            if match:
                return cls(match), index + len(match.group())
            else:
                raise ParseError
        cls.parse_from = parse_from
        return cls
    return decorator
