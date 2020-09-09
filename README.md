# EFNN

This is the code repository that includes the main scripts and notebooks for my Master 2 Graduation Project.


## efnndemo

efnndemo is a very simple django application hosted on azure cloud. its goal is to host the Memoire and provide a way for my professors to test EFNN without the need to install or run anything.

the application is deployed on https://efnn.ml

## models :

The models folder doesn't contain all the models that i created and trained during these past months. It contains the models that work best, as well as models that may not work but were used in the Memoire in order to explain a concept or a piece of code.

The best model is :

```
./models/50TH/256-04-0.93-0.00342.hdf5
```


## Notebooks & Ressources:

This repository contains many Jupyter notebooks. The notebooks contain the different implementations of all the concepts and steps explained in the Memoire.

Other present ressources (python, json, csv ..etc) are also all related to concepts, tables, figures or code present in the Memoire.

## Before you run anything :

This repository and these notebooks are supposed to run on Google Colab. don't use your home machine. https://colab.research.google.com/

On Colab :

1 - Install Imagemagik 7

```
apt install openexr build-essential
wget https://www.imagemagick.org/download/ImageMagick.tar.gz -O "ImageMagick.tar.gz"
mkdir -p ImageMagick
rm -rf ImageMagick/*
tar -xf ImageMagick.tar.gz -C ImageMagick --strip-components=1 
cd ImageMagick
ls
./configure
make
make install
ldconfig /user/local/lib
magick -version
```

2 - HDRPs Dataset Acquisition

```
mkdir -p ./dataset/exr
cd ./dataset/exr 
wget --show-progress --timeout 10 --tries 0 --continue -i ../../samples_links.txt
cd ../../
```

3 - Exposures Extraction :

```
chmod +x extract_evs.sh
chmod +x extract_allimages_evs.sh
./extract_allimages_evs.sh
```

4 - Start with the fusion notebook and go from there. EXPLORE !!!!


Reading the memoire will get you up to speed on the code written in the different notebooks.