import os
import numpy as np
from efimg import Exposures

def read_csv(path, delimiter = ','):
    f = open(path, 'r')
    content = f.read().split('\n')
    return [line.split(delimiter) for line in content]

lines = read_csv('./base_data.csv')

SAMPLE_DIR = './dataset/jpg'

for i, line in enumerate(lines):
    if i == 3:
        break
    print('Processing', line)
    if not int(line[5]): 
        # don't use this sample
        continue

    x = Exposures(
        os.path.join(SAMPLE_DIR, line[0]), evs = [
            f'{line[0]}-EV{line[1]}', 
            f'{line[0]}-EV{line[2]}',
            f'{line[0]}-EV{line[3]}', 
        ], colorspace="bgr", ef_file_name = f'{line[4]}.jpg'
    )

    x.create_ef()
    
    x.create_np_data()
    # x.save_np_data()

    # take every 50TH pixel
    EVERY_X_PIXEL = 50
    if i == 0:
        data = x.np_data['data'][::EVERY_X_PIXEL]
        labels = x.np_data['labels'][::EVERY_X_PIXEL]
    else:
        data = np.concatenate((data, x.np_data['data'][::EVERY_X_PIXEL]), 0)
        labels = np.concatenate((labels, x.np_data['labels'][::EVERY_X_PIXEL]), 0)

np.save('./rgb_data.npy', data)
np.save('./rgb_labels.npy', labels)

print(data[0], labels[0])
print(len(data), len(labels))