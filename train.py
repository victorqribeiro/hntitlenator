import json
from Dejavu import Dejavu

words = json.loads( open('words_vector_plus1.json').read() )

def stringToArrayInt(word):
	row = [0] * 20
	for i, l in enumerate(word.split()):
		if l not in words:
			words[l] = len(words.keys())
		row[i] = words[l]
	return row


x = json.loads( open('x.json','r').read() )
y = json.loads( open('y.json','r').read() )



nn = Dejavu( [len(x[0]), 100, 20, len(y[0])] , 0.1, 100 )

for i in range(10):
	nn.fit( x, y, True )
	nn.shuffle( x, y )


nn.save('nn.json')

r1 = nn.predict( stringToArrayInt("we were supposed to be living in pod houses") )[0].tolist()

print( r1 )

