import json
import sys
from add_encry_module import add_encrypt
from full_encry_module import full_encrypt
import time
from pymongo import MongoClient
import random
import numpy as np

#並列処理
from multiprocessing import Process, Value
import multiprocessing
import threading

class TestMongo(object):

	def __init__(self):
		self.clint = MongoClient()
		self.db = self.clint['test']

	def add_one(self,json_input,db_name):
		"""データ挿入"""
		post = json_input
		return self.db[db_name].insert_one(post)


def randomfloat(n):
	#小数点代何位までにするか
	answer_decimals = 2
	answer = random.uniform(0, 10**n)
	#小数点第2位以下で四捨五入
	answer = float(np.round(answer, decimals=answer_decimals))
	return answer

#jsonデータとコレクション名を受け取りMongoDBにデータを挿入する
def insert_data(json_name,collection_name):

    # jsonファイルの読み出し
	json_file = open(json_name,'r')
	plain_json_data = json.load(json_file)

	add_collection_name = "add_" + collection_name
	full_collection_name = "full_" + collection_name

	#ここからは非同期(要修正)
	#plain_json_dataを暗号化
	# add_encrypted_json_data = add_encrypt.add_encrypt_json(plain_json_data,add_collection_name)
	full_encrypted_json_data = full_encrypt.full_encrypt_json(plain_json_data,full_collection_name)

	# #mongodbに挿入
	# mongodb = TestMongo()
	# mongodb.add_one(full_encrypted_json_data,full_collection_name)
	# del full_encrypted_json_data["_id"]


	# return add_encrypted_json_data
	return full_encrypted_json_data


def add_insert_encrypted_data(plain_json_name, encrypted_json_name):
	plain_json_file = open(plain_json_name, 'r')
	plain_json_data = json.load(plain_json_file)

	add_collection_name = "add_test"

	# 暗号化
	encrypted_json_data = add_encrypt.add_encrypt_json(plain_json_data,add_collection_name)

	# ファイルに書き込み
	with open(encrypted_json_name, "w+") as f:
		json.dump(encrypted_json_data, f, indent = 4)

	return encrypted_json_data


def full_insert_encrypted_data(plain_json_name, encrypted_json_name):
	plain_json_file = open(plain_json_name, 'r')
	plain_json_data = json.load(plain_json_file)

	full_collection_name = "full_test"

	# 暗号化
	encrypted_json_data = full_encrypt.full_encrypt_json(plain_json_data,full_collection_name)

	# ファイルに書き込み
	with open(encrypted_json_name, "w+") as f:
		json.dump(encrypted_json_data, f, indent = 4)

	return encrypted_json_data

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
def calc_change_add_encry(calc_index_list, method, collection_name):
	add_collection_name = "add_" + collection_name
	db_file_place = "./encrypted_data/add_encry_exp copy.json"

	# jsonファイルの読み出し
	json_file = open(db_file_place,'r')
	add_encrypted_json_data = json.load(json_file)

	#　今回はadd_encrypted_json_dataにリストが来るとして考える(実際はjson typeで来てその中から該当部分を検索しリスト化する工程が加わる)
	if method != "add" and method != "delete":
		add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]


	# 計算
	if method == "sum":
		add_encrypted_answer = add_encrypt.add_caluculate_sum(add_encrypted_calc_list,add_collection_name)
	elif method == "average":
		add_encrypted_answer = add_encrypt.add_caluculate_average(add_encrypted_calc_list, add_collection_name)
	elif method == "stdev":
		add_encrypted_answer = add_encrypt.add_caluculate_stdev(add_encrypted_calc_list,add_collection_name)
	elif method == "add":
		add_encrypted_json_data.extend(add_encrypt.add_encrypt_json(calc_index_list, add_collection_name))
		with open(db_file_place, "w") as f:
			json.dump(add_encrypted_json_data, f, indent = 4)
	elif method == "delete":
		add_encrypted_deleted_json_data = [add_encrypted_json_data[i] for i in range(len(add_encrypted_json_data)) if i not in calc_index_list]

		with open(db_file_place, "w") as f:
			json.dump(add_encrypted_deleted_json_data, f, indent = 4)		
	else:
		print("error")

	# 実際はdecryptはuser側でやるべきだが、簡単のためここで行う
	add_plain_answer = -1
	if method != "add" and method != "delete":
		add_plain_answer = add_encrypt.add_decrypt_one(add_encrypted_answer, add_collection_name)


	return add_plain_answer


# 全てを完全準同型暗号で計算
def calc_change_full_encry(calc_index_list, method, collection_name):
	full_collection_name = "full_" + collection_name
	db_file_place = "./encrypted_data/full_encry_exp copy.json"

	# jsonファイルの読み出し
	json_file = open(db_file_place,'r')
	full_encrypted_json_data = json.load(json_file)

	#　今回はfull_encrypted_json_dataにリストが来るとして考える(実際はjson typeで来てその中から該当部分を検索しリスト化する工程が加わる)
	if method != "add" and method != "delete":
		full_encrypted_calc_list = [full_encrypted_json_data[i] for i in calc_index_list]


	# 計算
	if method == "sum":
		full_encrypted_answer = full_encrypt.full_caluculate_sum(full_encrypted_calc_list,full_collection_name)
	elif method == "average":
		full_encrypted_answer = full_encrypt.full_caluculate_average(full_encrypted_calc_list, full_collection_name)
	elif method == "stdev":
		full_encrypted_answer = full_encrypt.full_caluculate_stdev(full_encrypted_calc_list,full_collection_name)
	elif method == "add":
		full_encrypted_json_data.extend(full_encrypt.full_encrypt_json(calc_index_list, full_collection_name))
		with open(db_file_place, "w") as f:
			json.dump(full_encrypted_json_data, f, indent = 4)
	elif method == "delete":
		full_encrypted_deleted_json_data = [full_encrypted_json_data[i] for i in range(len(full_encrypted_json_data)) if i not in calc_index_list]
		with open(db_file_place, "w") as f:
			json.dump(full_encrypted_deleted_json_data, f, indent = 4)			
	else:
		pass

	# 実際はdecryptはuser側でやるべきだが、簡単のためここで行う
	full_plain_answer = -1
	if method != "add" and method != "delete":
		full_plain_answer = full_encrypt.full_decrypt_one(full_encrypted_answer, full_collection_name)

	return full_plain_answer


# 加法・完全準同型暗号の両方を用いて計算
# 今回は合計・平均は加法準同型を、分散は完全準同型を用いる
def caluculate_both_encry(calc_index_list, method, collection_name):
	add_collection_name = "add_" + collection_name
	full_collection_name = "full_" + collection_name
	add_db_file_place = "./encrypted_data/add_encry_exp copy.json"
	full_db_file_place = "./encrypted_data/full_encry_exp copy.json"

	#　計算
	if method == "sum":
		json_file = open(add_db_file_place,'r')
		add_encrypted_json_data = json.load(json_file)
		add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = add_encrypt.add_caluculate_sum(add_encrypted_calc_list,add_collection_name)
		plain_answer = add_encrypt.add_decrypt_one(encrypted_answer, add_collection_name)
	elif method == "average":
		json_file = open(add_db_file_place,'r')
		add_encrypted_json_data = json.load(json_file)
		add_encrypted_calc_list = [add_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = add_encrypt.add_caluculate_average(add_encrypted_calc_list,add_collection_name)
		plain_answer = add_encrypt.add_decrypt_one(encrypted_answer, add_collection_name)
	elif method == "stdev":
		json_file = open(full_db_file_place,'r')
		full_encrypted_json_data = json.load(json_file)
		full_encrypted_calc_list = [full_encrypted_json_data[i] for i in calc_index_list]
		encrypted_answer = full_encrypt.full_caluculate_stdev(full_encrypted_calc_list,full_collection_name)
		plain_answer = full_encrypt.full_decrypt_one(encrypted_answer, add_collection_name)
	elif method == "add":
		add_json_file = open(add_db_file_place,'r')
		add_encrypted_json_data = json.load(add_json_file)
		add_encrypted_json_data.extend(add_encrypt.add_encrypt_json(calc_index_list, add_collection_name))
		with open(add_db_file_place, "w") as f:
			json.dump(full_encrypted_json_data, f, indent = 4)

		full_json_file = open(full_db_file_place,'r')
		full_encrypted_json_data = json.load(full_json_file)
		full_encrypted_json_data.extend(full_encrypt.full_encrypt_json(calc_index_list, full_collection_name))
		with open(full_db_file_place, "w") as f:
			json.dump(full_encrypted_json_data, f, indent = 4)
		plain_answer = -1
	elif method == "delete":
		add_json_file = open(add_db_file_place,'r')
		add_encrypted_json_data = json.load(add_json_file)
		add_encrypted_deleted_json_data = [add_encrypted_json_data[i] for i in range(len(add_encrypted_json_data)) if i not in calc_index_list]
		with open(add_db_file_place, "w") as f:
			json.dump(add_encrypted_deleted_json_data, f, indent = 4)

		full_json_file = open(full_db_file_place,'r')
		full_encrypted_json_data = json.load(full_json_file)
		full_encrypted_deleted_json_data = [full_encrypted_json_data[i] for i in range(len(full_encrypted_json_data)) if i not in calc_index_list]
		with open(full_db_file_place, "w") as f:
			json.dump(full_encrypted_deleted_json_data, f, indent = 4)	
		plain_answer = -1			
	

	return plain_answer


# order_listに従って上記の三つにデータを流す
def do_order_list_add_or_full(calc_func, order_list, multiprocess_result_list):
	for order_list_item in order_list:
		answer_item = calc_func(order_list_item[0], order_list_item[1], order_list_item[2])
		multiprocess_result_list.append([answer_item, order_list_item[3]])
	
	return 1


# 命令を加法と完全に振り分け並列処理する
def parallel_distribute_order_do_add_full(order_list):

	#命令振り分け
	add_order_list = []
	full_order_list = []
	for order_item in order_list:
		if order_item[1] == "sum" or order_item[1] == "average":
			add_order_list.append(order_item)
		elif order_item[1] == "stdev":
			full_order_list.append(order_item)
		elif order_item[1] == "add" or order_item[1] == "delete":
			add_order_list.append(order_item)
			full_order_list.append(order_item)
	
	# add と fullで並列処理
	#async, threadingm, multiprocessing の三種類があるが、今回は並列処理のmultiprocessingを用いる
	manager = multiprocessing.Manager()
	multiprocess_result_list = manager.list()
	add_process = Process(target=do_order_list_add_or_full, args=(calc_change_add_encry, add_order_list,multiprocess_result_list,))
	full_process = Process(target=do_order_list_add_or_full, args=(calc_change_full_encry, full_order_list,multiprocess_result_list,))
	add_process.start()
	full_process.start()
	add_process.join()
	full_process.join()

	print(multiprocess_result_list)
	return multiprocess_result_list



#order_listに従って上記の完全準同型にデータを流す
def do_order_list_full_only(calc_func, order_list, multiprocess_result_list, multiprocess_change_stage):
	for order_list_item in order_list:
		# 要追加実装
		if order_list_item[1] == "add" or order_list_item[1] == "delete":
			while multiprocess_change_stage.value != int(order_list_item[4]) - 0.5:
				pass 
			answer_item = calc_func(order_list_item[0], order_list_item[1], order_list_item[2])
			multiprocess_result_list.append([answer_item, order_list_item[3]])
			multiprocess_change_stage.value = order_list_item[4]
		else:
			while multiprocess_change_stage.value != int(order_list_item[4]) and multiprocess_change_stage.value != int(order_list_item[4]) + 0.5:
				pass
			answer_item = calc_func(order_list_item[0], order_list_item[1], order_list_item[2])
			multiprocess_result_list.append([answer_item, order_list_item[3]])
			if multiprocess_change_stage.value < order_list_item[4]:
				multiprocess_change_stage.value = order_list_item[4]			

	return 1


#　並列処理＋完全準同型のみ
def parallel_distribute_order_do_full_only(order_list):

	#命令振り分け
	full_order_list_1 = []
	full_order_list_2 = []
	for item_num in range(len(order_list)):
		if item_num % 2 == 0:
			full_order_list_1.append(order_list[item_num])
		else:
			full_order_list_2.append(order_list[item_num])

	print(order_list)

	# #fullのみで
	manager = multiprocessing.Manager()
	multiprocess_result_list = manager.list()
	if order_list[0][1] == "add" or order_list[0][1] == "delete":
		change_stage = Value("d", 0.5)
	else:
		change_stage = Value("d", 0.0)
	full_process_1 = Process(target=do_order_list_full_only, args=(calc_change_full_encry, full_order_list_1,multiprocess_result_list, change_stage,))
	full_process_2 = Process(target=do_order_list_full_only, args=(calc_change_full_encry, full_order_list_2,multiprocess_result_list, change_stage,))
	# 続き
	full_process_1.start()
	full_process_2.start()
	full_process_1.join()
	full_process_2.join()

	print(multiprocess_result_list)
	return multiprocess_result_list



# 計算命令のみをランダム生成する
def make_calc_order(order_num, first_list_long, collection_name):
	order_list = []
	db_list_long = first_list_long
	change_stage = 0
	# 命令生成
	for i in range(order_num):
		calc_long = random.randint(1,db_list_long)
		calc_index_list = random.sample(range(db_list_long), k=calc_long)
		calc_kind = np.random.choice(["sum", "average", "stdev"], p=[0.33, 0.33, 0.34])

		order_item = [calc_index_list, calc_kind, collection_name, i, change_stage]
		order_list.append(order_item)

	return order_list


# 計算命令とデータの作成・削除命令をランダム生成する
def make_calc_change_order(order_num, first_list_long, collection_name):
	order_list = []
	db_list_long = first_list_long
	change_stage = 0

	#命令生成
	for i in range(order_num):
		calc_kind_seed = random.randint(0,4)
		calc_kind = np.random.choice(["sum", "average", "stdev", "add", "delete"], p=[0.2, 0.2, 0.2, 0.2, 0.2])
		
		if calc_kind == "sum" or calc_kind == "average" or calc_kind == "stdev":
			# データ計算
			calc_long = random.randint(1,db_list_long)
			calc_index_list = random.sample(range(db_list_long), k=calc_long)
			order_item = [calc_index_list, calc_kind, collection_name, i, change_stage]
			order_list.append(order_item)
		elif calc_kind == "add":
			# データ追加
			add_long = random.randint(1, 10)
			# float型の要素を持つlistに直す
			add_plain_list =  [randomfloat(3) for i in range(add_long)]
			change_stage += 1
			order_item = [add_plain_list, calc_kind, collection_name, i, change_stage]
			db_list_long += add_long
			order_list.append(order_item)
			if len(order_list) >= 2:
				order_list[-2][4] += 0.5
		elif calc_kind == "delete":
			#データ削除
			delete_long = random.randint(1,10)
			delete_index_list = random.sample(range(db_list_long), k=delete_long)
			change_stage += 1
			order_item = [delete_index_list, calc_kind, collection_name, i, change_stage]
			db_list_long -= delete_long
			order_list.append(order_item)
			if len(order_list) >= 2:
				order_list[-2][4] += 0.5

			
	print(order_list)
	return order_list


# order[計算list or 追加リスト、　操作内容、　collection_name、　命令番号、　変更ステージ]

		


# 暗号化テスト
def encry_test(encrypt_method):
	record = {}
	record["title"] = encrypt_method + "_encryption"

	##record_josn_nameを毎回変えること
	record_json_name = "./record/encry/" + encrypt_method + "_encry/" + encrypt_method + "_encry_record.json"

	encrypt_method = "add"
	plain_json_folder = ["3.2", "5.2", "7.2", "9.2"]
	plain_json_count = ["10", "20", "40", "60", "100"]
	exp_count_config = 3
	for exp_count in range(exp_count_config):
		if exp_count == 0:
			record[encrypt_method] = {}
		for plain_json_folder_item in plain_json_folder:
			if exp_count == 0:
				record[encrypt_method][plain_json_folder_item] = {}
			for plain_json_count_item in plain_json_count:
				if exp_count == 0:
					record[encrypt_method][plain_json_folder_item][plain_json_count_item] = {}
				for sample_no in range(1,4):
					#record等の設定
					if exp_count == 0:
						record[encrypt_method][plain_json_folder_item][plain_json_count_item][str(sample_no)] = []
					plain_json_name = "./plain_data/" + plain_json_folder_item + "/" + plain_json_count_item + "p_" + plain_json_folder_item + "_" + str(sample_no) + ".json"
					encrypted_json_name = "./encrypted_data/" + encrypt_method+ "_encry/" + plain_json_folder_item + "/" + plain_json_count_item + "p_" + plain_json_folder_item + "_" + str(sample_no) + ".json"

					# ファイルを空白に戻す
					white_data = []
					with open(encrypted_json_name, "w") as f:
						json.dump(white_data, f, indent = 4)

					# 時間を計測
					time_sta = time.perf_counter()
					add_insert_encrypted_data(plain_json_name, encrypted_json_name)
					time_end = time.perf_counter()
					elapsed_time = time_end - time_sta
					record["add"][plain_json_folder_item][plain_json_count_item][str(sample_no)].append(elapsed_time)

					with open(record_json_name, "w") as f:
						json.dump(record, f, indent = 4)



def main():

	# # insert json old
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]

	# time_sta = time.perf_counter()
	# result = insert_data(json_name,collection_name)
	# time_end = time.perf_counter()

	# with open("./encrypted_text.json", "w") as f:
	# 	json.dump(result, f, indent = 4)


	# JSONの暗号化＋書き込み
	encry_test("add")
				

	

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

	# #複数計算only
	# json_name = sys.argv[1]
	# collection_name = sys.argv[2]
	# order_list = make_calc_change_order(100,100, collection_name)
	# parallel_distribute_order_do_add_full(order_list)
	


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