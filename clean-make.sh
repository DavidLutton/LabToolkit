
#!/bin/bash
set -x

#find . -maxdepth 1 -type f ! -name "*.tex" ! -name "*.sh"  ! -name "*.py"  -delete && latexmk -pdf -pvc RF\ Immunity\ Test\ System.tex
find . -maxdepth 1 -type f ! -name "*.tex" ! -name "*.sh"  ! -name "*.py"  -delete && latexmk -pdf RF\ Immunity\ Test\ System.tex && latexmk -c
