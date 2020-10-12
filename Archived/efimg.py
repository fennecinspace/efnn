import os
import time
import cv2
import numpy as np
import tensorflow as tf
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
    def __init__(self, path, ext = 'jpg', colorspace = 'bgr', evs = None, ef_file_name = 'ef.jpg', prediction_file_name = 'ef_prediction.jpg', model = None):
        if os.path.exists(path):
            self.colorspace = colorspace
            self.dir = path
            self.sample_name = os.path.basename(self.dir)
            self.evs = evs or ['over', 'normal', 'under']
            self.exposures = {}
            self.ef = None
            self.ef_prediction = None 
            self.np_data = {
                'data' : None,
                'labels': None,
            }
            self.ef_file_name = ef_file_name
            self.prediction_file_name = prediction_file_name
            self.model = model

            for ev in self.evs:
                self.exposures.update({
                    ev: f'{path}/{ev}.{ext}',
                })

            for ev, path in self.exposures.items():
                if os.path.exists(path):
                    self.exposures[ev] = Image.read(path, colorspace)
                else:
                    raise Exception(f'Could not find {ev} exposure at {path}')

            self.size = self.exposures[evs[0]].shape


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

        t1 = time.time()

        exposures = [*self.exposures.values()]
        if align:
            alignMTB = cv2.createAlignMTB()
            alignMTB.process(exposures, exposures)
        mergeMertens = cv2.createMergeMertens()
        exposureFusion = mergeMertens.process(exposures)

        exposureFusion = exposureFusion * 255

        t2 = time.time()

        cv2.imwrite( os.path.join(self.dir, self.ef_file_name), exposureFusion )
        self.ef = Image.read(os.path.join(self.dir, self.ef_file_name), self.colorspace)

        return t2 - t1

    
    def predict_ef(self):
        Log.info(f'{self.dir} Creating Fusion')
        model = tf.keras.models.load_model(self.model)

        t1 = time.time()

        self.create_np_data()

        fusion = (model.predict_on_batch(self.np_data['data'] / 255) * 255).reshape(self.exposures[self.evs[0]].shape)

        t2 = time.time()

        cv2.imwrite( os.path.join(self.dir, self.prediction_file_name), fusion)
        self.ef_prediction = Image.read(os.path.join(self.dir, self.prediction_file_name), self.colorspace)

        return t2 - t1


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


    def create_np_data(self, concate_dims = True):
        if self.np_data['data'] is None:
            # stack 3 exposures
            image = np.stack(list(self.exposures.values()), axis = -2)
            if concate_dims:
                # merge inner rgb arrays (3rd (,:,:2) dim)
                image = np.concatenate(  tuple(image[:,:,i] for i in range(len(self.exposures))) , 2)
                image = image.reshape(len(image) * len(image[0]), len(image[0][0]))
            
            self.np_data['data'] = image

        if self.np_data['labels'] is None:
            if concate_dims:
                self.np_data['labels'] = self.ef.reshape(len(self.ef) * len(self.ef[0]), len(self.ef[0][0]))
            else:
                self.np_data['labels'] = self.ef

        # x = len(self.ef)
        # y = len(self.ef[0])
        # print( 
        #     '',
        #     self.pixel(3,1),
        #     '\n',
        #     [
        #         list(self.np_data['data'][y * 3 + 1]), 
        #         list(self.np_data['labels'][y * 3 + 1])
        #     ] 
        # )
        # assert list(self.np_data['data'][y]) == self.pixel(1,0)[0]


    def save_np_data(self, exposures_name = 'data', ef_name = 'labels'):
        if self.np_data['data'] is None or self.np_data['labels'] is None:
            self.create_np_data()

        e_save =  os.path.join(self.dir, f"{self.sample_name}_{exposures_name}.npy")
        ef_save = os.path.join(self.dir, f"{self.sample_name}_{ef_name}.npy")

        np.save( e_save, self.np_data['data'] )
        np.save( ef_save, self.np_data['labels'] )


    def load_np_data(self, exposures_name = 'data', ef_name = 'labels'):
        if self.np_data['data'] is None or self.np_data['labels'] is None:
            self.create_np_data()

        e_save =  os.path.join(self.dir, f"{self.sample_name}_{exposures_name}.npy")
        ef_save = os.path.join(self.dir, f"{self.sample_name}_{ef_name}.npy")

        self.np_data['data'] = np.load( e_save )
        self.np_data['labels'] = np.load( ef_save )

