import numpy as np
import pandas
import keras
from keras import layers
from keras import regularizers
from keras.datasets import mnist

def convert_to_one_hot(y):
    max_value = max(y)
    min_value = min(y)
    length = len(y)
    one_hot = np.zeros((length, (max_value - min_value + 1)))
    one_hot[np.arange(length), y - min_value] = 1
    return one_hot


def convert_from_one_hot(y):
    y_origin = np.argmax(y, axis=1)
    return y_origin


def model(input_shape):
    input_frame = keras.Input(shape=input_shape)
    F1 = layers.Dense(500, activation="relu", kernel_regularizer=regularizers.l2(0.03))(input_frame)
    output_layer = layers.Dense(2, activation="softmax")(F1)
    model = keras.Model(inputs=input_frame, outputs=output_layer)
    return model


(train_X, train_y), (test_X, test_y) = mnist.load_data()
train_X = train_X.reshape(train_X.shape[0], -1)
test_X = test_X.reshape(test_X.shape[0], -1)
train_X = train_X / 255
test_X = test_X / 255
train_y = convert_to_one_hot(train_y)
test_y = convert_to_one_hot(test_y)

nn_model = model(train_X.shape[1:])
nn_model.compile(optimizer=keras.optimizers.Adadelta(learning_rate=0.05),
                 loss='categorical_cross entropy',
                 metrics=['accuracy'])

nn_model.summary()
train_dataset = keras.datasets.from_tensor_slices((train_X, train_y)).batch(train_X.shape[0])
test_dataset = keras.datasets.from_tensor_slices((test_X, test_y)).batch(test_X.shape[0])
history = nn_model.fit(train_dataset, epochs=15, validation_data=test_dataset)

df_loss_acc = pandas.DataFrame(history, history)
df_loss = df_loss_acc[['loss', 'val_loss']]
df_loss.rename(columns={'loss': 'train', 'val_loss': 'validation'}, inplace=True)
df_acc = df_loss_acc[['accuracy', 'val_accuracy']]
df_acc.rename(columns={'accuracy': 'train', 'val_accuracy': 'validation'}, inplace=True)
df_loss.plot(title="Model loss", figsize=(12, 8)).set(xlabel='Epoch', ylabel='loss')
df_acc.plot(title='Model Accuracy', figsize=(12, 8)).set(xlabel='Epoch', ylabel='Accuracy')
