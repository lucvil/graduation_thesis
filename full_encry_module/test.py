from Pyfhel import Pyfhel, PyCtxt, PyPtxt
import numpy as np
import json

#Pyfhel ドキュメント 
# https://pyfhel.readthedocs.io/en/latest/index.html

# generate key
HE = Pyfhel()
# 他のサイトによるとhe.contextGen(p=65537, m=4096)
# https://colab.research.google.com/github/si1242/he-hackathon-2019/blob/master/Pyfhel_cheatsheet.ipynb#scrollTo=EvREoEHlcfV0
HE.contextGen(scheme='CKKS',n = 2**14, scale=2**30, qi_sizes = [60] + [30]*8 + [60])
HE.keyGen()
HE.relinKeyGen()

#store to file
s_context = HE.to_bytes_context()
s_public_key = HE.to_bytes_public_key()
s_secret_key = HE.to_bytes_secret_key()
s_relin_key = HE.to_bytes_relin_key()

filename = "./full_key.pub"
insert_key = {
	"context" : s_context.hex(),
	"public_key" : s_public_key.hex(),
	"secret_key" : s_secret_key.hex(),
	"relin_key" : s_relin_key.hex()
}



with open(filename, 'r') as f:
	read_data = json.load(f)
	read_data["a"] = insert_key

with open(filename, 'w') as f:
	json.dump(read_data, f, indent = 4)


with open(filename, 'r') as f:
	read_data = json.load(f)



HE_f = Pyfhel() # Empty creation
HE_f.from_bytes_context(bytes.fromhex(read_data["a"]["context"]))
HE_f.from_bytes_public_key(bytes.fromhex(read_data["a"]["public_key"]))
HE_f.from_bytes_secret_key(bytes.fromhex(read_data["a"]["secret_key"]))
HE_f.from_bytes_relin_key(bytes.fromhex(read_data["a"]["relin_key"]))


#int型の暗号化・復号
integer1 = np.array([127.0], dtype=np.float64)
integer2 = np.array([-2.0], dtype=np.float64)
print(integer1)
ctxt1 = HE_f.encryptFrac(integer1) # Encryption makes use of the public key
ctxt2 = HE_f.encryptFrac(integer2) # For integers, encryptInt function is used.
print("3. Integer Encryption, ")
print("    int ",integer1,'-> ctxt1 ', type(ctxt1))
print("    int ",integer2,'-> ctxt2 ', type(ctxt2))
c_b = ctxt1.to_bytes()
c_b_str = c_b.hex()

#16進法の文字列をint型に直す 相当時間がかかるためやらない
# c_b_int = int(c_b_str,16)

# # 0xを抜く
# c_b_str_dec = hex(c_b_int)[2:]

c_b_dec = bytes.fromhex(c_b_str_dec)
if c_b == c_b_dec:
	print("complete")

new_ctxt1 = PyCtxt(pyfhel=HE_f, bytestring=c_b_dec)

dtxt1 = HE_f.decryptFrac(new_ctxt1)
dtxt2 = HE_f.decryptFrac(ctxt2)
print(dtxt1[0],dtxt2[0])

