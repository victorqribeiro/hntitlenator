import json
import requests
import time

data = []

topstories = requests.get("https://hacker-news.firebaseio.com/v0/showstories.json").json()

for storie in topstories:
	result = requests.get("https://hacker-news.firebaseio.com/v0/item/{}.json".format( storie )).json()
	data.append( result )
	time.sleep(.500)
	
with open('showstories.json','w') as f:
	f.write( json.dumps( data ) )

print data
