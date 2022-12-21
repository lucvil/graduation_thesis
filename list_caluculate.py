import json
import sys
import time
import statistics
import math


json_name = "for_caluculate_plain.json"
json_file = open(json_name,'r')
plain_json_data = json.load(json_file)

print("合計", sum(plain_json_data))
print("平均", statistics.mean(plain_json_data))
print("分散", statistics.pvariance(plain_json_data))

