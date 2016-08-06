let s:repo_root = expand('<sfile>:p:h:h')

if !has('python') 
  echo 'Python required'
  finish
endif

let repo_root = expand("<sfile>:p:h:h")
let main_py_file = repo_root . '/lib/main.py'
execute 'pyfile ' . main_py_file

" Find the path of the require statement on the same line as the cursor. Returns the text value
fu! require#find_in_current_line()
  let current_line = getline('.')
  if current_line !~# 'require\(.*\)'
    echom 'Current line does not contain a require statement'
    return
  endif
  let current_buffer_path = expand('%:p')
  let path = ''
python << EOF
path = find_in_require_stmt(vim.eval('current_buffer_path'), vim.eval('current_line'))
vim.command('let path = "{}"'.format(path))
EOF
if path == 'None'
  echom 'No path found...Report this'
else
  return path
endif
endfu

" Declare a function that can autoload this file 
fu! require#Load() 
endfu

