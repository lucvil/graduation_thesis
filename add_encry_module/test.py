from phe import paillier
import time
import phe

public_key, private_key = paillier.generate_paillier_keypair()

#暗号文同士の足し算、引き算及び暗号文と平文との四則演算が可能



# keyring = paillier.PaillierPrivateKeyring()
# keyring.add(private_key)
# public_key1, private_key1 = paillier.generate_paillier_keypair(keyring) 
# public_key2, private_key2 = paillier.generate_paillier_keypair(keyring)

# secret_number_list = [3.141592653, 5000]
# encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]
# decrypted_number_list = [private_key.decrypt(x) for x in encrypted_number_list]
# print(encrypted_number_list)
# print(decrypted_number_list)

#暗号化→暗号文を数値化→復号
# encrypted = (public_key.encrypt(3))
# encrypted_cipher = encrypted.ciphertext()
# print(public_key.encrypt(3).ciphertext(),public_key.encrypt(3).ciphertext())

# encrypted_ob = paillier.EncryptedNumber(public_key,encrypted_cipher)
# print(private_key.decrypt(encrypted_ob))

#暗号文を数値化しない
# time_sta = time.perf_counter()




E1 = public_key.encrypt(4.0 / 3)
E1_cipher = str(E1.ciphertext()) + " " + str(E1.exponent)
E1_cipher_list = [int(x) for x in E1_cipher.split()]
new_E1 = paillier.EncryptedNumber(public_key,E1_cipher_list[0],E1_cipher_list[1])
print(private_key.decrypt(new_E1))

# Ed = public_key.encrypt(4.0)
# E1 = paillier.EncryptedNumber(public_key,Ed.ciphertext(),Ed.exponent)
# print(private_key.decrypt(E1))
# E2 = paillier.EncryptedNumber(public_key,(public_key.encrypt(6)).ciphertext())
# E3 = (public_key.encrypt(100))
# E_list = [E1,E2,E3]

# EA = 0
# EA += E1
# EA += E2
# # for i in E_list:
# #     EA += i
# EA =  EA / 2
 

# DA = private_key.decrypt(EA)
# EA_dammy = paillier.EncryptedNumber(public_key,EA.ciphertext())
# if EA == EA_dammy:
#     print("complete")
# DA = private_key.decrypt(paillier.EncryptedNumber(public_key,EA.ciphertext()))


# time_end = time.perf_counter()
# print(DA)
