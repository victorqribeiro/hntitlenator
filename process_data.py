import re
import json


dict = json.loads( open('words_vector_plus1.json', 'r').read() )

def get_index(word): 
	if word in dict:
		return dict[word]
	dict[word] = max( dict.values() ) + 1
	return dict[word]

x = []
y = []

# how many words have a title?
_max = 0
_avg = 0
_maxScore = 0
_avgScore = 0

categories = ["newstories", "showstories", "topstories", "beststories"]

for cat in categories:

	data = json.loads( open('{}.json'.format(cat), 'r').read() )

	for storie in data:

		_x = [get_index(w.lower()) for w in re.findall(r'\w+', storie['title']) if w.isalpha()]
		len_x = len(_x)

		if len_x > _max:
			_max = len_x
			
		_avg += len_x

		if storie['score'] > _maxScore:
			_maxScore = storie['score']
		_avgScore += storie['score']

		x.append( _x ) 
		if storie['score'] < 70 :
			y.append( [1,0] )
		else:
			y.append( [0,1] )


print( "max: {} \navg: {}".format( _max, _avg/len(x) ) )

print( "Max Score: {} \nAvg Score: {}".format(_maxScore, _avgScore/len(y)) )

# normalize entries to 20 words max, pad with 0
for _x in x:
	delta = 20 - len(_x)
	for i in range(delta):
		_x.append(0)

with open('words_vector_plus1.json', 'w') as f:
	f.write( json.dumps( dict ) )

with open('x.json', 'w') as f:
	f.write( json.dumps( x ) )

with open('y.json', 'w') as f:
	f.write( json.dumps( y ) )
