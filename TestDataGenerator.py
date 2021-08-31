

import datetime
from random import randint
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

import CarDatasetUtils
import SNConnector

cars = SNConnector.getCars()

family_labels = ["single", "couple", "small_family", "big_family"]
freetime_labels = ["friends", "hiking", "party", "city_trip", "mountainbiking", "family", "skiing", "dogs"]
mobility_labels = ["car", "two_wheels", "shared_mobility"]
# Elegant 0 - 100 Fresh
style = 50
# 0 - 100 000km
yearly_drive = 50000
planahead_labels = [6, 12, 18, 24, 36, 48]
# 0 - 2000 €
monthly_budget = 1000
birth_date = "19-08-2021"

def getInputsFromDataset(dataset):
    df = CarDatasetUtils.cleanDataframe(pd.read_csv(dataset))
    relationships = []
    friends = []
    hiking = []
    party = []
    city = []
    mountainbiking = []
    family = []
    skiing = []
    dogs = []
    cars = []
    shared_mobility = []
    two_wheels = []
    style = []
    plan = []
    budget = []
    birthday = []
    yearly_drive = []
    target = []
    is_car = df["Marke"]=="BMW"
    car = df[is_car]
    print(car["Modell"].unique())
    for index, obj in df.iterrows():
        print("")


def getRandomInputs():
    inputs = []
    # Family
    inputs.append(family_labels[randint(0, len(family_labels) - 1)])

    # Freetime
    openFreetime = freetime_labels.copy()
    selectedFreetime = []
    for i in range(randint(1, len(freetime_labels))):
        index = randint(0, len(openFreetime) - 1)
        selectedFreetime.append(openFreetime[index])
        openFreetime.remove(openFreetime[index])
        friends = selectedFreetime.__contains__("friends")
        hiking = selectedFreetime.__contains__("hiking")
        party = selectedFreetime.__contains__("party")
        city = selectedFreetime.__contains__("city_trip")
        mountainbiking = selectedFreetime.__contains__("mountainbiking")
        family = selectedFreetime.__contains__("family")
        skiing = selectedFreetime.__contains__("skiing")
        dogs = selectedFreetime.__contains__("dogs")
        freetimes = [friends, hiking, party, city, mountainbiking, family, skiing, dogs]

    inputs.append(freetimes)

    # Mobility
    openMobility = mobility_labels.copy()
    selectedMobility = []
    for j in range(randint(1, len(mobility_labels))):
        index = randint(0, len(openMobility) - 1)
        selectedMobility.append(openMobility[index])
        openMobility.remove(openMobility[index])
        car = selectedMobility.__contains__("car")
        shared = selectedMobility.__contains__("shared_mobility")
        twowheels = selectedMobility.__contains__("two_wheels")
        mobilities = [car, shared, twowheels]
    inputs.append(mobilities)

    # Style
    inputs.append(randint(0, 100))

    # Plan
    inputs.append(planahead_labels[randint(0, len(planahead_labels) - 1)])

    # Budget
    inputs.append(randint(0, 2000))

    day = randint(1, 28)
    month = randint(1, 12)
    year = randint(1940, 2000)
    inputs.append(datetime.datetime(year, month, day))
    inputs.append(randint(0, yearly_drive))
    return inputs


def getInputResult(input):
    relationship = input[0]
    freetime = input[1]
    mobility = input[2]
    style = int(input[3]) / 10
    plan = input[4]
    budget = input[5]
    birth = input[6]
    drive = input[7]

    def getMinTrunkspace():
        minTrunkSpace = 0
        if relationship == "couple":
            minTrunkSpace = 300
        if relationship == "small_family" or freetime[0] or freetime[1] or freetime[7]:
            minTrunkSpace = 400
        if relationship == "big_family" or freetime[5] or freetime[4] or freetime[6]:
            minTrunkSpace = 500
        return minTrunkSpace

    def getMinSeats():
        minSeats = 2
        if relationship == "small_family" or relationship == "big_family" or freetime[5] or freetime[0]:
            minSeats = 5
        return minSeats

    def getMinCityRange():
        minRange = 0
        if freetime[2]:
            minRange = 400
        if freetime[3]:
            minRange = 500
        return minRange

    def getMinCountryRange():
        minRange = 0
        if freetime[1] or freetime[4]:
            minRange = 1000
        return minRange

    def getMinRange():
        return drive / 40

    def getMinBudget():
        return budget

    def getResultScore(obj):
        return obj['score']

    minTrunkSpace = getMinTrunkspace()
    minSeats = getMinSeats()
    minCityRange = getMinCityRange()
    minCountryRange = getMinCountryRange()
    minRange = getMinRange()
    minBudget = getMinBudget()
    day = birth.day
    month = birth.month
    year = birth.year
    birthdate = datetime.datetime(year, month, day)
    now = datetime.datetime.now()
    age = (now - birthdate).days / 365
    rankings = []

    for car in cars:
        score = 0

        if minBudget < int(car['monthlyprice']) or int(car['trunkvolume']) < minTrunkSpace or age < int(
                car['minage']) or int(car['seats']) < minSeats or int(car['rangecity']) < minCityRange or int(
            car['rangecountry']) < minCountryRange or int(car['rangecombined']) < minRange or (
                (relationship == "small_family" or relationship == "big_family" or freetime[5]) and
                car['childseatmount'] != 'true' or ((car['vehicletype'] == "car" and not mobility[0]) or (
                car['vehicletype'] == "bike" and not mobility[2]) or (
                                                            car['vehicletype'] == "sharedmobility" and not mobility[
                                                        1]))):
            score = -1
            obj = {'car': car,
                   'score': score
                   }
            rankings.append(obj)
            continue

        if freetime[4] or freetime[6]:

            score += int(car['offroad'])

            if freetime[4] and car['trailerhitch'] == 'true':
                score += 10

            if freetime[6] and car['roofrack'] == 'true':
                score += 10

        if freetime[3] and car['kindofmobility'] == "electriccar":
            score += 10

        score += 10 - (int(car['style']) - style)

        obj = {'car': car,
               'score': score
               }
        rankings.append(obj)

    rankings.sort(key=getResultScore, reverse=True)
    return rankings


def getAttributeFromInput(input, index):
    values = []
    for x in input:
        values.append(x[index])
    return np.array(values)


def getResultID(input):
    values = []
    for x in input:
        values.append(x['car']['sys_id'])
    return np.array(values)


def getYears(birth_date):
    years = []
    for x in birth_date:
        years.append(x.year)
    return np.array(years)


def createFlattenedDataframe(inputs, results):
    freetime = np.array(getAttributeFromInput(inputs, 1))
    mobility = np.array(getAttributeFromInput(inputs, 2))
    birth_date = getYears(getAttributeFromInput(inputs, 6))
    le = LabelEncoder()
    d = {'relationship': le.fit_transform(getAttributeFromInput(inputs, 0)),
         'friends': le.fit_transform(freetime[:, 0]),
         'hiking': le.fit_transform(freetime[:, 1]),
         'party': le.fit_transform(freetime[:, 2]),
         'city': le.fit_transform(freetime[:, 3]),
         'mountainbiking': le.fit_transform(freetime[:, 4]),
         'family': le.fit_transform(freetime[:, 5]),
         'skiing': le.fit_transform(freetime[:, 6]),
         'dogs': le.fit_transform(freetime[:, 7]),
         'cars': le.fit_transform(mobility[:, 0]),
         'shared_mobility': le.fit_transform(mobility[:, 1]),
         'two_wheels': le.fit_transform(mobility[:, 2]),
         'style': getAttributeFromInput(inputs, 3),
         'plan': getAttributeFromInput(inputs, 4),
         'budget': getAttributeFromInput(inputs, 5),
         'birthday': birth_date,
         'yearly_drive': getAttributeFromInput(inputs, 7),
         'target': le.fit_transform(getResultID(results))
         }
    return pd.DataFrame(data=d)

def createDataframe(inputs, results):
    freetime = np.array(getAttributeFromInput(inputs, 1))
    mobility = np.array(getAttributeFromInput(inputs, 2))
    birth_date = getYears(getAttributeFromInput(inputs, 6))
    d = {'relationship': getAttributeFromInput(inputs, 0),
         'friends': freetime[:, 0],
         'hiking': freetime[:, 1],
         'party': freetime[:, 2],
         'city': freetime[:, 3],
         'mountainbiking': freetime[:, 4],
         'family': freetime[:, 5],
         'skiing': freetime[:, 6],
         'dogs': freetime[:, 7],
         'cars': mobility[:, 0],
         'shared_mobility': mobility[:, 1],
         'two_wheels': mobility[:, 2],
         'style': getAttributeFromInput(inputs, 3),
         'plan': getAttributeFromInput(inputs, 4),
         'budget': getAttributeFromInput(inputs, 5),
         'birthday': birth_date,
         'yearly_drive': getAttributeFromInput(inputs, 7),
         'target': getResultID(results)
         }
    df = pd.DataFrame(data=d)
    return df


def getRandomTrainingData(amount):
    inputs = []
    results = []
    for i in range(amount):
        while True:
            input = getRandomInputs()
            result = getInputResult(input)
            if result[0]['score'] > 0:
                inputs.append(input)
                results.append(result[0])
                break
    dataframe = createDataframe(inputs, results)

    return dataframe

getInputsFromDataset("AI Dataset.csv")