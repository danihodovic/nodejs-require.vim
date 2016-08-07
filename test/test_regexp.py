import unittest
import os
import sys

plugin_root = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(plugin_root, 'lib'))

import main

class RequireRegexp(unittest.TestCase):
    def test_package_require(self):
        result = main.extract_require_stmt("require('foo')")
        self.assertEqual('foo', result)

    def test_package_require_relative(self):
        result = main.extract_require_stmt("require('foo/bar/baz')")
        self.assertEqual('foo/bar/baz', result)

    def test_local_require(self):
        result = main.extract_require_stmt("require('./foo')")
        self.assertEqual('./foo', result)

    def test_local_require_nested_paths(self):
        result = main.extract_require_stmt("require('../../foo')")
        self.assertEqual('../../foo', result)

    def test_double_quotes(self):
        result = main.extract_require_stmt('require("bar")')
        self.assertEqual('bar', result)

