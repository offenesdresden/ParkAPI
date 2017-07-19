#!/bin/bash


USER=$(cut -d"/" -f4 <<< $1)
REPO=$(cut -d"/" -f5 <<< $1)
MODULE=$(sed "s/\.git$//g;s/[-\+\.]/_/g;s/\(.*\)/\L\1/g" <<< $REPO)

git submodule add https://github.com/$USER/$REPO $(pwd)/park_api/modules/$MODULE
