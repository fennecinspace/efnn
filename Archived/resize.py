import os
import cv2
from efimg import Image
from progress.bar import Bar


INPUT_DIR = '/home/hammi/Desktop/images/converted/'

WIDTH, HEIGHT = 500, 500

OUTPUT_DIR = f'/home/hammi/Desktop/images/{WIDTH}x{HEIGHT}/'

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

samples = os.listdir(INPUT_DIR)
samples.sort()

bar = Bar('Processing', max=len(samples))
for sample in samples:
    bar.next()
    exposures = os.listdir( os.path.join(INPUT_DIR, sample) )
    exposures.sort()

    if not os.path.exists(os.path.join(OUTPUT_DIR, sample)):
        os.mkdir(os.path.join(OUTPUT_DIR, sample))

    for exposure in exposures:
        img = Image.read(os.path.join(INPUT_DIR, sample, exposure))
        try:
            img = Image.resize(img, WIDTH, HEIGHT)
            cv2.imwrite(os.path.join(OUTPUT_DIR, sample, exposure), img)
        except Exception as e:
            pass
            # print(exposure)
