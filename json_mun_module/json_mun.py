#docker import done
import json
import sys
from collections import OrderedDict

# json型のデータを全探索し、個々の要素に対して何らかの操作をする
def func_json_data(func,json_data,collection_name):
	if type(json_data) == OrderedDict or type(json_data) == dict:
		funced_json = {}
		for k, v in json_data.items():
			funced_json[func(k,collection_name)] = func_json_data(func,v,collection_name)
		return funced_json
	elif type(json_data) == list:
		funced_list = []
		for i, e in enumerate(json_data):
			funced_list.append(func_json_data(func,e,collection_name))
		return funced_list
	else:
		return func(json_data,collection_name)