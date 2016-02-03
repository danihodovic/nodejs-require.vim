let s:pythonFile = expand('<sfile>:p:h')

fu! VimNodeRequire#test()
  echo s:pythonFile
endfu
" execute 'pyfile ' . fnameescape(s:script)
