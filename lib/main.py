try:
    import vim
except ImportError:
    pass

import os
import json

# Finds statement in cword
# Finds statement in require

# Find by relative to current path. Full pathname
# Relative and direct
# Unit test by passing the

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



def find_relative_require(requirePath):
    filename = requirePath
    if not filename.endswith('.js'):
        filename = filename + '.js'

    currDir = os.path.dirname(vim.current.buffer.name)
    realpath = os.path.realpath(os.path.join(currDir, filename))

    if os.path.isfile(realpath):
        return realpath
    else:
        filename = requirePath + '/index.js'

        relativePath = os.path.join(currDir, filename)
        realpath = os.path.realpath(relativePath)
        if os.path.isfile(realpath):
            return realpath

def findNodeModulesRequire(filename):
    if filename.endswith('.js'):
        filename = filename[:-3]

    currFile = vim.eval('expand("%:p")')
    currDir = os.path.dirname(currFile)

    # Walk until the package is found is found or we are at fs root. This accounts for nested
    # dependencies in the packages and shrinkwrapped projects.  If we are deep in a dependency
    # tree and look for a dependency that is common with the root projects dependency, npm may
    # have moved this dependency up in the tree.  So we need to check for this package in
    # every node_modules directory we encounter.
    # E.g we are looking for dependency c in b
    # $PROJ_ROOT/node_modules/a/node_modules/b
    # $PROJ_ROOT/node_modules/c

    packageDir = ''
    while currDir != '/':
        if 'node_modules' in os.listdir(currDir):
            packageDir = os.path.realpath(currDir + '/node_modules/' + filename)
            if os.path.isdir(packageDir):
                break
        currDir = os.path.dirname(currDir)

    packageJson = packageDir + '/package.json'
    if os.path.isfile(packageJson):
        with open(packageJson) as f:
            asJson = json.load(f)
            mainfile = packageDir + '/' + asJson['main']
            if mainfile.endswith('.js') == False:
                mainfile = mainfile + '.js'
            return mainfile


#  currLine = vim.current.line
#  m = re.search(REQUIRE_REGEX, vim.current.line)
#  if m:
  #  stmt = m.groups()[0]
  #  root = None
  #  if stmt.startswith('.'):
    #  root = findRelativeRequire(stmt)
  #  else:
    #  root = findNodeModulesRequire(stmt)

  #  if root:
    #  vim.command('return "{}"'.format(root))
