import datetime
from random import randint
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

import CarDatasetUtils
import Cities
import SNConnector

cars = SNConnector.getCars()

family_labels = ["single", "couple", "small_family", "big_family"]
freetime_labels = ["friends", "hiking", "party", "city_trip", "mountainbiking", "family", "skiing", "dogs"]
mobility_labels = ["car", "two_wheels", "shared_mobility"]
planahead_labels = [6, 12, 18, 24, 36, 48]

max_yearly_drive = 50000


def getCarById(carId):
    for car in cars:
        if car['sys_id'] == carId:
            return car
    return None

def getCarsByCategory(category):
    resultCars = []
    for car in cars:
        if category == 'limo' and (car['vehiclecategory']=='limousine' or car['vehiclecategory']=='coupe' or car['vehiclecategory']=='sports'):
            resultCars.append(car)
        elif category == 'suv' and (car['vehiclecategory']=='suv' or car['vehiclecategory']=='terrain'):
            resultCars.append(car)
        else:
            if car['vehiclecategory']==category:
                resultCars.append(car)
    return resultCars


def getRandomBoolean(chance):
    rdm = randint(0, 100)
    if rdm <= chance:
        return True
    return False


def getRandomString(stringList):
    return stringList[randint(0, len(stringList) - 1)]

def getResultScore(obj):
    return obj['score']

def getInputsFromDataset(dataset):
    def filterCars(carsList, type_filter=None):
        filteredCars = []
        for car in carsList:
            if car['type'] == type_filter:
                filteredCars.append(car)
        if len(filteredCars) < 1:

            return carsList
        return filteredCars

    def setValuesByCity(isCity, partyChance, category, minDrive, maxDrive, possible_cars):
        cityValue = isCity
        partyValue = getRandomBoolean(partyChance)
        possibleCarsValue = filterCars(possible_cars, category)
        yearly_driveValue = randint(minDrive, maxDrive)
        return cityValue, partyValue, possibleCarsValue, yearly_driveValue

    def setValuesByCategory(relationshipsList, familyChance, hikingChance, skiingChance, mountainbikingChance, dogsChance,
                            friendsChance, carsState, sharedState, twowheelsState, styleLower, styleUpper):
        relationshipsValue = getRandomString(relationshipsList)
        familyValue = getRandomBoolean(familyChance)
        hikingValue = getRandomBoolean(hikingChance)
        skiingValue = getRandomBoolean(skiingChance)
        mountainbikingValue = getRandomBoolean(mountainbikingChance)
        dogsValue = getRandomBoolean(dogsChance)
        friendsValue = getRandomBoolean(friendsChance)
        carsValue = carsState
        shared_mobilityValue = sharedState
        two_wheelsValue = twowheelsState
        styleValue = randint(styleLower, styleUpper)
        return relationshipsValue, familyValue, hikingValue, skiingValue, mountainbikingValue, dogsValue, friendsValue, carsValue, shared_mobilityValue, two_wheelsValue, styleValue

    df = CarDatasetUtils.cleanDataframe(pd.read_csv(dataset))
    inputs = []
    results = []

    for row in df.iterrows():
        cityPopulation = Cities.getCityPopulation(row[1]['Stadt'], row[1]['PLZ'])
        possibleCars = CarDatasetUtils.modelMap[row[1]['Marke']][row[1]['Modell']]

        if cityPopulation > 100000:
            if row[1]['Kilometerstand'] > 50000:
                city, party, possibleCars, yearly_drive = setValuesByCity(True, 50, 'hybrid', 20000, 50000,
                                                                          possibleCars)
            else:
                city, party, possibleCars, yearly_drive = setValuesByCity(True, 50, 'electric', 5000, 20000,
                                                                          possibleCars)
        else:
            if row[1]['Kilometerstand'] > 50000:
                city, party, possibleCars, yearly_drive = setValuesByCity(False, 20, 'diesel', 20000, 50000,
                                                                          possibleCars)
            else:
                city, party, possibleCars, yearly_drive = setValuesByCity(False, 20, 'petrol', 5000, 20000,
                                                                          possibleCars)
        selectedCar = {'car': getCarById(possibleCars[randint(0, len(possibleCars) - 1)]['id'])}
        results.append(selectedCar)
        if selectedCar['car']['vehiclecategory'] == 'combi':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["small_family", "big_family"], 70, 50, 50, 50, 50, 50, True, False, False, 1, 4)
        elif selectedCar['car']['vehiclecategory'] == 'suv':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["small_family", "big_family"], 70, 80, 60, 65, 50, 50, True, False, False, 2, 6)
        elif selectedCar['car']['vehiclecategory'] == 'compact':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["single", "couple", "small_family"], 10, 10, 10, 10, 40, 60, True, False, False, 4, 7)
        elif selectedCar['car']['vehiclecategory'] == 'limousine':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["single", "couple", "small_family"], 10, 10, 10, 10, 10, 20, True, False, False, 3, 7)
        elif selectedCar['car']['vehiclecategory'] == 'sports':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["single", "couple"], 5, 5, 5, 5, 5, 5, True, False, False, 8, 10)
        elif selectedCar['car']['vehiclecategory'] == 'coupe':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["single", "couple", "small_family"], 10, 10, 10, 10, 10, 30, True, False, False, 4, 8)
            relationships = getRandomString(["single", "couple", "small_family"])
        elif selectedCar['car']['vehiclecategory'] == 'terrain':
            relationships, family, hiking, skiing, mountainbiking, dogs, friends, cars, shared_mobility, two_wheels, style = setValuesByCategory(
                ["single", "couple", "small_family", "big_family"], 40, 80, 60, 70, 35, 10, True, False, False, 4, 6)

        plan = planahead_labels[randint(0, len(planahead_labels) - 1)]
        day = randint(1, 28)
        month = randint(1, 12)
        year = randint(1940, 2000)
        birthday = datetime.datetime(year, month, day)
        budget = randint(int(selectedCar['car']['monthlyprice']), 2500)
        freetimes = [friends, hiking, party, city, mountainbiking, family, skiing, dogs]
        mobilities = [cars, shared_mobility, two_wheels]
        input = [relationships, freetimes, mobilities, style, plan, budget, birthday, yearly_drive]
        inputs.append(input)
    return inputs, results


def getRandomInputs():
    inputs = [family_labels[randint(0, len(family_labels) - 1)]]
    # Family

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
    inputs.append(randint(700, 3000))

    day = randint(1, 28)
    month = randint(1, 12)
    year = randint(1940, 2000)
    inputs.append(datetime.datetime(year, month, day))
    inputs.append(randint(0, max_yearly_drive))
    return inputs


def getBestCategory(relationship, freetime, style,  drive):

    combiScore = 0
    compactScore = 0
    limoScore = 0
    suvScore = 0
    friends = freetime[0]
    hiking = freetime[1]
    party = freetime[2]
    city = freetime[3]
    mountainbiking = freetime[4]
    family = freetime[5]
    skiing = freetime[6]
    dogs = freetime[7]

    if relationship == "single":
        combiScore += 2
        compactScore += 4
        limoScore += 3
        suvScore += 1
    elif relationship == "couple":
        combiScore += 2
        compactScore += 3
        limoScore += 4
        suvScore += 1
    elif relationship == "small_family":
        combiScore += 4
        compactScore = -100
        limoScore += 2
        suvScore += 3
    elif relationship == "big_family":
        combiScore += 4
        compactScore = -100
        limoScore += 2
        suvScore += 3
    if friends:
        combiScore += 2
        compactScore += 3
        limoScore += 4
        suvScore += 1
    if hiking:
        combiScore += 3
        compactScore += 1
        limoScore += 2
        suvScore += 4
    if party:
        combiScore += 2
        compactScore += 4
        limoScore += 3
        suvScore += 1
    if city:
        combiScore += 2
        compactScore += 4
        limoScore += 3
        suvScore += 1
    if mountainbiking:
        combiScore += 3
        compactScore += 1
        limoScore += 2
        suvScore += 4
    if family:
        combiScore += 4
        compactScore += 1
        limoScore += 2
        suvScore += 3
    if skiing:
        combiScore += 3
        compactScore += 1
        limoScore += 2
        suvScore += 4
    if dogs:
        combiScore += 3
        compactScore += 1
        limoScore += 2
        suvScore += 4

    combiScore += 4-int(style*0.4)
    compactScore += int(style*0.4)
    limoScore += int(style*0.4)
    suvScore += 4-int(style*0.4)

    if drive < 10000:
        combiScore += 2
        compactScore += 3
        limoScore += 4
        suvScore += 1
    elif drive < 25000:
        combiScore += 2
        compactScore += 4
        limoScore += 3
        suvScore += 1
    else:
        combiScore += 3
        compactScore += 1
        limoScore += 2
        suvScore += 4
    result = [{'category' : 'combi', 'score': combiScore}, {'category' : 'compact', 'score': compactScore}, {'category' : 'limo', 'score': limoScore}, {'category' : 'suv', 'score': suvScore}]
    result.sort(key=getResultScore, reverse=True)
    print(result[0]['category'])
    # Todo
    return result[0]['category']


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
            minTrunkSpace += 200
        if relationship == "small_family":
            minTrunkSpace = 300
        if relationship == "big_family":
            minTrunkSpace += 400
        if freetime[0]:
            minTrunkSpace += 50
        if freetime[6]:
            minTrunkSpace += 50
        if freetime[1]:
            minTrunkSpace += 100
        if freetime[7]:
            minTrunkSpace += 100
        if freetime[5]:
            minTrunkSpace += 100
        if freetime[6]:
            minTrunkSpace += 100
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
    possibleCars = getCarsByCategory(getBestCategory(relationship, freetime, style, drive))
    rankings = []

    for car in possibleCars:
        score = 0
        # Checks budget
        if minBudget < int(car['monthlyprice']) or int(car['seats']) < minSeats or (
                style > 5 and int(car['style']) <= 5) or (style <= 5 and int(car['style']) > 5):
            score = -1
            obj = {'car': car,
                   'score': score
                   }
            rankings.append(obj)
            continue

        # Checks trunkspace
        if int(car['trunkvolume']) > minTrunkSpace:
            score += 7
            difference = int(car['trunkvolume']) - minTrunkSpace
            if difference < 50:
                score += 3
            elif difference < 100:
                score += 2
            elif difference < 200:
                score += 1

        # Checks range
        weekly_drive = drive / 52
        if int(car['rangecombined']) > weekly_drive * 2:
            score += 10
        elif int(car['rangecombined']) > weekly_drive:
            score += 5
        elif car['kindofmobility'] == 'electriccar':
            daily_drive = drive / 365
            if int(car['rangecombined']) > daily_drive * 2:
                score += 10
            if int(car['rangecombined']) > daily_drive + 50:
                score += 5

        # Checks freetime
        if freetime[4] or freetime[6]:

            score += int(car['offroad'])

            if freetime[4] and car['trailerhitch'] == 'true':
                score += 10

            if freetime[6] and car['roofrack'] == 'true':
                score += 10

        # Checks kind of car
        if freetime[3]:
            if minRange > 500 and car['kindofmobility'] == 'hybridpetrolcar':
                score += 20
            elif minRange < 500 and car['kindofmobility'] == 'electriccar':
                score += 20
        else:
            if weekly_drive > 750 and car['kindofmobility'] == 'dieselcar':
                score += 20

        # ToDo: Kompaktheit

        # Checks style
        score += (10 - (int(car['style']) - style)) * 2

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
    inputs1 = []
    results1 = []
    dataframe1 = pd.DataFrame()
    if amount > 300:
        inputs1, results1 = getInputsFromDataset("AI Dataset.csv")
        dataframe1 = createDataframe(inputs1, results1)
    inputs2 = []
    results2 = []
    for i in range(amount - len(inputs1)):
        while True:
            input = getRandomInputs()
            result = getInputResult(input)
            if result[0]['score'] > 0:
                inputs2.append(input)
                results2.append(result[0])
                break
    dataframe2 = createDataframe(inputs2, results2)
    frames = [dataframe1, dataframe2]
    dataframe = pd.concat(frames)
    return dataframe

# getRandomTrainingData(500)
# inputs, results = getInputsFromDataset("AI Dataset.csv")
# createDataframe(inputs, results)
