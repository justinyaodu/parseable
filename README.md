# parseable

`parseable` is a flexible, declarative, and object-oriented parser generator, written in Python.

## Features

* Create and use parsers at runtime: no source code generation involved
* Represent each symbol type with a Python class, enabling elegant use of class inheritance
* Define how each symbol is parsed using a concise decorator syntax
  * Parse terminal symbols using exact matching or regular expressions
  * Define non-terminal symbols as a sequence of other symbols
  * Implement more complex logic with custom parsing functions
* Decode symbols into the data they represent
  * Easily reuse existing parsing functions, like Python's built-in `int()` and `float()`

## Usage Example

This [simple JSON parser](example_json.py) uses `parseable` to parse [JSON](https://www.json.org/) into Python objects, similar to the built-in `json.dumps` function. It's RFC 8259 compliant, according to nst's [JSON test suite](https://github.com/nst/JSONTestSuite), which I forked [here](https://github.com/justinyaodu/JSONTestSuite).
