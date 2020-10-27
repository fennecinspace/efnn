import os
from efimg import Exposures

# tf.compat.v1.enable_eager_execution()

MODEL_TO_USE = './model-256-04-0.93-0.00342.hdf5'

SAMPLES_DIR = './'
SAMPLE = 'sample'

# SAMPLES_DIR = "./dataset/jpg"


# SAMPLE = 'OtterPoint'
# EVS = ['-6', '-4', '-2']

# SAMPLE = 'Zentrum'
# EVS = ['-3', '+0', '+3']

# SAMPLE = 'BandonSunset(2)'
# EVS = ['-6', '-2', '+1']

# SAMPLE = 'HDRMark'
# EVS = ['-8', '-4', '+1']

# SAMPLE = 'WallDrug'
# EVS = ['-8', '-3', '+0']

# reading sample
x = Exposures(
        os.path.join(SAMPLES_DIR, SAMPLE), 
        # evs = [f'{SAMPLE}-EV{ev}' for ev in EVS],
        model = MODEL_TO_USE
    )

# using mertens
x.create_ef()

# using efnn
x.predict_ef()

# result is saved to sample folder