import unittest


from parseable import *


@parse_from_literal("a")
class LowercaseA(Parseable):
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
