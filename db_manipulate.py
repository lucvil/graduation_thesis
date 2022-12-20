import json
import sys
from add_encry_module import add_encrypt
from full_encry_module import full_encrypt
import time
from pymongo import MongoClient

class TestMongo(object):

	def __init__(self):
		self.clint = MongoClient()
		self.db = self.clint['test']

	def add_one(self,json_input,db_name):
		"""データ挿入"""
		post = json_input
		return self.db[db_name].insert_one(post)


#jsonデータとコレクション名を受け取りMongoDBにデータを挿入する
def insert_data(json_name,collection_name):

    # jsonファイルの読み出し
	json_file = open(json_name,'r')
	plain_json_data = json.load(json_file)

	add_collection_name = "add_" + collection_name
	mul_collection_name = "mul_" + collection_name
	full_collection_name = "full_" + collection_name

	#ここからは非同期(要修正)
	#plain_json_dataを暗号化
	add_encrypted_json_data = add_encrypt.add_encrypt_json(plain_json_data,add_collection_name)
	# mul_encrypted_json_data = mul_encrypt_json(plain_json_data,mul_collection_name)
	# full_encrypted_json_data = full_encrypt.full_encrypt_json(plain_json_data,full_collection_name)

	# #mongodbに挿入
	# mongodb = TestMongo()
	# mongodb.add_one(full_encrypted_json_data,full_collection_name)
	# del full_encrypted_json_data["_id"]



	return add_encrypted_json_data




def main():

	# insert json
	json_name = sys.argv[1]
	collection_name = sys.argv[2]

	time_sta = time.perf_counter()
	result = insert_data(json_name,collection_name)
	with open("./encrypted_text.json", "w") as f:
		json.dump(result, f, indent = 4)
	time_end = time.perf_counter()

	with open("time.json", "w") as f:
		time_result = {
			"add_encry_time": time_end - time_sta
		}
		json.dump(time_result, f, indent = 4)
		

	# #decrypt json
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]
    # # jsonファイルの読み出し
	# json_file = open(json_name,'r')
	# encrypted_json_data = json.load(json_file)	
	# result = add_encrypt.add_decrypt_json(encrypted_json_data,"add_" + collection_name)
	# print(result)

if __name__ == '__main__':
    main()

#実行 第三引数->plainTextFile 第四引数->データベースの名前
#python db_manipulate.py new_confirm_copy.json test