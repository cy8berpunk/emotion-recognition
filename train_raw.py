import keras
from keras.layers import *
from keras.models import Model
from keras.regularizers import l2
from keras.optimizers import SGD
from cnn_model.models import *
from utils.data import *

def main():
    epochs = 60
    batch_size = 15
    val_training_factor = 0.7
    learning_rate = 0.0001
    files='F:/emotions_detection/raw/**'

    model = VGG_16((256, 256, 3), 9)
    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])

    print('training model on raw unlabeld data \r')

    tbCallBack = keras.callbacks.TensorBoard(log_dir='./dataset/raw_training_tb', histogram_freq=0, write_graph=True, write_images=True)

    data_gen = generate_data_batches(files, batch_size, val_training_factor)

    val_data_gen = generate_val_data_batches(files, batch_size, val_training_factor)

    train_batch_count, val_batch_count = get_data_metric(files, batch_size, val_training_factor)

    print('train_batch_count, val_batch_count: ', train_batch_count,', ', val_batch_count)

    model.fit_generator(data_gen, validation_data=val_data_gen, validation_steps=val_batch_count, steps_per_epoch=train_batch_count, epochs=epochs, verbose=1)
    model.save_weights('storage/train_raw_weights.h5')

if __name__ == "__main__":
    main()
