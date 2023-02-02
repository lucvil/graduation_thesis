import random
import numpy as np
import json


def randomfloat(n):
	#小数点代何位までにするか
	answer_decimals = 2
	answer = random.uniform(0, 10**n)
	#小数点第2位以下で四捨五入
	answer = float(np.round(answer, decimals=answer_decimals))
	return answer

# 計算命令とデータの作成・削除命令をランダム生成する
def make_calc_change_order(order_num, first_list_long, collection_name, calc_method, caluculation_count):
	order_list = []
	db_list_long = first_list_long
	change_stage = 0

	#命令生成
	for i in range(order_num):


		# calc_kind = np.random.choice(["sum", "average", "stdev", "add", "delete"], p=[0.266, 0.266, 0.268, 0.1, 0.1])
		calc_kind = calc_method

		if calc_kind == "sum" or calc_kind == "average" or calc_kind == "stdev":
			# データ計算
			# calc_long = random.randint(1,db_list_long)
			calc_long = caluculation_count
			calc_index_list = random.sample(range(db_list_long), k=calc_long)
			order_item = [calc_index_list, calc_kind, collection_name, i, change_stage]
			order_list.append(order_item)
		# elif calc_kind == "add":
		# 	# データ追加
		# 	add_long = 10
		# 	# float型の要素を持つlistに直す
		# 	add_plain_list =  [randomfloat(3) for i in range(add_long)]
		# 	change_stage += 1
		# 	order_item = [add_plain_list, calc_kind, collection_name, i, change_stage]
		# 	db_list_long += add_long
		# 	order_list.append(order_item)
		# 	if len(order_list) >= 2:
		# 		order_list[-2][4] += 0.5
		# elif calc_kind == "delete":
		# 	#データ削除
		# 	delete_long = 10
		# 	delete_index_list = random.sample(range(db_list_long), k=delete_long)
		# 	change_stage += 1
		# 	order_item = [delete_index_list, calc_kind, collection_name, i, change_stage]
		# 	db_list_long -= delete_long
		# 	order_list.append(order_item)
		# 	if len(order_list) >= 2:
		# 		order_list[-2][4] += 0.5

			
	return order_list

def write_calc_simple_order():
	first_list_long = 500
	calc_method = ["sum", "average", "stdev"]
	caluculation_count = ["10", "30", "50", "70", "100"]
	db_size = ["100", "200", "300", "400", "500"]
	caluculation_repeat = 20
	sample_count_config = 3
	
	for calc_method_item in calc_method:
		for db_size_item in db_size:
			for caluculation_count_item in caluculation_count:
				for sample_no in range(1, sample_count_config + 1):
					order_file = "./order/" + calc_method_item + "/db" + db_size_item + "/" + caluculation_count_item + "_db" + db_size_item + "_*"+ str(caluculation_repeat) + "_" + str(sample_no) + ".json"
					order = make_calc_change_order(caluculation_repeat, int(db_size_item), "test", calc_method_item, int(caluculation_count_item))

					with open(order_file, "w") as f:
						json.dump(order, f, indent = 4)



def main():
	write_calc_simple_order()


if __name__ == '__main__':
    main()