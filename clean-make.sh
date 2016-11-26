find . -maxdepth 1 -type f ! -name "*.tex" ! -name "*.sh"  -delete && latexmk -pdf   RF\ Immunity\ Test\ System.tex  
