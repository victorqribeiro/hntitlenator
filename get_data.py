import json
import requests
import time

data = []

categories = ["newstories", "showstories", "topstories", "beststories"]

for category in categories:

	stories_ids = requests.get("https://hacker-news.firebaseio.com/v0/{}.json".format(category)).json()

	for storie in stories_ids:
		result = requests.get("https://hacker-news.firebaseio.com/v0/item/{}.json".format(storie)).json()
		data.append( result )
		time.sleep(.5)
		
	with open('{}.json'.format(category), 'w') as f:
		f.write( json.dumps( data ) )

	print("{} done!".format(category))
