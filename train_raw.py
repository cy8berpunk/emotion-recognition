import keras
from keras.layers import *
from keras.models import Model
from keras.regularizers import l2
from keras.optimizers import SGD
from cnn_model.models import *
from utils.data import *
import calendar
import random
import time

def main():
    epochs = 10
    batchSize = 32
    VALTrainingFactor = 0.7
    learningRate = 0.001
    dataSetDir = 'data/MPI_large_centralcam_hi_islf_complete/**'
    files='data/raw/**'

    classes = getClassesForDataSet(dataSetDir)

    model = basicCNNModel((256, 256, 3), len(classes))
    model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=learningRate), metrics=['accuracy'])

    print('training model on raw unlabeld data \r')

    tbCallBack = keras.callbacks.TensorBoard(log_dir='data/tensorBoard/raw_training_tb_'+str(learningRate)+'_'+str(calendar.timegm(time.gmtime())), histogram_freq=0, write_graph=True, write_images=True)

    data_gen = generate_data_batches(files, batchSize, VALTrainingFactor)

    val_data_gen = generate_val_data_batches(files, batchSize, VALTrainingFactor)

    train_batch_count, val_batch_count = get_data_metric(files, batchSize, VALTrainingFactor)

    print('train_batch_count, val_batch_count: ', train_batch_count,', ', val_batch_count)

    model.fit(data_gen, validation_data=val_data_gen, shuffle=True, validation_steps=val_batch_count, steps_per_epoch=train_batch_count, epochs=epochs, verbose=1, callbacks=[tbCallBack])
    randomId = str(random.randrange(500))
    print('Model Id: ' + randomId)
    model.save_weights('data/trainedModels/train_raw_weight_'+randomId+'.h5')

if __name__ == "__main__":
    main()
