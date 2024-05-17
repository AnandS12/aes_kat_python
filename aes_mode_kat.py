from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import sys
import random
from Crypto.Util import Counter

mode = sys.argv[1].upper() if len(sys.argv) > 1 else "CFB"
n = int(sys.argv[2])  if  len(sys.argv) > 2 else 1
key_size = int(sys.argv[3]) if len(sys.argv) > 3 else 128

if mode == "CFB":
    aes_mode = AES.MODE_CFB
    iv_length=16
elif mode == "OFB":
    aes_mode = AES.MODE_OFB
    iv_length=16
elif mode == "CTR":
    aes_mode = AES.MODE_CTR
    iv_length=8

#string key_size_str = $sformatf("%d", key_size);

enc_file_path = "aes_{}_{}_kats.txt".format(mode.lower(),key_size)
with open(enc_file_path, 'w') as f:
    pass

with open(enc_file_path, 'w') as writer:
    writer.writelines("")


def  print_kat(plaintext, key, iv,ciphertext):
    hex_data = binascii.hexlify(key)
    # Convert hexadecimal bytes to a hexadecimal string
    hex_string = hex_data.decode('utf-8')
    with open(enc_file_path, 'a') as writer:
        writer.writelines("KEY=0X"+hex_string+"\n")
    hex_data = binascii.hexlify(iv)
    hex_string = hex_data.decode('utf-8')
    with open(enc_file_path, 'a') as writer:
      writer.writelines("IV=0X"+hex_string+"\n")
    hex_data = binascii.hexlify(plaintext)
    hex_string = hex_data.decode('utf-8')
    hex_data = binascii.unhexlify(hex_string)
    block_size_bytes = 16
    num_blocks = int(len(hex_data)/16) # block_size_bytes
    print(num_blocks)
    blocks = [hex_data[i*block_size_bytes:(i+1)*block_size_bytes] for i in range(num_blocks)]
    hex_blocks = ['0X' + binascii.hexlify(block).decode('utf-8') for block in blocks]
    with open(enc_file_path, 'a') as writer:
      for i, block in enumerate(hex_blocks):
        writer.writelines(f"Plain text Block {i+1}: {block}\n")
    hex_data = binascii.hexlify(ciphertext)
    hex_string = hex_data.decode('utf-8')
    hex_data = binascii.unhexlify(hex_string)
    blocks = [hex_data[i*block_size_bytes:(i+1)*block_size_bytes] for i in range(num_blocks)]
    hex_blocks = ['0X' + binascii.hexlify(block).decode('utf-8') for block in blocks]
    with open(enc_file_path, 'a') as writer:
      for i, block in enumerate(hex_blocks):
        writer.writelines(f"Cipher text Block {i+1}: {block}\n")
      #writer.writelines("CIPHERTEXT=0X"+hex_string+"\n")


def encrypt(plaintext, key, iv):
   if aes_mode==AES.MODE_CFB:
    cipher = AES.new(key, AES.MODE_CFB, iv,segment_size=128)
   elif aes_mode==AES.MODE_OFB:
    cipher = AES.new(key, AES.MODE_OFB, iv)
   elif aes_mode==AES.MODE_CTR:
    #ctr = Counter.new(128, prefix=iv)
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
   ciphertext = cipher.encrypt(plaintext)
   if aes_mode==AES.MODE_CTR:
     print_kat(plaintext, key,iv,ciphertext)
   else:
     print_kat(plaintext, key, iv,ciphertext)

def encrypt_128(plaintext,iv):
    key =get_random_bytes(16)  # 16 bytes key for AES-128
    encrypt(plaintext, key, iv)

def encrypt_192(plaintext,iv):
    key =get_random_bytes(24)  # 24 bytes key for AES-192
    encrypt(plaintext, key, iv)

def encrypt_256(plaintext,iv):
    key =get_random_bytes(32)  # 32 bytes key for AES-256
    encrypt(plaintext, key, iv)


def decrypt(ciphertext, key, iv):
    if aes_mode==AES.MODE_CFB:
      cipher = AES.new(key, aes_mode, iv,segment_size=128)
    elif aes_mode==AES.MODE_OFB:
      cipher = AES.new(key, AES.MODE_OFB, iv)
    elif aes_mode==AES.MODE_CTR:
      #ctr = Counter.new(64, prefix=iv)
      cipher = AES.new(key, AES.MODE_CTR,nonce=iv)
    decrypted = cipher.decrypt(ciphertext)
    print_kat(decrypted, key, iv,ciphertext)    
    #return decrypted

def decrypt_128(ciphertext,iv):
    key =get_random_bytes(16)  # 16 bytes key for AES-128
    decrypt(ciphertext, key, iv)

def decrypt_192(ciphertext,iv):
    key =get_random_bytes(24)  # 24 bytes key for AES-192
    decrypt(ciphertext, key, iv)

def decrypt_256(ciphertext,iv):
    key =get_random_bytes(32)  # 32 bytes key for AES-256
    decrypt(ciphertext, key, iv)

for i in range(n):
    e_or_d=random.choice([0,1])
    if(e_or_d==1):
      with open(enc_file_path, 'a') as writer:
        writer.writelines("OPERATION::ENCRYPTION"+"\n")
      num_block=random.choice(range(1,5))
      plaintext = get_random_bytes(16*num_block) 
      iv =get_random_bytes(iv_length)
      with open(enc_file_path, 'a') as writer:
        writer.writelines("Number_of_blocks="+str(num_block)+"\n")
      if(key_size==128):
         encrypt_128(plaintext,iv)
      elif(key_size==192):
         encrypt_192(plaintext,iv)
      elif(key_size==256):
         encrypt_256(plaintext,iv)
    elif(e_or_d==0):
      with open(enc_file_path, 'a') as writer:
        writer.writelines("OPERATION::DECRYPTION"+"\n")
      num_block=random.choice(range(1,7))
      ciphertext =get_random_bytes(16*num_block) 
      iv =get_random_bytes(iv_length)
      with open(enc_file_path, 'a') as writer:
        writer.writelines("Number_of_blocks="+str(num_block)+"\n")
      if(key_size==128):
         decrypt_128(ciphertext,iv)
      elif(key_size==192):
         decrypt_192(ciphertext,iv)
      elif(key_size==256):
         decrypt_256(ciphertext,iv)
    


