#!/usr/bin/env bas

# update github-page branch
pelican content -o output -s pelicanconf.py
ghp-import output
git push -u origin gh-pages
