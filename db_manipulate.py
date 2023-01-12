import json
import sys
from add_encry_module import add_encrypt
from full_encry_module import full_encrypt
import time
from pymongo import MongoClient
import random
import numpy as np

class TestMongo(object):

	def __init__(self):
		self.clint = MongoClient()
		self.db = self.clint['test']

	def add_one(self,json_input,db_name):
		"""データ挿入"""
		post = json_input
		return self.db[db_name].insert_one(post)


def randomfloat(n):
	return random.uniform(0, 10**n)

#jsonデータとコレクション名を受け取りMongoDBにデータを挿入する
def insert_data(json_name,collection_name):

    # jsonファイルの読み出し
	json_file = open(json_name,'r')
	plain_json_data = json.load(json_file)

	add_collection_name = "add_" + collection_name
	full_collection_name = "full_" + collection_name

	#ここからは非同期(要修正)
	#plain_json_dataを暗号化
	add_encrypted_json_data = add_encrypt.add_encrypt_json(plain_json_data,add_collection_name)
	# full_encrypted_json_data = full_encrypt.full_encrypt_json(plain_json_data,full_collection_name)

	# #mongodbに挿入
	# mongodb = TestMongo()
	# mongodb.add_one(full_encrypted_json_data,full_collection_name)
	# del full_encrypted_json_data["_id"]


	return add_encrypted_json_data
	# return full_encrypted_json_data
	

# 検索＋計算
# def caluculate_data(json_name, collection_name):
# 答えの数字を返す

#　要実装
# 該当が一つもない場合は例外処理をするべきか
def caluculate_data(plain_json_data, collection_name):
	# # jsonファイルの読み出し
	# json_file = open(json_name,'r')
	# plain_json_data = json.load(json_file)

	add_collection_name = "add_" + collection_name
	full_collection_name = "full_" + collection_name

	#jsonから検索して計算必要な該当データのみの配列にする
	add_plain_list = plain_json_data
	full_plain_list = plain_json_data

	#計算
	time_sta = time.perf_counter()
	# add_encrypted_sum = add_encrypt.add_caluculate_stdev(add_plain_list, add_collection_name)
	full_encrypted_sum = full_encrypt.full_caluculate_stdev(full_plain_list, full_collection_name)
	time_end = time.perf_counter()

	with open("time.json", "w") as f:
		time_result = {
			"full_encry_time": time_end - time_sta
		}
		json.dump(time_result, f, indent = 4)



	#復号
	# add_plain_sum = add_encrypt.add_decrypt_one(add_encrypted_sum, add_collection_name)
	full_plain_sum = full_encrypt.full_decrypt_one(full_encrypted_sum, full_collection_name)

	return full_plain_sum


# 全てを加法準同型暗号で計算
def caluculate_add_encry(calc_index_list, method, collection_name):
	add_collection_name = "add_" + collection_name

	# jsonファイルの読み出し
	json_file = open("./encrypted_data/add_encrypted_data.json",'r')
	add_encrypted_json_data = json.load(json_file)

	#　今回はadd_encrypted_json_dataにリストが来るとして考える(実際はjson typeで来てその中から該当部分を検索しリスト化する工程が加わる)
	add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]


	# 計算
	if method == "sum":
		add_encrypted_answer = add_encrypt.add_caluculate_sum(add_encrypted_calc_list,add_collection_name)
	elif method == "average":
		add_encrypted_answer = add_encrypt.add_caluculate_average(add_encrypted_calc_list, add_collection_name)
	elif method == "stdev":
		add_encrypted_answer = add_encrypt.add_caluculate_stdev(add_encrypted_calc_list,add_collection_name)
	else:
		print("error")

	# 実際はdecryptはuser側でやるべきだが、簡単のためここで行う
	add_plain_answer = add_encrypt.add_decrypt_one(add_encrypted_answer, add_collection_name)

	return add_plain_answer


# 全てを完全準同型暗号で計算
def caluculate_full_encry(calc_index_list, method, collection_name):
	full_collection_name = "full_" + collection_name

	# jsonファイルの読み出し
	json_file = open("./encrypted_data/full_encrypted_data.json",'r')
	full_encrypted_json_data = json.load(json_file)

	#　今回はfull_encrypted_json_dataにリストが来るとして考える(実際はjson typeで来てその中から該当部分を検索しリスト化する工程が加わる)
	full_encrypted_calc_list = [full_encrypted_json_data[i] for i in calc_index_list]


	# 計算
	if method == "sum":
		full_encrypted_answer = full_encrypt.full_caluculate_sum(full_encrypted_calc_list,full_collection_name)
	elif method == "average":
		full_encrypted_answer = full_encrypt.full_caluculate_average(full_encrypted_calc_list, full_collection_name)
	elif method == "stdev":
		full_encrypted_answer = full_encrypt.full_caluculate_stdev(full_encrypted_calc_list,full_collection_name)
	else:
		pass

	# 実際はdecryptはuser側でやるべきだが、簡単のためここで行う
	full_plain_answer = full_encrypt.full_decrypt_one(full_encrypted_answer, full_collection_name)

	return full_plain_answer



# 加法・完全準同型暗号の両方を用いて計算
# 今回は合計・平均は加法準同型を、分散は完全準同型を用いる
def caluculate_both_encry(calc_index_list, method, collection_name):
	add_collection_name = "add_" + collection_name
	full_collection_name = "full_" + collection_name

	#　計算
	if method == "sum":
		json_file = open("./encrypted_data/add_encrypted_data.json",'r')
		add_encrypted_json_data = json.load(json_file)
		add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = add_encrypt.add_caluculate_sum(add_encrypted_calc_list,add_collection_name)
		plain_answer = add_encrypt.add_decrypt_one(encrypted_answer, add_collection_name)
	elif method == "average":
		json_file = open("./encrypted_data/add_encrypted_data.json",'r')
		add_encrypted_json_data = json.load(json_file)
		add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = add_encrypt.add_caluculate_average(add_encrypted_calc_list,add_collection_name)
		plain_answer = add_encrypt.add_decrypt_one(encrypted_answer, add_collection_name)
	elif method == "stdev":
		json_file = open("./encrypted_data/full_encrypted_data.json",'r')
		full_encrypted_json_data = json.load(json_file)
		full_encrypted_calc_list = [full_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = full_encrypt.full_caluculate_stdev(full_encrypted_calc_list,full_collection_name)
		plain_answer = full_encrypt.full_decrypt_one(encrypted_answer, add_collection_name)

	return plain_answer



def parrallel_distribute_order_do(order_list):
	pass




# 計算命令のみをランダム生成する
def make_calc_order(order_num, first_list_long, collection_name):
	order_list = []
	db_list_long = first_list_long

	# 命令生成
	for i in range(order_num):
		calc_long = random.randint(1,db_list_long)
		calc_index_list = random.sample(range(db_list_long), k=calc_long)
		calc_kind_seed = random.randint(0,2)
		if calc_kind_seed == 0:
			calc_kind = "sum"
		elif calc_kind_seed == 1:
			calc_kind = "average"
		elif calc_kind_seed == 2:
			calc_kind = "stdev"

		order_item = [calc_index_list, calc_kind, collection_name]
		order_list.append(order_item)

		# # 計算の方式は以下の関数を変える
		# calc_answer = caluculate_add_encry(calc_index_list, calc_kind, collection_name)

	return order_list

def make_calc_change_order(order_num, first_list_long, collection_name):
	order_list = []
	db_list_long = first_list_long

	#命令生成
	for i in range(order_num):
		calc_kind_seed = random.randint(0,4)
		if calc_kind_seed == 0:
			calc_kind = "sum"
		elif calc_kind_seed == 1:
			calc_kind = "average"
		elif calc_kind_seed == 2:
			calc_kind = "stdev"
		elif calc_kind_seed == 3:
			calc_kind = "add"
		elif calc_kind_seed == 4:
			calc_kind = "delete"
		
		if calc_kind_seed <= 2:
			# データ計算
			calc_long = random.randint(1,db_list_long)
			calc_index_list = random.sample(range(db_list_long), k=calc_long)
			order_item = [calc_index_list, calc_kind, collection_name]
			order_list.append(order_item)
		elif calc_kind == "add":
			# データ追加
			add_long = random.randint(1, 10)
			add_plain_list =  [np.round(randomfloat(3), decimals=2) for i in range(add_long)]
			order_item = [add_plain_list, calc_kind, collection_name]
			db_list_long += add_long
			order_list.append(order_item)
		elif calc_kind == "delete":
			#データ削除
			delete_long = random.randint(1,10)
			delete_index_list = random.sample(range(db_list_long), k=calc_long)
			order_item = [delete_index_list, calc_kind, collection_name]
			db_list_long -= delete_long
			order_list.append(order_item)		
			
	print(order_list)
	return order_list
		


def main():

	# # insert json
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]

	# time_sta = time.perf_counter()
	# result = insert_data(json_name,collection_name)
	# time_end = time.perf_counter()

	# with open("./encrypted_text.json", "w") as f:
	# 	json.dump(result, f, indent = 4)
	

	# with open("time.json", "w") as f:
	# 	time_result = {
	# 		"add_encry_time": time_end - time_sta
	# 	}
	# 	json.dump(time_result, f, indent = 4)
		

	# #decrypt json
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]
    # # jsonファイルの読み出し
	# json_file = open(json_name,'r')
	# encrypted_json_data = json.load(json_file)	
	# result = add_encrypt.add_decrypt_json(encrypted_json_data,"add_" + collection_name)
	# print(result)


	# #caluculate json
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]

	# result = insert_data(json_name,collection_name)
	# answer = caluculate_data(result, collection_name)
	# print(answer)


	# #one計算only
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]
	# answer = caluculate_both_encry([0,1,2,3], "sum", collection_name)
	# print(answer)

	#複数計算only
	json_name = sys.argv[1]
	collection_name = sys.argv[2]
	make_caluculate_order(100, 100, collection_name)


	#計算+追加・削除




	

if __name__ == '__main__':
    main()



#時間の計測
# time_sta = time.perf_counter()
#(処理)
# time_end = time.perf_counter()

# with open("time.json", "w") as f:
# 	time_result = {
# 		"add_encry_time": time_end - time_sta
# 	}
# 	json.dump(time_result, f, indent = 4)



#実行 第三引数->plainTextFile 第四引数->データベースの名前
#計算テスト
#python db_manipulate.py for_caluculate_plain.json test

#insert テスト
# python db_manipulate.py for_caluculate_plain.json test