import json
from datetime import datetime
import matplotlib.pyplot as plt

dict = json.loads( open('words_vector_plus1.json', 'r').read() )

top  = [ [0 for i in range(24)] for j in range(7) ]

categories = ["newstories", "showstories", "topstories", "beststories"]

for cat in categories:

	data = json.loads( open('{}.json'.format(cat), 'r').read() )
	
	for story in data:
	
		if story['score'] > 70 :
	
			date = datetime.fromtimestamp(story['time'])
		
			top[ date.weekday() ][ date.hour ] += 1
		

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sunday"]

for t, d in zip(top, days):
	plt.plot( t, label=d)
plt.legend()
plt.xlabel("Time 24h")
plt.ylabel("More than 70 upvotes")
plt.yticks([i*2 for i in range(10)])
plt.xticks([i for i in range(24)])
plt.show()
