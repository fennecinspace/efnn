import os
import numpy as np
import tensorflow as tf

# create models folder
if not os.path.exists('models'):
    os.makedirs('models')

# reading dataset
data = np.load('rgb_data.npy')
labels = np.load('rgb_labels.npy')

# randomization
idx = np.random.permutation(len(data))
data = data[idx]
labels = labels[idx]

# normalization
data = data / 255
labels = labels / 255

# model definition
model = tf.keras.Sequential()

model.add(tf.keras.layers.Dense(5, input_shape = (9,), activation='relu'))
model.add(tf.keras.layers.Dense(3, activation = 'linear'))
model.compile(loss='mean_squared_error', optimizer= tf.keras.optimizers.Adam(lr=0.0001), metrics = ['accuracy'])

# save each epoch result as a seperate model
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath="models/" + "{epoch:02d}-{accuracy:.2f}-{loss:.5f}.hdf5", monitor='loss', verbose=1, save_best_only=False, mode='auto', save_freq = 'epoch')

# initiate learning
model.fit(data, labels, epochs = 20, batch_size = 256, callbacks=[checkpoint])