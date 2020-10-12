#!/bin/bash

file=$1
extraction_dir=$2

base="${file%.*}"
filename=$(basename $base)

echo "Processing ${filename}"

mkdir -p "${extraction_dir}/${filename}"

magick "$file" \
	\( +clone -evaluate multiply 0.00390625 -write "${extraction_dir}/${filename}/${filename}-EV-8.jpg" +delete \)  \
	\( +clone -evaluate multiply 0.0078125 -write "${extraction_dir}/${filename}/${filename}-EV-7.jpg" +delete \)  \
	\( +clone -evaluate multiply 0.015625 -write "${extraction_dir}/${filename}/${filename}-EV-6.jpg" +delete \)  \
	\( +clone -evaluate multiply 0.03125 -write "${extraction_dir}/${filename}/${filename}-EV-5.jpg" +delete \)  \
	\( +clone -evaluate multiply 0.0625 -write "${extraction_dir}/${filename}/${filename}-EV-4.jpg" +delete \)  \
    \( +clone -evaluate multiply 0.125 -write "${extraction_dir}/${filename}/${filename}-EV-3.jpg" +delete \)  \
    \( +clone -evaluate multiply 0.25  -write "${extraction_dir}/${filename}/${filename}-EV-2.jpg" +delete \)  \
    \( +clone -evaluate multiply 0.5   -write "${extraction_dir}/${filename}/${filename}-EV-1.jpg" +delete \)  \
    \( +clone -evaluate multiply 1     -write "${extraction_dir}/${filename}/${filename}-EV+0.jpg" +delete \)  \
    \( +clone -evaluate multiply 2     -write "${extraction_dir}/${filename}/${filename}-EV+1.jpg" +delete \)  \
    \( +clone -evaluate multiply 4     -write "${extraction_dir}/${filename}/${filename}-EV+2.jpg" +delete \)  \
              -evaluate multiply 8     "${extraction_dir}/${filename}/${filename}-EV+3.jpg"