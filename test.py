import json
import sys
from collections import OrderedDict

import rsa

# 参照：https://self-development.info/rsa暗号の計算処理を実装できるpython-rsaのインストール/



# rsa暗号化
def encrypt(data):
	pub_file_path = "pub_key.pem"
	private_file_path = "private_key.pem"
	
	with open(pub_file_path, mode='rb') as f:
		pub_str = f.read()
		pub_key = rsa.PublicKey.load_pkcs1(pub_str)
	
	with open(private_file_path, mode='rb') as f:
		private_str = f.read()
		private_key = rsa.PrivateKey.load_pkcs1(private_str)
	
	ans = rsa.encrypt(((str)(data).encode('utf-8')),pub_key)
	return ans

# rsa復号化
def decrypt(data):
	pub_file_path = "pub_key.pem"
	private_file_path = "private_key.pem"
	
	with open(pub_file_path, mode='rb') as f:
		pub_str = f.read()
		pub_key = rsa.PublicKey.load_pkcs1(pub_str)
	
	with open(private_file_path, mode='rb') as f:
		private_str = f.read()
		private_key = rsa.PrivateKey.load_pkcs1(private_str)
	
	ans = rsa.decrypt(data,private_key).decode('utf-8')
	return ans


# json型のデータを全探索し、個々の要素に対して何らかの操作をする
def make_data_encry(data):
	if type(data) == OrderedDict or type(data) == dict:
		encrypted_json = {}
		for k, v in data.items():
			encrypted_json[encrypt(k)] = make_data_encry(v)
		return encrypted_json
	elif type(data) == list:
		encrypted_list = []
		for i, e in enumerate(data):
			encrypted_list.append(make_data_encry(e))
		return encrypted_list
	else:
		return encrypt(data)



def make_data_decry(data):
	if type(data) == OrderedDict or type(data) == dict:
		decrypted_json = {}
		for k, v in data.items():
			decrypted_json[decrypt(k)] = make_data_decry(v)
		return decrypted_json
	elif type(data) == list:
		decrypted_list = []
		for i, e in enumerate(data):
			decrypted_list.append(make_data_decry(e))
		return decrypted_list
	else:
		print(data)
		return decrypt(data)

def main():
	# input = sys.argv[1]
	input = "test.json"
	json_open = open(input,'r')
	json_load = json.load(json_open)
	print(json_load)

	encrypted_data = make_data_encry(json_load)
	print(encrypted_data)
	decrypted_data = make_data_decry(encrypted_data)
	print(decrypted_data)
	

if __name__ == '__main__':
    main()
