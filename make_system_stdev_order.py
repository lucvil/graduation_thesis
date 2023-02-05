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

def make_bias_order_seed(change_order_ratio, order_num, bias_group_size, stdev_order_ratio):
	change_order_list = []
	calc_order_list = []
	change_order_num = int(order_num * change_order_ratio)
	calc_order_num = order_num - int(order_num * change_order_ratio)

	for i in range(change_order_num):
		if i % 2 == 0:
			change_order_list.append("add")
		else:
			change_order_list.append("delete")
	
	for i in range(calc_order_num):
		if i % 2 == 0:
			calc_order_list.append("stdev")
		elif i % 4 == 1:
			calc_order_list.append("sum")
		else:
			calc_order_list.append("average")

	
	order_kind_list = []
	now_calc_index = 0
	now_change_index = 0
	for i in range(order_num):
		if i % bias_group_size < int(bias_group_size -  bias_group_size * change_order_ratio):
			order_kind_list.append(calc_order_list[now_calc_index])
			now_calc_index += 1
		else:
			order_kind_list.append(change_order_list[now_change_index])
			now_change_index += 1
	
	if now_calc_index != calc_order_num or now_change_index != change_order_num:
		print("error")

	return order_kind_list

def make_even_order_seed(change_order_ratio, order_num, stdev_order_ratio):
	change_order_list = []
	calc_order_list = []
	change_order_num = int(order_num * change_order_ratio)
	calc_order_num = order_num - int(order_num * change_order_ratio)

	for i in range(change_order_num):
		if i % 2 == 0:
			change_order_list.append("add")
		else:
			change_order_list.append("delete")
	
	for i in range(calc_order_num):
		if i % 4 <= int(4*stdev_order_ratio) - 1:
			calc_order_list.append("stdev")
		elif i % 2 == 1:
			calc_order_list.append("sum")
		else:
			calc_order_list.append("average")

	
	order_kind_list = []
	now_calc_index = 0
	now_change_index = 0
	for i in range(order_num):
		if i % 5 < int(5 - 5 * change_order_ratio):
			order_kind_list.append(calc_order_list[now_calc_index])
			now_calc_index += 1
		else:
			order_kind_list.append(change_order_list[now_change_index])
			now_change_index += 1
	
	if now_calc_index != calc_order_num or now_change_index != change_order_num:
		print("error")
	
	return order_kind_list






# 計算命令とデータの作成・削除命令をランダム生成する
def make_calc_change_order(order_num, first_list_long, collection_name, caluculation_count, change_order_ratio ,bias_method, bias_group_size, stdev_order_ratio):
	order_list = []
	db_list_long = first_list_long
	change_stage = 0

	# 命令種類決定
	if bias_method == "even":
		calc_kind_list = make_even_order_seed(change_order_ratio, order_num, stdev_order_ratio)
	elif bias_method == "bias":
		calc_kind_list = make_bias_order_seed(change_order_ratio, order_num, bias_group_size, stdev_order_ratio)

	#命令生成
	for i in range(order_num):
		

		# calc_kind = np.random.choice(["sum", "average", "stdev", "add", "delete"], p=[0.266, 0.266, 0.268, 0.1, 0.1])
		calc_kind = calc_kind_list[i]

		if calc_kind == "sum" or calc_kind == "average" or calc_kind == "stdev":
			# データ計算
			# calc_long = random.randint(1,db_list_long)
			calc_long = caluculation_count
			calc_index_list = random.sample(range(db_list_long), k=calc_long)
			order_item = [calc_index_list, calc_kind, collection_name, i, change_stage]
			order_list.append(order_item)
		elif calc_kind == "add":
			# データ追加
			add_long = 10
			# float型の要素を持つlistに直す
			add_plain_list =  [randomfloat(5) for i in range(add_long)]
			change_stage += 1
			order_item = [add_plain_list, calc_kind, collection_name, i, change_stage]
			db_list_long += add_long
			order_list.append(order_item)
			if len(order_list) >= 2:
				order_list[-2][4] += 0.5
		elif calc_kind == "delete":
			#データ削除
			delete_long = 10
			delete_index_list = random.sample(range(db_list_long), k=delete_long)
			change_stage += 1
			order_item = [delete_index_list, calc_kind, collection_name, i, change_stage]
			db_list_long -= delete_long
			order_list.append(order_item)
			if len(order_list) >= 2:
				order_list[-2][4] += 0.5

			
	return order_list

def write_calc_simple_order():

	caluculation_count = ["50"]
	db_size = ["100"]
	order_num = 50
	sample_count_config = 1
	bias_method = ["even", "bias"]
	change_order_ratio = [0.2]
	bias_group_size = 50
	stdev_order_ratio = [0, 0.25, 0.5, 0.75, 1.0]
	

	for bias_method_item in bias_method:
		for db_size_item in db_size:
			for caluculation_count_item in caluculation_count:
				for change_order_ratio_item in change_order_ratio:
					for stdev_order_ratio_item in stdev_order_ratio: 
						for sample_no in range(1, sample_count_config + 1):
							order_file = "./order/system/" + bias_method_item + "/db" + db_size_item + "/db" + db_size_item + "_*"+ str(order_num) + "_" + str(change_order_ratio_item) + "_" + str(stdev_order_ratio_item) + "_" + str(sample_no) + ".json"
							order = make_calc_change_order(order_num, int(db_size_item), "test", int(caluculation_count_item), change_order_ratio_item, bias_method_item, bias_group_size, stdev_order_ratio_item)

							with open(order_file, "w") as f:
								json.dump(order, f, indent = 4)



def main():
	write_calc_simple_order()


if __name__ == '__main__':
    main()