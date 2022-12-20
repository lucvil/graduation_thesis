import json
import random
import string
import numpy as np

def randomname(n):
	randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
	return ''.join(randlst)

def randomfloat(n):
	return random.uniform(0, 10**n)

str_json = {}

for i in range(1):
	key = randomname(20)
	value = np.round(randomfloat(7), decimals=3)
	str_json[key] = value


f = open('plain_text.json', 'w')
json.dump(str_json, f, ensure_ascii=False, indent=4, separators=(',', ': '))