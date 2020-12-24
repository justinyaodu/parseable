import unittest


from example_json import *


class TestJSON(unittest.TestCase):
    @staticmethod
    def parsed(string):
        return JSONElement.parse(string).value

    def test_literals(self):
        self.assertIs(self.parsed("true"), True)
        self.assertIs(self.parsed("false"), False)
        self.assertIs(self.parsed("null"), None)

        with self.assertRaises(ParseError):
            self.parsed("truffle")

    def test_empty_list(self):
        self.assertEqual(self.parsed("[]"), [])
        self.assertEqual(self.parsed(" [ ] "), [])

        with self.assertRaises(ParseError):
            self.parsed("[")

        with self.assertRaises(ParseError):
            self.parsed("]")

    def test_empty_object(self):
        self.assertEqual(self.parsed("{}"), {})
        self.assertEqual(self.parsed(" { } "), {})

        with self.assertRaises(ParseError):
            self.parsed("{")

        with self.assertRaises(ParseError):
            self.parsed("}")

    def test_list(self):
        self.assertEqual(self.parsed("[[true], false]"), [[True], False])
        self.assertEqual(self.parsed("[7, [null], -456]"), [7, [None], -456])

    def test_object(self):
        self.assertEqual(self.parsed('{"hello":"there"}'), dict(hello="there"))
        self.assertEqual(
                self.parsed(r'{"stuff": [[7]], "foo": "\"bar\""}'),
                {"stuff": [[7]], "foo": '"bar"'})

        for bad_json in ['{true: 7}', '{:9}', '{"foo":}', '{"a":3,}']:
            with self.assertRaises(ParseError):
                self.parsed(bad_json)

    def test_number(self):
        self.assertEqual(self.parsed("2345"), 2345)
        self.assertIsInstance(self.parsed("73"), int)
        self.assertIsInstance(self.parsed("-49"), int)
        self.assertIsInstance(self.parsed("+23.45e9"), float)

        for bad_json in ["23.45.6", "23-7", "e9", "3e4e5"]:
            with self.assertRaises(ParseError):
                self.parsed(bad_json)

    def test_string(self):
        self.assertEqual(
                self.parsed(r'"1\\2\/3\"4\b5\f6\n7\r8\t9"'),
                '1\\2/3"4\b5\f6\n7\r8\t9')
        self.assertEqual(self.parsed(r'"alpha\u1a2b73"'), "alpha\u1a2b73")
        self.assertEqual(self.parsed('""'), "")

        for bad_json in [r'"', r'"\"', r"'hello'", r'"\uqz23"']:
            with self.assertRaises(ParseError):
                self.parsed(bad_json)
