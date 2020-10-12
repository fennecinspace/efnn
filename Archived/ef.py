import os
from progress.bar import Bar
from efimg import Exposures

def test1(sample):
    x = Exposures(f'/home/hammi/Desktop/images/converted/{sample}', evs = [
            # f'{sample}-EV-8', 
            # f'{sample}-EV-7', 
            f'{sample}-EV-6', 
            # f'{sample}-EV-5', 
            # f'{sample}-EV-4',
            f'{sample}-EV-3', 
            # f'{sample}-EV-2',
            # f'{sample}-EV-1',
            f'{sample}-EV+0',
            # f'{sample}-EV+1', 
            # f'{sample}-EV+2', 
            # f'{sample}-EV+3', 
        ], colorspace="rgb", ef_file_name = 'test1.jpg'
    )
    # x.show_exposures(True, 40, 4)
    # x.show_ef()
    print(x.pixel(0,0))


def test2(sample):
    x = Exposures(f'/home/hammi/Desktop/SAMPLE001', evs = ['SAMPLE001-EV-3', 'SAMPLE001-EV+0', 'SAMPLE001-EV+3'], colorspace="bgr")
    # x.show_exposures(True, 40, 4)
    x.show_ef()


def createEFLabels(samples_dir):
    samples = os.listdir(samples_dir)
    samples.sort()
    
    bar = Bar('Processing', max=len(samples))

    for i, sample in enumerate(samples):
        bar.next()
        Exposures(
            f'/home/hammi/Desktop/images/converted/{sample}', evs = [ 
                f'{sample}-EV-8', 
                # f'{sample}-EV-7', 
                # f'{sample}-EV-6', 
                f'{sample}-EV-5', 
                # f'{sample}-EV-4', 
                # f'{sample}-EV-3', 
                f'{sample}-EV-2', 
                # f'{sample}-EV-1', 
                # f'{sample}-EV+0', 
                # f'{sample}-EV+1', 
                # f'{sample}-EV+2', 
                # f'{sample}-EV+3',
            ], 
            colorspace="bgr", ef_file_name = 'ef5.jpg'
        )
    bar.finish()



if __name__ == '__main__':
    # test1('CemeteryTree(1)')
    test2(1)
    # createEFLabels('/home/hammi/Desktop/images/converted/')

# ef : -8 / -4 / +1
# ef1 : -8 -> +0
# ef2 : -6 / -2 / +1
# ef3 : -7 / -3 / +1
# ef4 : -8 -> +3
# ef5 : -8 / -5 / -2