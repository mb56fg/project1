import requests, json

#key     = "83984f460e3af01fb87fb1becd5a51a8"
#string  = "https://api.darksky.net/forecast/" + key + "/42.37,-71.11"

#weather = requests.get(string).json()
#print(string)

#y = weather["currently"]["dewPoint"]

#print(y)

#print(weather["currently"])


#print(json.dumps(y, indent = 2))

string  = "http://ide50-harrelblatt.cs50.io:8080/api/02446"

taco = requests.get(string)