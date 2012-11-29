#!/bin/bash
PWD=`pwd`;
PROJECT=`basename $PWD`;

if [ -f static/css/$PROJECT.styl ]
then
    stylus --watch --include ../../static/lib/styls static/css/$PROJECT.styl;
fi