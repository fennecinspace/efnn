import os

RES = [
    './npy-new/results/50TH',
    './npy-new/results/3RD',
]

DATA_TO_HANDLE = RES[1]

samples = os.listdir(DATA_TO_HANDLE)

if '.ipynb_checkpoints' in samples:
    del samples[samples.index('.ipynb_checkpoints')]

for sample in samples:
    
    models_results = os.path.join( DATA_TO_HANDLE, sample )
    
    for example in os.listdir(models_results):

        if os.path.isfile(os.path.join( models_results, example)):
            if not os.path.exists( os.path.join( models_results, example.split('-')[1]) ):
                os.mkdir( os.path.join( models_results, example.split('-')[1]) )

            os.rename( 
                os.path.join( models_results, example ), 
                os.path.join( models_results, example.split('-')[1], example ) 
            )

############################################################################################
### 2 ND PART - LEARNING RATE 

for sample in samples:
    
    batches = os.path.join( DATA_TO_HANDLE, sample )
    
    for batch in os.listdir(batches):
        
        for example in os.listdir(os.path.join(batches, batch)):

            if os.path.isfile(os.path.join(batches, batch, example)):
            
                if example.split('-').__len__() == 6:
                    
                    learning_rate = example.split('-')[-1].replace('.hdf5.jpg', '')

                    if not os.path.exists( os.path.join( batches, batch,  learning_rate) ):
                        os.mkdir( os.path.join( batches, batch,  learning_rate) )

                    os.rename( 
                        os.path.join( batches, batch, example ), 
                        os.path.join( batches, batch,  learning_rate, example ) 
                    )