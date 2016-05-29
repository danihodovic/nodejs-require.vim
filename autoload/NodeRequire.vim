let s:repo_root = expand('<sfile>:p:h:h')

if !has('python') 
  echo 'Python required'
  finish
endif


" execute 

fu! NodeRequire#Load()
  echom 'NodeRequire#load()'
  command! FindDani -buffer :pyfile main.py
endfu

" execute 'pyfile ' . fnameescape(s:script)
