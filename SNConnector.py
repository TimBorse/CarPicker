# Requests Initials
import requests

user = 'car.picker'
pwd = 'genericai'
headers = {"Content-Type": "application/json", "Accept": "application/json"}

# Retrieves the Controller SysID from the ServiceNow Instance
def getCars():
    # Set the request parameters
    mobilityUrl = 'https://nttdatadeutschlandgmbhdemo4.service-now.com/api/now/v1/table/x_ntt47_daimlerpoc_mobilitytable'

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
