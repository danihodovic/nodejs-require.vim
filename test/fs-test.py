import unittest
import sys
import os
import tempfile
import shutil
import json

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

        finally:
            shutil.rmtree(temp_dir)

@unittest.expectedFailure
class PackageRequire(unittest.TestCase):

    def test_find_main_file_root_dir(self):
        '''
        Finds a file specified as "main" in package.json
        directory structure:

        dir/
            main.js         <- We are here
            package.json
            node_modules/
                package/
                    package.json
                    index.js    <- Find this file
        '''

        temp_dir = tempfile.mkdtemp(prefix='node-require-test')
        try:
            os.makedirs(temp_dir + '/node_modules/package')
            package_json = open(temp_dir + '/node_modules/package/package.json', 'w')
            json.dump({'main': 'foo.js'}, package_json)
            open(temp_dir + '/node_modules/package/foo.js', 'w').close()

            current_file = temp_dir + '/main.js'
            result = main.find_relative(current_file, 'package')
            expected = temp_dir + '/node_modules/package/foo.js'
            self.assertEqual(expected, result)

        except Exception as err:
            self.fail(err)

        finally:
            shutil.rmtree(temp_dir)

    def test_find_main_file_other_dir(self):
        temp_dir = tempfile.mkdtemp(prefix='node-require-test')
        try:
            os.makedirs(temp_dir + '/node_modules/package')
            os.makedirs(temp_dir + '/node_modules/package/lib')
            package_json = open(temp_dir + '/node_modules/package/package.json', 'w')
            json.dump({'main': './lib/foo.js'}, package_json)
            open(temp_dir + '/node_modules/package/lib/foo.js', 'w').close()

            current_file = temp_dir + '/main.js'
            result = main.find_relative(current_file, 'package')
            expected = temp_dir + '/node_modules/package/lib/foo.js'
            self.assertEqual(expected, result)

        except Exception as err:
            self.fail(err)

        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
