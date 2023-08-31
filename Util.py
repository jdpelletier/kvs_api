import requests
import json
import config
from datetime import datetime, timezone

def coordConvert(long, lat):
    if long is None or lat is None:
        return "Disconnected"
    coordinates = config.coordinates
    for key in coordinates:
        if coordinates[key][0] >= long >= coordinates[key][2] and coordinates[key][1] >= lat >= coordinates[key][3]:
            if "Saddle, Waimea Side" in key:
                key = "Saddle, Waimea Side"
            return key
    return f"{long}, {lat}"
    
def timeConvert(in_time):
    time = ' '.join(in_time.split('T')).replace("Z","")
    if len(time) < 17:
       timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M')
       timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None)
       timestamp = timestamp.strftime('%m-%d-%Y  %H:%M')
    else:
        try:
            timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None)
        timestamp = timestamp.strftime('%m-%d-%Y %H:%M:%S')
    return timestamp

def getVehicles():
    URL = config.token_url
    user = config.email
    password = config.password
    userId = config.userid
    PARAMS = {"username":user, "password":password}
    r = requests.post(url = URL, params = PARAMS)
    data = r.json()
    token = data['access_token']
    token = f'Bearer {token}'
    URL = config.graphql_url
    HEADERS = {'Authorization': token, 'userId': userId, 'Content-Type': 'application/json'}
    body = """
    {
    getVehicles {
        name
        lastData {
            timestamp
            gps{
                latitude
                longitude
            }
        }
    }
    }
    """
    
    r = requests.post(url=URL, headers = HEADERS, json={"query": body})

    data = r.json()
    data = data["data"]["getVehicles"]
    formatted_list = []
    for car in data:
        name = car["name"]
        formatted_car = {}
        formatted_car["Vehicle"] = name
        if car["lastData"] is None:
          formatted_car["Location"] = "Disconected"
          formatted_car["Last Timestamp"] = "Disconected"
        else:
            location = coordConvert(car["lastData"]["gps"]["longitude"], car["lastData"]["gps"]["latitude"])
            formatted_car["Vehicle"] = name
            formatted_car["Location"] = location
            formatted_car["Last Timestamp"] = timeConvert(car["lastData"]["timestamp"])
        formatted_list.append(formatted_car)
    return(json.dumps(sorted(formatted_list, key=lambda x: int(x['Vehicle'][2:4]), reverse=True)))
