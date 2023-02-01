import json
import random
import string
import numpy as np

def randomfloat(n):
	return random.uniform(0, 10**n)


sample_count = [500]
sample_digit = [3,7,9]
for sample_digit_item in sample_digit:
    for sample_count_item in sample_count:
        for j in range(3):
            result = []
            for i in range(sample_count_item):
                list_item = np.round(randomfloat(sample_digit_item), decimals=2)
                result.append(list_item)

            f = open('./data/plain_data/'+str(sample_digit_item)+'.2/'+str(sample_count_item)+'p_'+str(sample_digit_item)+'.2_'+str(j+1)+'.json', 'w+')
            json.dump(result, f, ensure_ascii=False, indent=4, separators=(',', ': '))