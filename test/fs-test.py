import unittest
import sys
import os
import tempfile
import shutil

plugin_root = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(plugin_root, 'lib'))

import main

join = os.path.join

class RelativeRequire(unittest.TestCase):

    def test_find_relative_same_dir(self):
        temp_dir = tempfile.mkdtemp(prefix='node-require-test')
        try:
            open(temp_dir + '/required.js', 'a').close()
            result = main.find_relative(temp_dir + '/main.js', './required')

            expected = temp_dir + '/required.js'
            self.assertEqual(expected, result)

        except Exception as err:
            self.fail(err)
            shutil.rmtree(temp_dir)

    def test_find_relative_nested_dir_below(self):
        temp_dir = tempfile.mkdtemp(prefix='node-require-test')
        try:
            nested_dir = temp_dir + '/foo/bar/baz'
            os.makedirs(nested_dir)
            open(nested_dir + '/required.js', 'a').close()
            result = main.find_relative(temp_dir + '/main.js', './foo/bar/baz/required')

            expected = temp_dir + '/foo/bar/baz/required.js'
            self.assertEqual(expected, result)

        except Exception as err:
            self.fail(err)
            shutil.rmtree(temp_dir)

    def test_find_relative_nested_dir_above(self):
        temp_dir = tempfile.mkdtemp(prefix='node-require-test')
        try:
            open(temp_dir + '/required.js', 'a').close()
            current_file = temp_dir + '/foo/main.js'
            result = main.find_relative(current_file, '../required')

            expected = temp_dir + '/required.js'
            self.assertEqual(expected, result)

        except Exception as err:
            self.fail(err)
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
