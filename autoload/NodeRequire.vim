let s:pythonFile = expand('<sfile>:p:h:h')

fu! Load()
  echom 'zingo'
endfu

fu! NodeRequire#test()
  echom 'hello'
endfu
" execute 'pyfile ' . fnameescape(s:script)
