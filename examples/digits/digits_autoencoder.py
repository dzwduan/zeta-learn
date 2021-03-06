# -*- coding: utf-8 -*-

import numpy as np
from sklearn import datasets

from ztlearn.utils import *
from ztlearn.dl.models import Sequential
from ztlearn.optimizers import register_opt
from ztlearn.dl.layers import BatchNormalization, Dense

img_rows   = 8
img_cols   = 8
img_dim    = 64  # img_rows * img_cols
latent_dim = 4
init_type  = 'he_normal'

def stack_encoder_layers(init):
    model = Sequential(init_method = init)
    model.add(Dense(256, activation = 'relu', input_shape = (img_dim,)))
    model.add(BatchNormalization())
    model.add(Dense(128, activation = 'relu'))
    model.add(BatchNormalization())
    model.add(Dense(latent_dim, activation = 'relu'))

    return model

def stack_decoder_layers(init):
    model = Sequential(init_method = init)
    model.add(Dense(128, activation = 'relu', input_shape = (latent_dim,)))
    model.add(BatchNormalization())
    model.add(Dense(256, activation = 'relu'))
    model.add(BatchNormalization())
    model.add(Dense(img_dim, activation = 'sigmoid'))

    return model

encoder = stack_encoder_layers(init = init_type)
decoder = stack_decoder_layers(init = init_type)

opt = register_opt(optimizer_name = 'adam', momentum = 0.01, learning_rate = 0.0001)

autoencoder = Sequential(init_method = init_type)
autoencoder.layers.extend(encoder.layers)
autoencoder.layers.extend(decoder.layers)
autoencoder.compile(loss = 'categorical_crossentropy', optimizer = opt)

autoencoder.summary('digits autoencoder')

data   = datasets.load_digits()
images = range_normalize(data.data.astype(np.float32), 0, 1)  # rescale to range [0, 1]
train_data, test_data, train_label, test_label = train_test_split(images,
                                                                          images,
                                                                          test_size = 0.2, random_seed = 15)
# plot samples of training data
plot_img_samples(train_data, None)

model_epochs = 500
fit_stats = autoencoder.fit(train_data,
                            train_label,
                            batch_size      = 64,
                            epochs          = model_epochs,
                            validation_data = (test_data, test_label),
                            shuffle_data    = True)

# generate non rescaled test labels for use in generated digits plot
_, _, _, test_label = train_test_split(data.data, data.target, test_size = 0.2, random_seed = 15)
predictions         = autoencoder.predict(test_data).reshape((-1, img_rows, img_cols))

model_name = autoencoder.model_name
plot_generated_img_samples(unhot(one_hot(test_label)),
                                                       predictions,
                                                       to_save    = False,
                                                       iteration  = model_epochs,
                                                       model_name = model_name)

plot_metric('loss',     model_epochs, fit_stats['train_loss'], fit_stats['valid_loss'], model_name = model_name)
plot_metric('accuracy', model_epochs, fit_stats['train_acc'],  fit_stats['valid_acc'],  model_name = model_name)
