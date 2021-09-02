
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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


def generateModel(data=TestDataGenerator.getRandomTrainingData(3000), recreate=True):
    global columns
    columns = data.columns.values

    if recreate:
        x_train, x_test, y_train, y_test = preprocessDataframe(data, split=True)
        inputs = x_train.shape[1]
        outputs = y_train.shape[1]

        model = Sequential()
        model.add(Dense(500, activation="relu", input_dim=inputs))
        model.add(Dense(100, activation="relu"))
        model.add(Dense(50, activation="relu"))
        model.add(Dense(outputs, activation="softmax"))

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=20)
        model.save("car_model")

        pred_train = model.predict(x_train)
        scores = model.evaluate(x_train, y_train, verbose=0)
        print('Accuracy on training data: {}% \n Error on training data: {}'.format(scores[1], 1 - scores[1]))

        pred_test = model.predict(x_test)
        scores2 = model.evaluate(x_test, y_test, verbose=0)
        print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))
    else:
        model = tf.keras.models.load_model("car_model")
    return model

"""
model = generateModel(recreate=True)

test = TestDataGenerator.getRandomTrainingData(1)
for index, obj in test.iterrows():
    predict(model=model, relationship=obj["relationship"], birthday=obj["birthday"], budget=obj["budget"],
            cars=obj["cars"], city=obj["city"], dogs=obj["dogs"],
            family=obj["family"], friends=obj["friends"], hiking=obj["hiking"], mountainbiking=obj["mountainbiking"],
            party=obj["party"], plan=obj["plan"], shared_mobility=obj["shared_mobility"],
            skiing=obj["skiing"], two_wheels=obj["two_wheels"]
            , yearly_drive=obj["yearly_drive"], style=obj["style"])
"""
print("Done")

class CarPickerAI():

    def __init__(self):
        self.model = generateModel(recreate=True)

    def predict(self, relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs, cars,
            shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive):
        return predict(self.model, relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs, cars, shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive)
