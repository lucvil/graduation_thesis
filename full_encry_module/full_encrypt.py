import sys
import json
sys.path.append('../')
from json_mun_module import json_mun
from Pyfhel import Pyfhel, PyCtxt, PyPtxt
import numpy as np
import copy

#record key_pair in file
def full_keypair_store(HE, collection_name):
	filename = "./full_encry_module/full_key.pub"

	#make key_data to insert
	s_context = HE.to_bytes_context()
	s_public_key = HE.to_bytes_public_key()
	s_secret_key = HE.to_bytes_secret_key()
	s_relin_key = HE.to_bytes_relin_key()

	#byte Objectを.hex()により16進数の文字列に直して挿入
	insert_key = {
		"context" : s_context.hex(),
		"public_key" : s_public_key.hex(),
		"secret_key" : s_secret_key.hex(),
		"relin_key" : s_relin_key.hex()
	}

	with open(filename, 'r') as f:
		read_data = json.load(f)
		read_data[collection_name] = insert_key

	with open(filename, 'w') as f:
		json.dump(read_data, f, indent = 4)


#load key_pair from file
def full_keypair_load(collection_name):
	filename = "./full_encry_module/full_key.pub"
	with open(filename,"r") as f:
		read_data = json.load(f)

	#full_key.pubからkeyを取ってくる、なければ例外処理で作る
	#keyを取る時16進数の文字列からbyteObjecttに直す
	try:
		rec_HE = Pyfhel() # Empty creation
		rec_HE.from_bytes_context(bytes.fromhex(read_data[collection_name]["context"]))
		rec_HE.from_bytes_public_key(bytes.fromhex(read_data[collection_name]["public_key"]))
		rec_HE.from_bytes_secret_key(bytes.fromhex(read_data[collection_name]["secret_key"]))
		rec_HE.from_bytes_relin_key(bytes.fromhex(read_data[collection_name]["relin_key"]))
	
	except Exception:
		made_HE = Pyfhel()
		made_HE.contextGen(scheme='CKKS',n = 2**14, scale=2**30, qi_sizes = [60] + [30]*8 + [60])
		made_HE.keyGen()
		made_HE.relinKeyGen()

		full_keypair_store(made_HE, collection_name)

		with open(filename, 'r') as f:
			read_data = json.load(f)

		rec_HE = Pyfhel() # Empty creation
		rec_HE.from_bytes_context(bytes.fromhex(read_data[collection_name]["context"]))
		rec_HE.from_bytes_public_key(bytes.fromhex(read_data[collection_name]["public_key"]))
		rec_HE.from_bytes_secret_key(bytes.fromhex(read_data[collection_name]["secret_key"]))
		rec_HE.from_bytes_relin_key(bytes.fromhex(read_data[collection_name]["relin_key"]))

	return rec_HE

		
#full_encrypt simple data
#return cipher 16進法の文字列
def full_only_encrypt_one(data, collection_name):
	HE = full_keypair_load(collection_name)
	np_data = np.array([data], dtype=np.float64)
	encrypted_data_pyctext = HE.encryptFrac(np_data)
	encrypted_data_bytes = encrypted_data_pyctext.to_bytes()
	encrypted_data_str16 = encrypted_data_bytes.hex()
	
	return encrypted_data_str16


#full_decrypt simple data
def full_only_decrypt_one(data_str16, collection_name):
	HE = full_keypair_load(collection_name)
	data_bytes = bytes.fromhex(data_str16)
	data_pyctxt = PyCtxt(pyfhel=HE, bytestring=data_bytes)
	decrypted_array = HE.decryptFrac(data_pyctxt)
	return decrypted_array[0]

#encrypt simple data
def full_encrypt_one(data, collection_name):
	if type(data) is str:
		return data
	elif type(data) is int:
		result = full_only_encrypt_one(float(data), collection_name) 
		return result
	elif type(data) is float:
		result = full_only_encrypt_one(data, collection_name) 
		return result


#decrypt simple data
def full_decrypt_one(data, collection_name):
	try:
		return full_only_decrypt_one(data, collection_name)
	except Exception:
		return data

#encrypt json
def full_encrypt_json(plain_json,collection_name):
	result =  json_mun.func_json_data(full_encrypt_one,plain_json,collection_name)
	return result

#decrypt json
def full_decrypt_json(encrypted_json, collection_name):
	result = json_mun.func_json_data(full_decrypt_one, encrypted_json, collection_name)
	return result


#caluculate sum from list
#今の所実装していないが計算しすぎるとError:scale out of boundsするので、
# 本当はtry文でエラー検知し復号->暗号化し直す必要がある
# 掛け算を8回ぐらいするとアウト、足し算は基本的には問題ない

# 注意
# 足し算するときはそれぞれのparamaterを揃える必要がある
# 具体的には足し算、掛け算をするときはそれぞれの数が今まで行ってきた掛け算の数を同じにする必要がある。
# 0とciphertextを足すのも基本的には禁止
# でないとValueError: encrypted1 and encrypted2 parameter mismatchが出る
def full_caluculate_sum(encrypted_list, collection_name):
	# 十六進法文字列の配列をPyCtxt型の配列に直す
	HE = full_keypair_load(collection_name)
	cipher_bytes = [bytes.fromhex(encry_str16_item) for encry_str16_item in encrypted_list]
	cipher_pyctxt = [PyCtxt(pyfhel=HE, bytestring=cipher_bytes_item) for cipher_bytes_item in cipher_bytes]

	#計算
	#ただ代入するだけだと代入元と代入先で同じメモリを参照することになる。
	#これで引き算をすると同じメモリを参照しているもの同士の引き算となりエラーを出す
	#その場合RuntimeError: result ciphertext is transparentを出す
	encrypted_sum_pyctxt = cipher_pyctxt[0].copy()
	for cipher_pyctxt_item in cipher_pyctxt[1:]:
		encrypted_sum_pyctxt += cipher_pyctxt_item
		~encrypted_sum_pyctxt
	
	#答えを16進法文字列に直す
	encrypted_sum_bytes = encrypted_sum_pyctxt.to_bytes()
	encrypted_sum_str16 = encrypted_sum_bytes.hex()

	return encrypted_sum_str16
	

#caluculate average from list
def full_caluculate_average(encrypted_list, collection_name):
	# 十六進法文字列の配列をPyCtxt型の配列に直す
	HE = full_keypair_load(collection_name)
	cipher_bytes = [bytes.fromhex(encry_str16_item) for encry_str16_item in encrypted_list]
	cipher_pyctxt = [PyCtxt(pyfhel=HE, bytestring=cipher_bytes_item) for cipher_bytes_item in cipher_bytes]

	#計算
	encrypted_sum_pyctxt = cipher_pyctxt[0].copy()
	for cipher_pyctxt_item in cipher_pyctxt[1:]:
		encrypted_sum_pyctxt += cipher_pyctxt_item
		~encrypted_sum_pyctxt
	encrypted_average_pyctxt = encrypted_sum_pyctxt / len(encrypted_list)
	~encrypted_average_pyctxt

	#答えを16進法文字列に直す
	encrypted_average_bytes = encrypted_average_pyctxt.to_bytes()
	encrypted_average_str16 = encrypted_average_bytes.hex()

	return encrypted_average_str16

#caluculate stdev
def full_caluculate_stdev(encrypted_list, collection_name):
	# 十六進法文字列の配列をPyCtxt型の配列に直す
	HE = full_keypair_load(collection_name)
	cipher_bytes = [bytes.fromhex(encry_str16_item) for encry_str16_item in encrypted_list]
	cipher_pyctxt = [PyCtxt(pyfhel=HE, bytestring=cipher_bytes_item) for cipher_bytes_item in cipher_bytes]

	#計算
	encrypted_sum_pyctxt = cipher_pyctxt[0].copy()
	for cipher_pyctxt_item in cipher_pyctxt[1:]:
		encrypted_sum_pyctxt += cipher_pyctxt_item
		~encrypted_sum_pyctxt
	encrypted_average_pyctxt = encrypted_sum_pyctxt / len(encrypted_list)
	
	encrypted_stdev_pyctxt = (cipher_pyctxt[0] - encrypted_average_pyctxt) ** 2
	for cipher_pyctxt_item in cipher_pyctxt[1:]:
		encrypted_stdev_pyctxt += (cipher_pyctxt_item - encrypted_average_pyctxt) ** 2

	encrypted_stdev_pyctxt /= len(encrypted_list)

	#答えを16進法文字列に直す
	encrypted_stdev_bytes = encrypted_stdev_pyctxt.to_bytes()
	encrypted_stdev_str16 = encrypted_stdev_bytes.hex()

	return encrypted_stdev_str16


#caluculate 