#!/bin/sh

repopath=$1

for dir in $repopath/AP/2022*; do
  race=$(basename $dir)
  echo $dir
  ./convert-csv.sh $repopath AP/$race
done
