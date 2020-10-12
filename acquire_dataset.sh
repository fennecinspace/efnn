#!/bin/bash

mkdir -p ./dataset/exr
cd ./dataset/

wget -c -r -np -k -L -A .exr -p http://markfairchild.org/HDRPS/HDRthumbs.html

mv ./markfairchild.org/HDRPS/EXRs/* ./exr

rm -rf ./markfairchild.org
