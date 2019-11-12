import numpy as np
np.seterr(over='ignore')

class Dejavu(object) :
	
	def __init__(self, nn=[0], learningRate = 0.1, iterations = 100) :

		self.layers = {'length': 0}
		
		for i in range(len(nn)-1) :
			self.layers[i] = {}
			self.layers[i]['weights'] = np.random.uniform(low=-1.0, high=1.0, size=(nn[i+1],nn[i]))
			self.layers[i]['bias'] = np.random.uniform(low=-1.0, high=1.0, size=(nn[i+1],1))
			self.layers[i]['activation'] = 'tanh'
			self.layers['length'] += 1

		self.lr = learningRate
		
		self.it = iterations
		
		self.sigmoid = lambda x : 1.0 / ( 1.0 + np.exp(-x) )
				
		self.dSigmoid = lambda x : x * (1.0 - x)
		
		self.tanh = lambda x : np.tanh(x)
		
		self.dTanh = lambda x : 1.0 - (x * x)
		
		self.relu = lambda x : x if x > 0 else 0.0
		
		self.dRelu = lambda x: 1.0 if x > 0 else 0.0
		
		self.err_sqr = lambda x : x ** 2


	def predict(self, inputs) :

		output = np.array( inputs ).reshape(len(inputs),1)
		
		for i in range( self.layers['length'] ) :
		
			output = np.matmul( self.layers[i]['weights'], output )
			output = np.add( output, self.layers[i]['bias'] )
			#act = np.vectorize( self.tanh )
			#output = act( output )
			output = self.sigmoid( output )
			self.layers[i]['output'] = output
		
		return np.transpose(output)
		
	
	def fit(self, inputs, labels, verbose = False) :
		it = 0
		while it < self.it :
			s = 0.0
			for i in range(len(inputs)) :
			
				output_error = np.array( labels[i] ).reshape(len(labels[i]),1)
			
				inputsMatrix = np.array( inputs[i] ).reshape(len(inputs[i]),1)
		
				self.predict( inputsMatrix )
				
				output_error = np.subtract( output_error, self.layers[ self.layers['length']-1]['output'] )
				
				s += np.sum( self.err_sqr(output_error) ) #/ self.layers[ self.layers['length']-1 ]['output'].shape[0]
				
				for i in range(self.layers['length']-1, -1, -1) :

					gradient = self.layers[i]['output'].copy()
					#act = np.vectorize( self.dTanh )
					#gradient = act( gradient )
					gradient = self.dSigmoid( gradient )
					gradient = np.multiply( gradient, output_error )
					gradient *= self.lr
					
					layer = self.layers[i-1]['output'].copy() if i != 0 else inputsMatrix

					delta = np.matmul( gradient, layer.T )
					
					self.layers[i]['weights'] = np.add( self.layers[i]['weights'], delta )
					self.layers[i]['bias'] = np.add( self.layers[i]['bias'], gradient )
					
					error = self.layers[i]['weights'].copy()
					output_error = np.matmul( error.T, output_error )
				
			it += 1
			if verbose :
				print( '{0} - {1}'.format(it,s) )

	def shuffle(self, x, y):
		_max = len(x)
		for i in range(_max):
			r1 = np.random.randint(low=0, high=_max-1)
			r2 = np.random.randint(low=0, high=_max-1)
			if r1 == r2:
				continue
			tmp_x = x[r1]
			tmp_y = y[r1]
			x[r1] = x[r2]
			y[r1] = y[r2]
			x[r2] = tmp_x
			y[r2] = tmp_y
			
				
	def save(self, namefile = 'nn.json') :
		import json

		nn = { 
			'layers': {'length': 0},
			'lr': self.lr,
			'it': self.it
		}

		for i in range(self.layers['length']) :
			nn['layers'][i] = {}
			nn['layers'][i]['weights'] = {
				'rows': self.layers[i]['weights'].shape[0],
				'cols': self.layers[i]['weights'].shape[1],
				'data': self.layers[i]['weights'].reshape(-1).tolist()
			}
			nn['layers'][i]['bias'] = {
				'rows': self.layers[i]['bias'].shape[0],
				'cols': self.layers[i]['bias'].shape[1],
				'data': self.layers[i]['bias'].reshape(-1).tolist()
			}
			nn['layers'][i]['output'] = {
				'rows': self.layers[i]['output'].shape[0],
				'cols': self.layers[i]['output'].shape[1],
				'data': self.layers[i]['output'].reshape(-1).tolist()
			}
			nn['layers'][i]['activation'] = self.layers[i]['activation']
			nn['layers']['length'] += 1

		with open(namefile, 'w') as fp:
			json.dump(nn, fp)
			

	def load(self, data) :

		self.layers = {'length': 0}

		for i in range(data['layers']['length']) :
			key = str(i)
			self.layers[i] = {}
			self.layers[i]['weights'] = (np.array(data['layers'][key]['weights']['data'])
														.reshape(data['layers'][key]['weights']['rows'], data['layers'][key]['weights']['cols']))
			self.layers[i]['bias'] = (np.array(data['layers'][key]['bias']['data'])
														.reshape(data['layers'][key]['bias']['rows'], data['layers'][key]['bias']['cols']))
			self.layers[i]['output'] = (np.array(data['layers'][key]['output']['data'])
														.reshape(data['layers'][key]['output']['rows'], data['layers'][key]['output']['cols']))
			self.layers[i]['activation'] = data['layers'][key]['activation']
			self.layers['length'] += 1
		
		self.lr = data['lr']
		
		self.it = data['it']
