import json
from os import listdir, path

DIRS = [
	'./forms',
	'./calibrations'
]

for d in DIRS:
	for name in listdir(d):
		try:
			with open(path.join(d, name), 'r') as in_file:
				c = json.load(in_file)
			with open(path.join(d, name), 'w') as out_file:
				json.dump(c, out_file, indent='\t')
		except:
			print('Error with {}/{}'.format(d, name))
