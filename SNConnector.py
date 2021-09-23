# Requests Initials
import json

import requests

user = 'car.picker'
pwd = 'genericai'
headers = {"Content-Type": "application/json", "Accept": "application/json"}

def sendPredictionToInstance(table, userID, prediction):
    sysId = getSurvey(userID)
    url = "https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/" + table + "/" + sysId
    requests.put(url, auth=(user, pwd), headers=headers, data='{\"mobility\": \"' + prediction + '\"}')

def getSurvey(userID):
    # Retrieves the Controller SysID from the ServiceNow Instance
    # Set the request parameters
    url = 'https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/x_ntt47_genericcar_survey_result?sysparm_query=user='+userID
    # GET Request with the defined Parameters
    response = requests.get(url, auth=(user, pwd), headers=headers)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print("Success!")

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    # Returns the SysID from the retrieved Data
    return data["result"][0]["sys_id"]

def getAIServer():
    # Retrieves the Controller SysID from the ServiceNow Instance
    # Set the request parameters
    url = 'https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/x_ntt47_genericcar_ai_server'
    params = {"name": "CarPicker AI Server"}
    # GET Request with the defined Parameters
    response = requests.get(url, auth=(user, pwd), headers=headers, json=params)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print("Success!")

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    # Returns the SysID from the retrieved Data
    return data["result"][0]["sys_id"]

# Sends a PUT Request to the ServiceNow Instance and updates the IP of the Controller Record
def updateIP(table, ip, sysId):
    url = "https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/"+table+"/"+sysId
    requests.put(url, auth=(user, pwd),  headers=headers, data='{\"ip_address\": \"'+ip+'\"}')

# Retrieves the Controller SysID from the ServiceNow Instance
def getCars():
    # Set the request parameters
    mobilityUrl = 'https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/x_ntt47_daimlerpoc_daimler_mobility'

    # GET Request with the defined Parameters
    response = requests.get(mobilityUrl, auth=(user, pwd), headers=headers)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print("Success!")

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    # Returns the SysID from the retrieved Data
    return data["result"]


def getQuery(list):
    query = ""
    for x in list:
        query += "sys_id=" + x + "^OR"
    query = query[:-3]
    return query
