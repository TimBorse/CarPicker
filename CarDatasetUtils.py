import pandas as pd

suvs = [{'id': 'b81004fedbda3850836009c4e2961971',
         'price': 812,
         'type': 'diesel'},
        {'id': 'f506582adb9af450836009c4e29619ce',
         'price': 1150,
         'type': 'electric'},
        {'id': 'abc21294dbea7410836009c4e2961984',
         'price': 895,
         'type': 'petrol'},
        {'id': 'd6d4d218dbea7410836009c4e2961918',
         'price': 1562,
         'type': 'hybrid'}
        ]
kompaktlimo = [{'id': '966db3eadbda3850836009c4e296190a',
                'price': 750,
                'type': 'petrol'}]
limo = [{'id': 'f4a5b722dbda3850836009c4e29619d1',
         'price': 765,
         'type': 'hybrid'},
        {'id': '0c5f73aedbda3850836009c4e29619fb',
         'price': 1166,
         'type': 'petrol'},
        {'id': '891bb32adbda3850836009c4e2961915',
         'price': 2250,
         'type': 'diesel'},
        {'id': '687e772edbda3850836009c4e2961922',
         'price': 1450,
         'type': 'electric'}]
tmodel = [{'id': 'f6f1c072db1e3850836009c4e2961955',
           'price': 953,
           'type': 'petrol'},
          {'id': '8c0ab32adbda3850836009c4e296190b',
           'price': 1250,
           'type': 'hybrid'},
          {'id': 'dd57186adb9af450836009c4e29619c5',
           'price': 1250,
           'type': 'diesel'},
          {'id': '5d66506adb9af450836009c4e29619e3',
           'price': 699,
           'type': 'electric'}]
coupe = [{'id': '94acb3eadbda3850836009c4e2961903',
          'price': 680,
          'type': 'diesel'},
         {'id': '4c4973e6dbda3850836009c4e296194b',
          'price': 833,
          'type': 'hybrid'},
         {'id': 'ec410cfedbda3850836009c4e29619cf',
          'price': 1104,
          'type': 'diesel'},
         {'id': 'd7b6186adb9af450836009c4e29619bc',
          'price': 1399,
          'type': 'petrol'}]
sport = [{'id': 'bbd200b2db1e3850836009c4e29619ca',
          'price': 2500,
          'type': 'petrol'}]
terrain = [{'id': '78900cfedbda3850836009c4e29619c9',
            'price': 2400,
            'type': 'petrol'}]
modelMap = {'Mercedes-Benz': {'C-Klasse': tmodel,
                              'E-Klasse': limo,
                              'M-Klasse': suvs,
                              'A-Klasse': kompaktlimo,
                              'G-Klasse': terrain
                              },
            'Audi': {'A4': tmodel,
                     'A6': limo,
                     'A3': tmodel,
                     'S3': kompaktlimo,
                     'Q5': suvs,
                     'A1': kompaktlimo,
                     'A5': coupe,
                     'Q7': suvs,
                     'SQ5': suvs
                     },
            'Porsche': {'Cayenne': sport,
                        'Panamera': sport,
                        '911': sport,
                        'Boxster': sport
                        },
            'Tesla': {'Model S': [{'id': '8c0ab32adbda3850836009c4e296190b',
                                  'price': 1250,
                                  'type': 'hybrid'}]},
            'Volvo': {'S60': tmodel},
            'Volkswagen': {'Passat': tmodel,
                           'Passat CC': limo,
                           'Touareg': suvs,
                           'Tiguan': suvs,
                           'Golf': kompaktlimo,
                           'Beetle': kompaktlimo,
                           'Golf Sportsvan': tmodel,
                           'Polo': kompaktlimo,
                           'Passat Variant': tmodel,
                           'Golf GTI': kompaktlimo,
                           'Golf Variant': tmodel
                           },
            'Mazda': {'6': tmodel,
                      'CX-5': suvs,
                      '3': tmodel
                      },
            'Opel': {'Insignia': limo,
                     'Corsa': kompaktlimo,
                     'Astra': tmodel,
                     'Cascada': coupe
                     },
            'Skoda': {'Superb': tmodel,
                      'Octavia': tmodel,
                      'Fabia': kompaktlimo,
                      'Yeti': terrain
                      },
            'Ford': {'Mondeo': tmodel,
                     'Kuga': suvs,
                     'Focus': tmodel,
                     'Fiesta': kompaktlimo
                     },
            'Kia': {'Optima': tmodel,
                    'Sportage': suvs
                    },
            'Nissan': {'370Z': sport},
            'Honda': {'CR-V': suvs,
                      'Civic': limo,
                      'Jazz': kompaktlimo
                      },
            'Renault': {'Koleos': suvs,
                        'Clio': kompaktlimo
                        },
            'Hyundai': {'i20': kompaktlimo,
                        'i30': tmodel
                        },
            'Toyota': {'Auris': tmodel,
                       'Yaris': kompaktlimo
                       },
            'Suzuki': {'Grand Vitara': terrain},
            'BMW': {'316': limo,
                    '116': tmodel,
                    'X5': suvs,
                    '118': tmodel,
                    '520': limo,
                    'X3': suvs,
                    'X1': suvs,
                    '523': limo,
                    '320': coupe,
                    '535': limo,
                    '135': tmodel,
                    '530': tmodel,
                    '114': tmodel,
                    '335': coupe,
                    '325': coupe,
                    '525': limo,
                    '318': limo,
                    '330': limo
                    }
            }


def convertSpecialChars(string):
    return string.replace("√∂", "ö").replace("√º", "ü").replace("√§", "ä").replace("√ü", "ß").replace("ue",
                                                                                                      "ü").replace(
        "ae", "ä").replace("oe", "ö")


def removeArticle(string):
    return string.replace("der", "").replace("die", "").replace("das", "").lstrip()


def cleanDataframe(dataframe, not_NaN=True):
    # Filter out NaN Values
    if not_NaN:
        dataframe = dataframe[dataframe[['Geschlecht', 'PLZ', 'Stadt']].notnull().all(1)]

    # Convert Special Characters like ß, ä, ö to the right format
    for index, object in dataframe.iterrows():
        dataframe["Stadt"][index] = convertSpecialChars(object["Stadt"])
        dataframe["Marke"][index] = removeArticle(object["Marke"])
    return dataframe
