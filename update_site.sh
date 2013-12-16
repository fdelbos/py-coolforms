#!/bin/sh

docco coolforms.py && mv docs/coolforms.html docs/index.html
git checkout gh-pages
mv docs/docco.css .
mv docs/index.html .
mv docs/public .
git add docco.css index.html public
rm -fr docs
git commit -m "updating site"
git push origin gh-pages 
git checkout master

