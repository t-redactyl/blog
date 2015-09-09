#!/bin/bash
cp -r output/** ../blog
cd ../blog
git add .
git commit
git push origin master
