import os
import json
import re

# Finds statement in cword
# Finds statement in require

REQUIRE_REGEX = r'require\(["\'](.*)["\']\)'

def find_relative(current_buffer_path, required_file):
    # Get the file without the extension
    required_file = os.path.splitext(required_file)[0]

    current_folder = os.path.dirname(current_buffer_path)
    relative_path = os.path.join(current_folder, required_file)
    # The require statement can contain ../../foo so we have to normalize it
    real_path = os.path.normpath(relative_path)

    # Files take precendence over directory/index.js
    if os.path.isfile(real_path + '.js'):
        return real_path + '.js'
    else:
        index_path = real_path + '/index.js'
        if os.path.isfile(index_path):
            return index_path

def is_root_directory(path):
    return os.path.dirname(path) == path

def find_package_require(current_buffer_path, required_file):
    package_dir = ''
    current_path = os.path.dirname(current_buffer_path)
    # Walk until the package is found is found or we are at fs root. This accounts for nested
    # dependencies in the packages and shrinkwrapped projects.  If we are deep in a dependency
    # tree and look for a dependency that is common with the root projects dependency, npm may
    # have moved this dependency up in the tree.  So we need to check for this package in
    # every node_modules directory we encounter.
    # E.g we are looking for dependency c in b
    # $PROJ_ROOT/node_modules/a/node_modules/b
    # $PROJ_ROOT/node_modules/c
    while not is_root_directory(current_path):
        if 'node_modules' in os.listdir(current_path):
            package_dir_path = os.path.join(current_path, 'node_modules', required_file)
            package_dir = os.path.realpath(package_dir_path)
            if os.path.isdir(package_dir):
                break
        current_path = os.path.dirname(current_path)

    if package_dir != '':
        package_json = os.path.join(package_dir, 'package.json')
        if os.path.isfile(package_json):
            with open(package_json) as package_json_file:
                as_json = json.load(package_json_file)
                main_file = os.path.join(package_dir, as_json['main'])
                return os.path.realpath(main_file)

def find_in_require_stmt(current_buffer_path, line):
    print current_buffer_path
    print line
    path = None
    m = re.search(REQUIRE_REGEX, line)
    if m:
        stmt = m.groups()[0]
        if stmt.startswith('.'):
            path = find_relative(current_buffer_path, stmt)
        else:
            path = find_package_require(current_buffer_path, stmt)
        return path

