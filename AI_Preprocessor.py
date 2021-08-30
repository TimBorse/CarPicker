from copy import copy


from sklearn.preprocessing import LabelEncoder

categoricalColumns = ['relationship', 'friends', 'hiking', 'party', 'city', 'mountainbiking', 'family', 'skiing',
                      'dogs', 'cars', 'shared_mobility', 'two_wheels']

numericalColumns = ['plan', 'budget', 'birthday', 'yearly_drive']

min_max = {
    "relationship": {"min": 0, "max": 3},
    "friends": {"min": 0, "max": 1},
    "hiking": {"min": 0, "max": 1},
    "party": {"min": 0, "max": 1},
    "city": {"min": 0, "max": 1},
    "mountainbiking": {"min": 0, "max": 1},
    "family": {"min": 0, "max": 1},
    "skiing": {"min": 0, "max": 1},
    "dogs": {"min": 0, "max": 1},
    "cars": {"min": 0, "max": 1},
    "shared_mobility": {"min": 0, "max": 1},
    "two_wheels": {"min": 0, "max": 1},
    "plan": {"min": 6, "max": 48},
    "budget": {"min": 0, "max": 2000},
    "style": {"min": 0, "max": 100},
    "birthday": {"min": 1940, "max": 2000},
    "yearly_drive": {"min": 0, "max": 50000},
}



def scaleMinMax(min, max, values):
    values = (values - min) / (max - min)
    return values

class AI_Preprocessor():

    def __init__(self):
        self.copy = copy
        self.labels = {}
        self.encoders = {}

    def transformColumn(self, data, column):
        try:
            le = self.encoders[column]
            data[column] = le.transform(data[column])
        except:
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            self.labels[column] = le.classes_
            self.encoders[column] = le

    def normalizeData(self, dataframe):
        columns = dataframe.columns.values
        for catCol in categoricalColumns:
            self.transformColumn(dataframe, catCol)
        for col in columns:
            dataframe[col] = scaleMinMax(min=min_max[col]["min"], max=min_max[col]["max"], values=dataframe[col])
        return dataframe

