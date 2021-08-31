import pandas as pd

modelMap = {'Mercedes': {'C-Klasse': {},
                         'E-Klasse': {},
                         'M-Klasse': {},
                         'A-Klasse': {},
                         'G-Klasse': {}
                         },
            'Audi': {'A4': {},
                     'A6': {},
                     'A3': {},
                     'S3': {},
                     'Q5': {},
                     'A1': {},
                     'A5': {},
                     'Q7': {},
                     'SQ5': {}
                     },
            'Porsche': {'Cayenne': {},
                        'Panamera': {},
                        '911': {},
                        'Boxster': {}
                        },
            'Tesla': {'Model S': {}},
            'Volvo': {'S60': {}},
            'Volkswagen': {'Passat': {},
                           'Passat CC': {},
                           'Touareg': {},
                           'Tiguan': {},
                           'Golf': {},
                           'Beetle': {},
                           'Golf Sportsvan': {},
                           'Polo': {},
                           'Passat Variant': {},
                           'Golf GTI': {},
                           'Golf Variant': {}
                           },
            'Mazda': {'6': {},
                      'CX-5': {},
                      '3': {}
                      },
            'Opel': {'Insignia': {},
                     'Corsa': {},
                     'Astra': {},
                     'Cascada': {}
                    },
            'Skoda': {'Superb': {},
                      'Octavia': {},
                      'Fabia': {},
                      'Yeti': {}
                      },
            'Ford': {'Mondeo': {},
                     'Kuga': {},
                     'Focus': {},
                     'Fiesta': {}
                     },
            'Kia': {'Optima': {},
                    'Sportage': {}
                    },
            'Nissan': {'370Z': {}},
            'Honda': {'CR-V': {},
                      'Civic': {},
                      'Jazz': {}
                      },
            'Renault': {'Koleos': {},
                        'Clio': {}
                        },
            'Hyundai': {'i20': {},
                        'i30': {}
                        },
            'Toyota': {'Auris': {},
                       'Yaris': {}
                       },
            'Suzuki': {'Grand Vitara': {}},
            'BMW': {'316': {},
                    '116': {},
                    'X5': {},
                    '118': {},
                    '520': {},
                    'X3': {},
                    'X1': {},
                    '523': {},
                    '320': {},
                    '535': {},
                    '135': {},
                    '530': {},
                    '114': {},
                    '335': {},
                    '325': {},
                    '525': {},
                    '318': {},
                    '330': {}
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
