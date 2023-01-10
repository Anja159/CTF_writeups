## babymixup (Crypto, easy)
We are provided with a python program and it's output. This is the source:

```python
from Crypto.Cipher import AES
import os

key = os.urandom(16)

flag = b"flag{REDACTED}"
assert len(flag) % 16 == 0

iv = os.urandom(16)
cipher = AES.new(iv,  AES.MODE_CBC, key)
print("IV1 =", iv.hex())
print("CT1 =", cipher.encrypt(b"Hello, this is a public message. This message contains no flags.").hex())

iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
print("IV2 =", iv.hex())
print("CT2 =", cipher.encrypt(flag).hex())
```
![CBC.png](CBC.png)

The application uses the AES-CBC encryption. If we look at the way both ciphers are initalised, we notice that the first cipher uses the value of `iv` as the `key`, which is later used as key in the second cipher:
```python
cipher = AES.new(iv,  AES.MODE_CBC, key)
cipher = AES.new(key, AES.MODE_CBC, iv)
```
And because the value of `iv` is printed out, we now know the key and we only need to calculate the IV. We are going to calculate it through the equation:

$\;\;\;\;\;\;\;\;\;\;\;IV=decrypt(key,ciphertext)\;\;xor\;\;plaintext$

Because of the way AES-CBC works the first block is encypted the same as in AES-ECB, which doesn't use IV in decryption. We decrypt the first block and then xor it with the known plaintext (which is in hex). The value of IV is represented by the first 32 characters (16 bytes).

```python
cipher = AES.new(key,  AES.MODE_ECB)
decrypted = cipher2.decrypt(ciphertext)
iv = xor(dec,pt).hex()
```

The only thing left to do is decrypt the ciphertext with AES-CBC, with the known key and IV value. Solve script:

```python
from Crypto.Cipher import AES
from pwn import *

IV1 = bytearray.fromhex("4ee04f8303c0146d82e0bbe376f44e10")
CT1 = bytearray.fromhex("de49b7bb8e3c5e9ed51905b6de326b39b102c7a6f0e09e92fe398c75d032b41189b11f873c6cd8cdb65a276f2e48761f6372df0a109fd29842a999f4cc4be164")
IV2 = bytearray.fromhex("1fe31329e7c15feadbf0e43a0ee2f163")
CT2 = bytearray.fromhex("f6816a603cefb0a0fd8a23a804b921bf489116fcc11d650c6ffb3fc0aae9393409c8f4f24c3d4b72ccea787e84de7dd0")
pt  = str.encode("Hello, this is a public message. This message contains no flags.")

cipher = AES.new(IV1,  AES.MODE_ECB)
decrypted = cipher.decrypt(CT1)
iv = bytearray.fromhex(xor(decrypted,pt).hex()[0:32])

cipher = AES.new(iv,  AES.MODE_CBC, IV2)
print(cipher.decrypt(CT2))
```

The flag is: `irisctf{the_iv_aint_secret_either_way_using_cbc}`