let s:pythonFile = expand('<sfile>:p:h:h') . '/lib/main.py'

fu! NodeRequire#init()
  exe 'pyfile ' . s:pythonFile
endfu

fu! NodeRequire#find()
let file = ''
python << EOF
vim.command('let file = "{}"'.format(findRequire()))
EOF

  echo file
endfu
