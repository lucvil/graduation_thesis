#docker import done
import sys
import json
sys.path.append('../')
from json_mun_module import json_mun
import phe
from phe import paillier
import statistics


# record key_pair in file
def add_keypair_dump_jwk(pub, priv, collection_name, date=None):
	"""Serializer for public-private keypair, to JWK format."""

	filename = "./add_encry_module/add_key.pub"

	from datetime import datetime
	if date is None:
		date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

	rec_pub = {
		'kty': 'DAJ',
		'alg': 'PAI-GN1',
		'key_ops': ['encrypt'],
		'n': phe.util.int_to_base64(pub.n),
		'kid': 'Paillier public key generated by phe on {}'.format(date)
	}

	rec_priv = {
		'kty': 'DAJ',
		'key_ops': ['decrypt'],
		'p': phe.util.int_to_base64(priv.p),
		'q': phe.util.int_to_base64(priv.q),
		'kid': 'Paillier private key generated by phe on {}'.format(date)
	}

	insert_key = {
		"rec_pub" : rec_pub,
		"rec_priv" : rec_priv
	}
	

	with open(filename, 'r') as f:
		read_data = json.load(f)
		read_data[collection_name] = insert_key
	
	with open(filename, 'w') as f:
		json.dump(read_data, f, indent = 4)

#load keypair from file
def add_keypair_load_jwk(collection_name):
	"""Deserializer for public-private keypair, from JWK format."""
	filename = "./add_encry_module/add_key.pub"
	with open(filename,"r") as f:
		read_data = json.load(f)

	#add_key.pubからkeyを取ってくる、なければ例外処理にいき作る
	try:
		rec_pub = read_data[collection_name]["rec_pub"]
		rec_priv = read_data[collection_name]["rec_priv"]
	except Exception:
		public_key, private_key = paillier.generate_paillier_keypair()
		add_keypair_dump_jwk(public_key, private_key, collection_name)
		with open(filename,"r") as f:
			read_data = json.load(f)
		rec_pub = read_data[collection_name]["rec_pub"]
		rec_priv = read_data[collection_name]["rec_priv"]
	
	# Do some basic checks                                                                                                                                                      
	assert rec_pub['kty'] == "DAJ", "Invalid public key type"
	assert rec_pub['alg'] == "PAI-GN1", "Invalid public key algorithm"
	assert rec_priv['kty'] == "DAJ", "Invalid private key type"
	pub_n = phe.util.base64_to_int(rec_pub['n'])
	pub = paillier.PaillierPublicKey(pub_n)
	priv_p = phe.util.base64_to_int(rec_priv['p'])
	priv_q = phe.util.base64_to_int(rec_priv['q'])
	priv = paillier.PaillierPrivateKey(pub, priv_p, priv_q)
	return pub, priv





#add_encrypt simple data
def add_only_encrypt_one(data,collection_name):
	public_key, private_key = add_keypair_load_jwk(collection_name)
	return public_key.encrypt(data)

#add_decrypt simple data
def add_only_decrypt_one(data, collection_name):
	public_key, private_key = add_keypair_load_jwk(collection_name)
	return private_key.decrypt(paillier.EncryptedNumber(public_key,data))
	


#encrypt simple data
def add_encrypt_one(data,collection_name):
	if type(data) is str:
		return data
	elif type(data) is int:
		result = add_only_encrypt_one(data, collection_name) 
		return result.ciphertext()
	elif type(data) is float:
		result = add_only_encrypt_one(data, collection_name) 
		return result.ciphertext()

#decrypt simple data
def add_decrypt_one(data,collection_name):
	try:
		return add_only_decrypt_one(data, collection_name)
	except Exception:
		return data


#encrypt json
#add_encrypt_oneによりadd_encyptされた暗号文はint型に直される
def add_encrypt_json(plain_json,collection_name):
	result = json_mun.func_json_data(add_encrypt_one,plain_json,collection_name)
	return result


#decrypt json
def add_decrypt_json(encrypted_json, collection_name):
	result = json_mun.func_json_data(add_decrypt_one, encrypted_json,collection_name)
	return result



#caluculate系はまだテストしていない
#caluculate sum from list
def add_caluculate_sum(encrypted_list, collection_name):
	encrypted_sum = 0
	for i in range(len(encrypted_list)):
		encrypted_sum += encrypted_list[i]
	
	return encrypted_sum


#caluculate average from list
def add_caluculate_average(encrypted_list, collection_name):
	encrypted_sum = 0
	for i in range(len(encrypted_list)):
		encrypted_sum += encrypted_list[i]
	
	encrypted_average = encrypted_sum / len(encrypted_list)

	return encrypted_average


#caluculate stdev(標準偏差) from list
#全てのデータを復号して計算し暗号化し直す
def add_caluculate_stdev(encrypted_list, collection_name):
	#標準偏差を求めるため一回復号する
	#この時本来であればユーザーとの通信が入るためダミー時間のsleepを設けること
	public_key, private_key = add_keypair_load_jwk(collection_name)
	decrypted_number_list = [private_key.decrypt(x) for x in encrypted_list]
	plain_stdev = statistics.pstdev(decrypted_number_list)
	encrypted_stdev = public_key.encrypt(plain_stdev)

	return encrypted_stdev



# def main():

# 	collection_name = "add_test"
# 	result = add_keypair_load_jwk(collection_name)

# if __name__ == '__main__':
#     main()



