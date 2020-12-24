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

    def test_empty_list(self):
        self.assertEqual(self.parsed("[]"), [])
        self.assertEqual(self.parsed(" [ ] "), [])

    def test_empty_object(self):
        self.assertEqual(self.parsed("{}"), {})
        self.assertEqual(self.parsed(" { } "), {})

    def test_list(self):
        self.assertEqual(self.parsed("[[true], false]"), [[True], False])

    def test_object(self):
        self.assertEqual(self.parsed('{"hello":"there"}'), dict(hello="there"))

    def test_string(self):
        self.assertEqual(
                self.parsed(r'"1\\2\/3\"4\b5\f6\n7\r8\t9"'),
                '1\\2/3"4\b5\f6\n7\r8\t9')
        self.assertEqual(self.parsed(r'"alpha\u1a2b73"'), "alpha\u1a2b73")
        self.assertEqual(self.parsed('""'), "")
