let s:repo_root = expand('<sfile>:p:h:h')

if !has('python') 
  echo 'Python required'
  finish
endif

fu! NodeRequire#Load()
  " command! FindDani -buffer :pyfile main.py
endfu

