import json
from Dejavu import Dejavu


x = json.loads( open('x.json','r').read() )
y = json.loads( open('y.json','r').read() )



nn = Dejavu( [len(x[0]), 50, 25, len(y[0])] , 0.1, 100 )

data = json.loads( open('nn.json').read() )

nn.load( data )

for i in range(10):
	nn.fit( x, y, True )
	nn.shuffle( x, y )


nn.save('nn.json')



