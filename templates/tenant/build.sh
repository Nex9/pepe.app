#!/bin/bash
PWD=`pwd`;
PROJECT=`basename $PWD`;

if [ -f static/css/$PROJECT.styl ]
then
    stylus --include ../../static/lib/styls static/css/$PROJECT.styl;
    stylus --compress < static/css/$PROJECT.css > static/css/$PROJECT.min.css;

elif [ -f static/css/$PROJECT.css ]
then
    stylus -c < static/css/$PROJECT.css > static/css/$PROJECT.min.css;
fi

if [ -f static/js/$PROJECT.js ]
then
    uglifyjs2 static/js/$PROJECT.js > static/js/$PROJECT.min.js
fi