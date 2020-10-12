import os
import numpy as np
from progress.bar import Bar
from efimg import Exposures

def read_csv(path, delimiter = ','):
    f = open(path, 'r')
    content = f.read().split('\n')
    return [line.split(delimiter) for line in content]

lines = read_csv('/home/hammi/Projects/efnn/list.csv')

to_keep = []
for line in lines:
    if int(line[5]):
        to_keep += [line]

del lines
lines = to_keep


bar = Bar('Creating Numpy Data', max=len(lines))
i = 0
for line in lines:
    bar.next()
    x = Exposures(f'/home/hammi/Desktop/images/converted/{line[0]}', evs = [
                f'{line[0]}-EV{line[1]}', 
                f'{line[0]}-EV{line[2]}', 
                f'{line[0]}-EV{line[3]}', 
            ], colorspace="rgb", ef_file_name = f'{line[4]}.jpg'
        )
    
    # x.create_np_data()
    # x.save_np_data()
    x.load_np_data()

    if i == 0:
        data = x.np_data['data'][0::10]
        labels = x.np_data['labels'][0::10]
    else:
        data = np.concatenate((data, x.np_data['data'][0::10]), 0)
        labels = np.concatenate((labels, x.np_data['labels'][0::10]), 0)

    # print("\n", x.pixel(0,1000), data[100])
    del x
    i += 1
    # break

bar.finish()


np.save('./rgb_data.npy', data)
np.save('./rgb_labels.npy', labels)

    