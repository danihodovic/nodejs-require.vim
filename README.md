# nodejs-require.vim [![CircleCI](https://circleci.com/gh/danihodovic/nodejs-require.vim/tree/master.svg?style=svg)](https://circleci.com/gh/danihodovic/nodejs-require.vim/tree/master)

Find the file which was `require()` called in Node.js source files. Works for both local files and
packages in `node_modules/`.

# Usage
The plugin exposes one function which returns the full path of the required file. The cursor must
hover over a line which contains a require statement. Using regular expressions it extracts the
require calls contents and finds the required file.

Example:

    " Place your cursor over a line containing a `require()` statement
    :execute 'edit ' . require#find_in_current_line()

Using a mapping:

    autocmd FileType javascript nnoremap <buffer>gf :execute 'edit ' . require#find_in_current_line()<cr>

## API

    require#find_in_current_line()

Infers the path of the current buffer and the current line. Returns the path of found file.

    require#find(current_file, require_stmt)

Pass the current file path and the require statement to the function. Returns the path of the found
file. Example usage: `echom require#find(expand('%:p'), expand('<cword>'))`


# Installation
You need a VIM version that was compiled with Python 2.6 or later (+python).

## Using vim-plug
Add this to your .vimrc

    Plug 'danihodovic/nodejs-require.vim'

Run `:PlugInstall`

# Test coverage:

- [X] Require a local file with the require statement matching a file
- [X] Require a local file and fall back to index.js if the require path is a directory
- [X] Require a local file a directory above
- [X] Require a local file a directory below
- [X] Require a package file where the package.json `main` property points to a file
- [ ] Require a package file relative to the package directory

