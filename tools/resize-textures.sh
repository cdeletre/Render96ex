#!/usr/bin/env sh

SOURCE="$1.fullsize"
DESTINATION="$1"

mv $1 ${SOURCE}
mkdir ${DESTINATION}
cd ${SOURCE}

find . -type d -exec mkdir -p -- ../${DESTINATION}/{} \;
find . -iname '*.c' -exec cp {} ../${DESTINATION}/{} \;
find . -iname '*.h' -exec cp {} ../${DESTINATION}/{} \;

find . -iname '*.png' -exec convert {} -define png:color-type=6 -resize 25% -filter lanczos "../${DESTINATION}/{}" \;
cd ..