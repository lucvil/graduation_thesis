import rsa
 
pub_file_path = "pub_key.pem"
private_file_path = "private_key.pem"
 
with open(pub_file_path, mode='rb') as f:
    pub_str = f.read()
    pub_key = rsa.PublicKey.load_pkcs1(pub_str)
 
with open(private_file_path, mode='rb') as f:
    private_str = f.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_str)
 
 
message = 'RSAで暗号化'.encode('utf8')
 
# 暗号化
crypto = rsa.encrypt(message, pub_key)
print(crypto)
 
# 復号化
decode_message = rsa.decrypt(crypto, private_key)
print(decode_message.decode('utf8'))