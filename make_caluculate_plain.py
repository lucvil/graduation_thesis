import json
import random
import string
import numpy as np

def randomfloat(n):
	return random.uniform(0, 10**n)

result = []
for i in range(100):
    list_item = np.round(randomfloat(3), decimals=2)
    result.append(list_item)

f = open('for_caluculate_plain.json', 'w')
json.dump(result, f, ensure_ascii=False, indent=4, separators=(',', ': '))