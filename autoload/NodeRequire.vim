let s:pythonFile = expand('<sfile>:p:h:h')

fu! NodeRequire#test()
  echo s:pythonFile
endfu
" execute 'pyfile ' . fnameescape(s:script)
