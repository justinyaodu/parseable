from parseable import *


@parse_from_subclasses
class JSONValue(Parseable):
    pass


@parse_from_literal("true", True)
class JSONTrue(JSONValue):
    pass


@parse_from_literal("false", False)
class JSONFalse(JSONValue):
    pass


@parse_from_literal("null", None)
class JSONNull(JSONValue):
    pass


Whitespace = parse_from_regex(r"[ \n\r\t]*")()
LeftBrace = parse_from_literal("{")()
RightBrace = parse_from_literal("}")()
LeftBracket = parse_from_literal("[")()
RightBracket = parse_from_literal("]")()
Comma = parse_from_literal(",")()
Colon = parse_from_literal(":")()
DoubleQuote = parse_from_literal("\"")()


@parse_from_subclasses
class JSONNumber(JSONValue):
    pass


@parse_from_regex(r"[0-9-]+")
class JSONInteger(JSONNumber):
    @staticmethod
    def compute_value(match):
        try:
            return int(match[0])
        except ValueError as e:
            raise ParseError from e


@parse_from_regex(r"[0-9.eE+-]+")
class JSONFloat(JSONNumber):
    @staticmethod
    def compute_value(match):
        try:
            return float(match[0])
        except ValueError as e:
            raise ParseError from e


@parse_from_subclasses
class JSONChar(Parseable):
    pass


@parse_from_regex(r'\\(["\\/bfnrt])')
class JSONCharEscape(JSONChar):
    _char_map = {
        "\"": "\"",
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    @classmethod
    def compute_value(cls, match):
        return cls._char_map[match[1]]


@parse_from_regex(r"\\u([0-9a-fA-F]{4})")
class JSONCharHex(JSONChar):
    @staticmethod
    def compute_value(match):
        return chr(int(match[1], base=16))


@parse_from_regex(r'[^\u0000-\u001F"\\]', 0)
class JSONCharLiteral(JSONChar):
    pass


class JSONString(JSONValue):
    @classmethod
    def parse_from(cls, string, index):
        match = []
        _, index = parse_and_append(DoubleQuote, string, index, match)
        while True:
            try:
                _, index = parse_and_append(JSONChar, string, index, match)
            except ParseError:
                _, index = parse_and_append(DoubleQuote, string, index, match)
                return cls(match), index

    @staticmethod
    def compute_value(match):
        return "".join(c.value for c in match[1:-1])


@parse_from_sequence(Whitespace, JSONValue, Whitespace)
class JSONElement(Parseable):
    @staticmethod
    def compute_value(match):
        return match[1].value


@parseable_decorator
def parse_comma_separated(inner_class):
    def decorator(cls):
        @classmethod
        def parse_from(cls, string, index):
            match = []
            _, index = parse_and_append(inner_class, string, index, match)
            while True:
                try:
                    _, index = parse_and_append(Comma, string, index, match)
                except ParseError:
                    return cls(match), index
                _, index = parse_and_append(inner_class, string, index, match)
        cls.parse_from = parse_from
        return cls
    return decorator


@parse_comma_separated(JSONElement)
class JSONElements(Parseable):
    @staticmethod
    def compute_value(match):
        return [m.value for m in match if isinstance(m, JSONElement)]


@parse_from_any(JSONElements, Whitespace)
class JSONArrayBody(Parseable):
    @staticmethod
    def compute_value(match):
        if isinstance(match, Whitespace):
            return []
        else:
            return match.value


@parse_from_sequence(LeftBracket, JSONArrayBody, RightBracket)
class JSONArray(JSONValue):
    @staticmethod
    def compute_value(match):
        return match[1].value


@parse_from_sequence(Whitespace, JSONString, Whitespace, Colon, JSONElement)
class JSONMember(Parseable):
    @staticmethod
    def compute_value(match):
        return {match[1].value: match[4].value}


@parse_comma_separated(JSONMember)
class JSONMembers(Parseable):
    @staticmethod
    def compute_value(match):
        value = {}
        for m in match:
            if isinstance(m, JSONMember):
                value |= m.value
        return value


@parse_from_any(JSONMembers, Whitespace)
class JSONObjectBody(Parseable):
    @staticmethod
    def compute_value(match):
        if isinstance(match, Whitespace):
            return {}
        else:
            return match.value


@parse_from_sequence(LeftBrace, JSONObjectBody, RightBrace)
class JSONObject(JSONValue):
    @staticmethod
    def compute_value(match):
        return match[1].value
