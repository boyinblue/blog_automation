#!/bin/bash

git pull
pushd ../../boyinblue.github.io
git pull
popd

./accumulate.py
./process.py

pushd ../../boyinblue.github.io/_build
./check_md_files.py
popd

pushd ../../boyinblue.github.io
git add .
git commit -m "[Automatic Commit] Event Info Generate"
git push
popd
