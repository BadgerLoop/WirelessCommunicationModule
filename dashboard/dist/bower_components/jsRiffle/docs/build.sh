#!/bin/bash
if [ $# -lt 1 ]
then
    echo "Usage:"
    echo -e " call with version of docs to build i.e. 0.X.X"
    exit -1
fi
cat contents.md | sed "s/###version###/$1/" > jsRiffle.md && \
cat changelog.md | sed -n /START__$1/,/END__$1/p | sed "s/START__$1//" | sed "s/END__$1//" >> jsRiffle.md && \
jsdoc2md ../index.js ../src/appliances/* >> jsRiffle.md
