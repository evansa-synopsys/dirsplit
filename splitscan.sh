#!/bin/bash
#
#

PROJECT=$1
SIZE=$2

rm -rf foobar
mkdir foobar

python dirsplit.py $PROJECT $SIZE foobar

rm -rf chunk-* 

for i in `ls foobar`
do
   echo processing $i
   mkdir $i
   cat foobar/$i | while read line
   do
      folder=$(dirname "${i}/${line}")
      test ! -d "$folder" && mkdir -p "$folder"
      cp -l "${line}" "${i}/${line}"
   done
done

for i in `ls foobar`
do 

bash scan.sh $PROJECT LATEST $i

done

