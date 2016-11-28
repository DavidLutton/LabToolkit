find . -maxdepth 1 -type f ! -name "*.tex" ! -name "*.sh"  ! -name "*.py" "$@" -delete
