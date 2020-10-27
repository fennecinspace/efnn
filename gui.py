import os
import cv2
import tensorflow as tf

from efimg import Exposures

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

tf.compat.v1.enable_eager_execution()

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

MODEL_TO_USE = os.path.join(BASE_PATH, 'model-256-04-0.93-0.00342.hdf5')


class Root(Tk):
    def open_file(self, t): 
        try:
            filename = filedialog.askopenfilename(title = "Select A File")
            if not filename:
                return
            self.exposures[t] = cv2.imread(filename)
            self.exposures_resized[t] = cv2.resize( self.exposures[t], (self.CANVAS_SIZE_X, self.CANVAS_SIZE_Y) )
            self.to_display[t] = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.exposures_resized[t], cv2.COLOR_BGR2RGB)))
            self.canvas[t].create_image(0, 0, anchor = NW, image = self.to_display[t])
        except Exception as e:
            messagebox.showerror("Error", str(e))
            

    def fusion_popup(self):
        try:
            res_window = Toplevel()
            self.canvas['mertens'] = Canvas(res_window, width = self.BIG_CANVAS_SIZE_X, height = self.BIG_CANVAS_SIZE_Y)  
            self.canvas['mertens'].grid(row = 0, column = 0, padx = 5, pady = 20)
            self.canvas['mertens'].config(background="#fff")
            self.canvas['mertens'].create_text(self.BIG_CANVAS_SIZE_X / 2, self.BIG_CANVAS_SIZE_Y / 2, fill="#000", font="Times 20 bold", text="COULD NOT CALCULATE METENS")

            self.canvas['efnn'] = Canvas(res_window, width = self.BIG_CANVAS_SIZE_X, height = self.BIG_CANVAS_SIZE_Y)  
            self.canvas['efnn'].grid(row = 0, column = 1, padx = (5,10,), pady = 20)
            self.canvas['efnn'].config(background="#fff")
            self.canvas['efnn'].create_text(self.BIG_CANVAS_SIZE_X / 2, self.BIG_CANVAS_SIZE_Y / 2, fill="#000", font="Times 20 bold", text="COULD NOT CALCULATE EFNN")

            self.mertens_time = Label(res_window, text="MERTENS : ? seconds")
            self.mertens_time.grid(row=1, column=0, padx = 5, pady = 10)

            self.efnn_time = Label(res_window, text="EFNN : ? seconds")
            self.efnn_time.grid(row=1, column=1, padx = 5, pady = 10)
            
            self.run_fusion()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_fusion(self):
        try: 
            if any([self.exposures[key] is None for key in self.exposures.keys()]):
                messagebox.showerror("Error", "You must load all three exposures")
                return

            if not ( self.exposures['under'].shape == self.exposures['normal'].shape and self.exposures['over'].shape == self.exposures['normal'].shape ):
                messagebox.showerror("Error", "Exposures must have the same resolutions/shape")
                return

            x = Exposures(BASE_PATH, exposures_files = self.exposures, model = MODEL_TO_USE)
            
            try:
                ef_t = x.create_ef()

                self.ef_resized = cv2.resize(x.ef, (self.BIG_CANVAS_SIZE_X, self.BIG_CANVAS_SIZE_Y) )
                self.ef_to_display = ImageTk.PhotoImage( Image.fromarray(cv2.cvtColor(self.ef_resized, cv2.COLOR_BGR2RGB)) )
                self.canvas['mertens'].create_image(0, 0, anchor = NW, image = self.ef_to_display)
                self.mertens_time['text'] = f"MERTENS : {ef_t:.2f} seconds"
            except Exception as e:
                messagebox.showerror("Error", str(e))

            try:
                efnn_t = x.predict_ef()

                self.efnn_resized = cv2.resize(x.ef_prediction, (self.BIG_CANVAS_SIZE_X, self.BIG_CANVAS_SIZE_Y) )
                self.efnn_to_display = ImageTk.PhotoImage( Image.fromarray(cv2.cvtColor(self.efnn_resized, cv2.COLOR_BGR2RGB)) )
                self.canvas['efnn'].create_image(0, 0, anchor = NW, image = self.efnn_to_display)
                self.efnn_time['text'] = f"EFNN : {efnn_t:.2f} seconds"
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def __init__(self):
        super(Root, self).__init__()
        
        self.exposures = {
            'under': None,
            'normal': None,
            'over': None,
        }

        self.exposures_resized = {
            'under': None,
            'normal': None,
            'over': None,
        }

        self.to_display = {
            'under': None,
            'normal': None,
            'over': None,
        }


        self.canvas = {}

        self.title("EFNN vs Mertens")

        self.CANVAS_SIZE_X = 300
        self.CANVAS_SIZE_Y = 200
        self.BIG_CANVAS_SIZE_X = 600
        self.BIG_CANVAS_SIZE_Y = 400

        self.w = Label(self, text="Choose 3 different exposures. The images must be jpg or png and of the same resolution.\nBecause Metens is quite slow, it is better to use images under 1000x1000")
        self.w.grid(row=0, column=0, columnspan=3, padx = 50, pady = 10)


        self.btn1 = Button(self, text ='Select Under exposed', command = lambda : self.open_file('under'))
        self.btn1.grid(row=1, column=0, padx=0, pady= (10,10,))

        self.btn2 = Button(self, text ='Select Normal exposed', command = lambda : self.open_file('normal'))
        self.btn2.grid(row=1, column=1, padx=0, pady= (0,10,))

        self.btn3 = Button(self, text ='Select Over exposed', command = lambda : self.open_file('over'))
        self.btn3.grid(row=1, column=2, padx=0, pady= (0,10,))

        self.canvas['under'] = Canvas(self, width = self.CANVAS_SIZE_X, height = self.CANVAS_SIZE_Y)  
        self.canvas['under'].grid(row = 2, column = 0, padx = (10,5,), pady = 20)
        self.canvas['under'].config(background="#fff")
        self.canvas['under'].create_text(self.CANVAS_SIZE_X / 2, self.CANVAS_SIZE_Y / 2, fill="#000", font="Times 20 bold", text="UNDER")

        self.canvas['normal'] = Canvas(self, width = self.CANVAS_SIZE_X, height = self.CANVAS_SIZE_Y)  
        self.canvas['normal'].grid(row = 2, column = 1, padx = 5, pady = 20)
        self.canvas['normal'].config(background="#fff")
        self.canvas['normal'].create_text(self.CANVAS_SIZE_X / 2, self.CANVAS_SIZE_Y / 2, fill="#000", font="Times 20 bold", text="NORMAL")

        self.canvas['over'] = Canvas(self, width = self.CANVAS_SIZE_X, height = self.CANVAS_SIZE_Y)  
        self.canvas['over'].grid(row = 2, column = 2, padx = (5,10,), pady = 20)
        self.canvas['over'].config(background="#fff")
        self.canvas['over'].create_text(self.CANVAS_SIZE_X / 2, self.CANVAS_SIZE_Y / 2, fill="#000", font="Times 20 bold", text="OVER")

        self.runBtn = Button(self, text ='Run', command = self.fusion_popup)
        self.runBtn.grid(row = 3, column = 0, columnspan = 3, padx = 0, pady = 10)

app = Root()
app.mainloop()

# # tf.compat.v1.enable_eager_execution()

# MODEL_TO_USE = './model-256-04-0.93-0.00342.hdf5'

# SAMPLES_DIR = './'
# SAMPLE = 'sample'

# # SAMPLES_DIR = "./dataset/jpg"


# # SAMPLE = 'OtterPoint'
# # EVS = ['-6', '-4', '-2']

# # SAMPLE = 'Zentrum'
# # EVS = ['-3', '+0', '+3']

# # SAMPLE = 'BandonSunset(2)'
# # EVS = ['-6', '-2', '+1']

# # SAMPLE = 'HDRMark'
# # EVS = ['-8', '-4', '+1']

# # SAMPLE = 'WallDrug'
# # EVS = ['-8', '-3', '+0']

# x = Exposures(
#         os.path.join(SAMPLES_DIR, SAMPLE), 
#         # evs = [f'{SAMPLE}-EV{ev}' for ev in EVS],
#         model = MODEL_TO_USE
#     )

# x.create_ef()

# x.predict_ef()
