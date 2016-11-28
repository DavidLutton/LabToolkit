#!/bin/bash
set -x

bash clean.sh && latexmk -pdf RF\ Immunity\ Test\ System.tex && latexmk -c && bash clean.sh ! -name "*.pdf"
