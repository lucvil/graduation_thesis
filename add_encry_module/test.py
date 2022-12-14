from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()



# keyring = paillier.PaillierPrivateKeyring()
# keyring.add(private_key)
# public_key1, private_key1 = paillier.generate_paillier_keypair(keyring) 
# public_key2, private_key2 = paillier.generate_paillier_keypair(keyring)

# secret_number_list = [3.141592653, 5000]
# encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]
# decrypted_number_list = [private_key.decrypt(x) for x in encrypted_number_list]
# print(encrypted_number_list)
# print(decrypted_number_list)

encrypted = (public_key.encrypt(3))
encrypted_cipher = encrypted.ciphertext()
print(public_key.encrypt(3).ciphertext(),public_key.encrypt(3).ciphertext())

encrypted_ob = paillier.EncryptedNumber(public_key,encrypted_cipher)
print(private_key.decrypt(encrypted_ob))
