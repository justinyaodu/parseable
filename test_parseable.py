import unittest


from parseable import *


@parse_from_literal("a")
class LowercaseA(Parseable):
    pass


@parse_from_regex(r"[Bb]*")
class ManyB(Parseable):
    pass


@parse_from_regex(r"\s*([*/+-])(\s*)")
class MathOperatorUnnamedGroup(Parseable):
    pass


@parse_from_regex(r"(\s*)(?P<str>[*/+-])(\s*)")
class MathOperatorNamedGroup(Parseable):
    pass


class TestParseable(unittest.TestCase):
    def test_parseable_parse_from_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Parseable.parse_from("foo", 3)

    def test_lowercase_a(self):
        string = "aab"
        index = 0

        a1, index = LowercaseA.parse_from(string, index)
        self.assertEqual(str(a1), "a")
        self.assertEqual(index, 1)

        a2, index = LowercaseA.parse_from(string, index)
        self.assertEqual(str(a2), "a")
        self.assertEqual(index, 2)

        with self.assertRaises(ParseError):
            a3, index = LowercaseA.parse_from(string, index)

    def test_many_b(self):
        string = "Babba"
        index = 0

        b1, index = ManyB.parse_from(string, index)
        self.assertEqual(str(b1), "B")
        self.assertEqual(index, 1)

        a1, index = LowercaseA.parse_from(string, index)

        b2, index = ManyB.parse_from(string, index)
        self.assertEqual(str(b2), "bb")
        self.assertEqual(index, 4)

        b3, index = ManyB.parse_from(string, index)
        self.assertEqual(str(b3), "")
        self.assertEqual(index, 4)

    def test_math_operator(self):
        self._test_math_operator(MathOperatorUnnamedGroup)
        self._test_math_operator(MathOperatorNamedGroup)

    def _test_math_operator(self, cls):
        string = "\n+ "
        index = 0

        op, index = cls.parse_from(string, index)
        self.assertEqual(str(op), "+")
        self.assertEqual(index, len(string))
