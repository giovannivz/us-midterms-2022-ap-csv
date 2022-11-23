#!/bin/sh

repopath=$1
dir=$2
race=$(basename $dir)

mkdir -p CSV/$race/
python3 json2csv.py $repopath $dir/summary.json CSV/$race/
python3 json2csv.py $repopath $dir/detail.json CSV/$race/
python3 json2csv.py $repopath $dir/metadata.json CSV/$race/
