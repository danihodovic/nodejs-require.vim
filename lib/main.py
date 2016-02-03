# This is a clusterfuck, but surprisingly works for JS
# TODO: Log when it can't find results
import vim
import os
import json
import re

REQUIRE_REGEX = r'require\(["\'](.*)["\']\)'

def findRelativeRequire(requirePath):
    filename = requirePath
    if not filename.endswith('.js'):
        filename = filename + '.js'

    # Node permits you to require('./foo') where foo is a directory that contains index.js
    # Node will always prioritize a file named file.js rather than file/index.js
    if not os.path.isfile(filename):
        filename = requirePath + '/index.js'

    currDir = os.path.dirname(vim.current.buffer.name)
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
            if not mainfile.endswith('.js'):
                mainfile = mainfile + '.js'
            return mainfile

currLine = vim.current.line
m = re.search(REQUIRE_REGEX, vim.current.line)
if m:
    stmt = m.groups()[0]
    root = None
    if stmt.startswith('.'):
        root = findRelativeRequire(stmt)
    else:
        root = findNodeModulesRequire(stmt)

    if root:
        vim.command('return "{}"'.format(root))
