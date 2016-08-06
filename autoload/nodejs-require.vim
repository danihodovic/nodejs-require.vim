let s:repo_root = expand('<sfile>:p:h:h')

if !has('python') 
  echo 'Python required'
  finish
endif

let repo_root = expand("<sfile>:p:h:h")
let main_py_file = repo_root . '/lib/main.py'
execute 'pyfile ' . main_py_file

" Line under cursor must contain a require statement
fu! Find_in_current_line()
  let current_line = getline('.')
  let current_buffer_path = expand('%:p')

python << EOF
path = find_in_require_stmt(vim.eval('current_buffer_path'), vim.eval('current_line'))
vim.command('return "{}"'.format(path))
EOF
endfu

fu! NodeRequire#Load()
  command! -buffer FindDani execute 'edit ' . Find_in_current_line()
endfu

