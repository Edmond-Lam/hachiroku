#!/bin/bash

echo "===" >> devlog.txt
usr="dMonteagudo"
dt=$(date '+%-m/%d/%y %l:%M %p');
echo "$dt"
echo "$usr $dt" >> devlog.txt
echo "" >> devlog.txt
for var in "$@"
do
    echo "- $var" >> devlog.txt
done
echo "===" >> devlog.txt
echo "" >> devlog.txt
