import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, Dropout
import pandas as pd
import numpy as np
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from kerastuner.tuners import RandomSearch
from kerastuner.engine.hyperparameters import HyperParameters
import time
from AI_Preprocessor import AI_Preprocessor
import TestDataGenerator

categoricalColumns = ['relationship', 'friends', 'hiking', 'party', 'city', 'mountainbiking', 'family', 'skiing',
                      'dogs', 'cars', 'shared_mobility', 'two_wheels', 'target']
numericalColumns = ['plan', 'budget', 'birthday', 'yearly_drive']
predictors = ['relationship', 'friends', 'hiking', 'party', 'city', 'mountainbiking', 'family', 'skiing', 'dogs',
              'cars', 'shared_mobility', 'two_wheels', 'style', 'plan', 'budget', 'birthday', 'yearly_drive']
labels = {}
predictions = []
Preprocessor = AI_Preprocessor()


def transformColumn(data, column):
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    labels[column] = le.classes_


def preprocessDataframe(data, target="target", split=False):
    target_column = [target]
    data[predictors] = Preprocessor.normalizeData(data[predictors])
    Preprocessor.transformColumn(data, target)
    data.describe()
    if split:
        return splitData(data, target_column)
    return data


def splitData(data, target_column):
    x = data[predictors].values
    y = data[target_column].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    return x_train, x_test, y_train, y_test


def translatePrediction(data, prediction):
    prediction = prediction
    print("Inputs:\n")
    for i in range(len(data)):
        print(columns[i], ": ", data[i])
    print("Prediction: ", prediction)


def predict(model, relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs, cars,
            shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive):
    data = {'relationship': [relationship],
            'friends': [friends],
            'hiking': [hiking],
            'party': [party],
            'city': [city],
            'mountainbiking': [mountainbiking],
            'family': [family],
            'skiing': [skiing],
            'dogs': [dogs],
            'cars': [cars],
            'shared_mobility': [shared_mobility],
            'two_wheels': [two_wheels],
            'style': [style],
            'plan': [plan],
            'budget': [budget],
            'birthday': [birthday],
            'yearly_drive': [yearly_drive]
            }
    print("Inputs:\n")
    for col in data:
        print(str(col), ":", str(data[col]))

    df = pd.DataFrame(data=data)
    df = Preprocessor.normalizeData(df)
    values = df.values
    predict = model.predict(values)
    print(Preprocessor.labels["target"][np.argmax(predict[0])])
    predictions.append(Preprocessor.labels["target"][np.argmax(predict[0])])
    return Preprocessor.labels["target"][np.argmax(predict[0])]


def generateModel(data=TestDataGenerator.getRandomTrainingData(500), search_params=False, trials=250, directory=None):
    global columns
    columns = data.columns.values
    x_train, x_test, y_train, y_test = preprocessDataframe(data, split=True)
    inputs = x_train.shape[1]
    outputs = y_train.shape[1]

    def buildModel(hp):
        model = Sequential()
        model.add(
            Dense(hp.Int("input_units", 16, 512, 32), activation=hp.Choice('act_input', ['relu', 'sigmoid', 'tanh']),
                  input_dim=inputs))
        for i in range(hp.Int("n_layers", 1, 4)):
            model.add(Dense(hp.Int(f"dense_{i}_units", 16, 512, 32),
                            activation=hp.Choice('act_' + str(i), ['relu', 'sigmoid', 'tanh'])))
        model.add(Dense(outputs, activation="softmax"))

        model.compile(optimizer=tf.keras.optimizers.Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    if search_params:
        LOG_DIR = f"{int(time.time())}"
        tuner = RandomSearch(
            buildModel,
            objective="val_accuracy",
            max_trials=trials,
            executions_per_trial=3,
            directory=directory
        )
        if directory == None:
            tuner.search(x_train, y_train, epochs=30, validation_data=(x_test, y_test))
        model = tuner.get_best_models(1)[0]
        model.fit(x_train, y_train, epochs=30, batch_size=8)
        return model


    else:
        model = Sequential()
        model.add(Dense(240, activation="relu", input_dim=inputs))
        model.add(Dense(176, activation="relu"))
        model.add(Dense(240, activation="relu"))
        model.add(Dense(outputs, activation="softmax"))
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=40, batch_size=4)
        model.save("car_model")

    pred_train = model.predict(x_train)
    scores = model.evaluate(x_train, y_train, verbose=0)
    print('Accuracy on training data: {}% \n Error on training data: {}'.format(scores[1], 1 - scores[1]))

    pred_test = model.predict(x_test)
    scores2 = model.evaluate(x_test, y_test, verbose=0)
    print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))
    return model

class CarPickerAI():

    def __init__(self):
        self.model = generateModel(search_params=True)

    def predict(self, relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs, cars,
                shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive):
        return predict(self.model, relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs,
                       cars, shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive)
