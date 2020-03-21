import os
import cv2
import matplotlib.pyplot as plt

class Log():
    @classmethod
    def log(cls, level, message):
        print(f'[{level}]: {message}')


    @classmethod
    def info(cls, message):
        cls.log('INFO', message)


    @classmethod
    def error(cls, message):
        cls.log('ERROR', message)



class Image():
    @classmethod
    def BRG2RGB(cls, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    @classmethod
    def resize(cls, img, width, height):
        return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)


    @classmethod
    def read(cls, path, colorspace = 'bgr'):
        if colorspace == 'rgb':
            return cls.BRG2RGB(cv2.imread(path, cv2.IMREAD_COLOR))

        elif colorspace == 'gray':
            return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        elif colorspace == 'bgr':
            return cv2.imread(path, cv2.IMREAD_COLOR)
        
        else:
            return cv2.imread(path)



class Exposures:
    def __init__(self, path, ext = 'jpg', colorspace = 'bgr', evs = None, ef_file_name = 'ef.jpg'):
        if os.path.exists(path):
            self.colorspace = colorspace
            self.dir = path
            self.evs = evs or ['over', 'normal', 'under']
            self.exposures = {}
            self.ef = None
            self.ef_file_name = ef_file_name

            for ev in self.evs:
                self.exposures.update({
                    ev: f'{path}/{ev}.{ext}',
                })

            for ev, path in self.exposures.items():
                if os.path.exists(path):
                    self.exposures[ev] = Image.read(path, colorspace)
                else:
                    raise Exception(f'Could not find {ev} exposure at {path}')


            if os.path.exists(os.path.join(self.dir, self.ef_file_name)):
                self.ef = Image.read(os.path.join(self.dir, self.ef_file_name), self.colorspace)
            
        else:
            raise Exception(f"Invalid Directory {path}")


    def pixel(self, i, j):        
        if self.ef is None:
            self.create_ef()

        pixel_set = []
        for ev, exposure in self.exposures.items(): 
            pixel_set += list(exposure[i][j])

        return [ pixel_set, list(self.ef[i][j]) ]


    def create_ef(self, align = False):
        Log.info(f'{self.dir} Creating Fusion')
        exposures = [*self.exposures.values()]
        if align:
            alignMTB = cv2.createAlignMTB()
            alignMTB.process(exposures, exposures)
        mergeMertens = cv2.createMergeMertens()
        exposureFusion = mergeMertens.process(exposures)
        cv2.imwrite( os.path.join(self.dir, self.ef_file_name), exposureFusion * 255 )
        self.ef = Image.read(os.path.join(self.dir, self.ef_file_name), self.colorspace)


    def show_exposures(self, suplot_adjust = True, *figsize, **kwargs):
        fig = plt.figure(figsize=figsize)
        nb_exposures = self.exposures.__len__()
        cols = kwargs['cols'] if 'cols' in kwargs else nb_exposures
        rows = kwargs['rows'] if 'cols' in kwargs else 1
        
        for i in range(0, nb_exposures):
            fig.add_subplot(rows, cols, i + 1)
            if self.colorspace == 'bgr':
                plt.imshow(Image.BRG2RGB(self.exposures[self.evs[i]]))
            else:
                plt.imshow(self.exposures[self.evs[i]])

        # plt.subplot_tool
        if suplot_adjust:
            plt.subplots_adjust(left=0.05, right=0.99, top=1, bottom=0, wspace=0.17)

        plt.show()


    def show_ef(self):
        if self.ef is None:
            self.create_ef()

        if self.colorspace == 'bgr':
            plt.imshow(Image.BRG2RGB(self.ef))
        else:
            plt.imshow(self.ef)
        
        plt.show()
