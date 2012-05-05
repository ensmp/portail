'''prend en entrée un fichier avec des lignes copiées de la page de cours SGS,
une ligne sur deux avec code + description, l'autre avec ECTS et catégorie'''

import sys
import json

if __name__ == '__main__':
	f = open(sys.argv[1])
	lines = f.readlines()
	lines = [lines[i].strip() for i in range(len(lines)) if i % 2 == 0]
	out = []
	for l in lines:
		i = l.find(':')
		out.append({'code': l[:i], 'description': l[(i+2):], 'year': 3})

	print json.dumps(out)
