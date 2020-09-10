from django.shortcuts import render
from django.http import HttpResponse
from app.efimg import Exposures

import time

import os
from PIL import Image

# Create your views here.


def Home(req, *args, **kwargs):

    # # x = Exposures('media/HDRMark', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')
    # x = Exposures('media/AirBellowsGap', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')
    # # x = Exposures('media/LightHouse', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')
    # # x = Exposures('media/OSTROW', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')
    # # x = Exposures('media/SAMPLE001', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')

    # x.create_ef()

    # x.predict_ef()

    return render(req, template_name = 'index.html')


def Run(req, sample_name, *args, **kwargs):

    try:
        x = Exposures(f'media/{sample_name}', evs = ['under', 'normal', 'over'], model = 'media/model.hdf5')

        t_ef = x.create_ef()

        t_efnn = x.predict_ef()

        return render(req, template_name = 'results_page.html', context = {
            'SAMPLE_NAME' : sample_name,
            'EF_TIME' : round(t_ef * 1000),
            'EFNN_TIME' : round(t_efnn * 1000),
        })

    except Exception as e:
        print(e)

    # return render(req, template_name = 'index.html')

    return render(req, template_name = 'results_page.html')