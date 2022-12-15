## Whole Lotta Candy (Crypto, easy)

We’re provided with two connected python files, a [program](server.py) and an [encryption program](encrypt.py).
The server (with which we can only interact with in JSON format) has many functionalities:
1. it encrypts the flag, 
2. we can encrypt our own plaintext,
3. we can change the AES mode

The main problem in this configuration is key reuse, as the server uses the same key for multiple strings. We switch to CTR mode, because it has this vulnerability. Then we send server a plaintext that is at least as long as our ciphertext. To get the result we need to xor our plaintext with the encrypted plaintext and then we xor it again with the encrypted flag, as stated in this equation (although with xor the order of operations doesn't really matter):

`plaintext XOR encrypted plaintext XOR encrypted flag = flag`

This is the solution in python:
```python
import binascii
from pwn import *

encrypted_flag = binascii.unhexlify("138071eae782c7e222ac5a3208529a47f7732c987fac79cf75b32a71c6fc5659a741e61991889fb3f6a88eeabfe9a6dc5f17dd3cdd3d60dc0cba53b273873f5e")
plaintext = b"0000000000000000000000000000000000000000000000000000000000000000"
encrypted_plaintext = binascii.unhexlify("6be403a19cdcb8855cc31a6e5953e440f474649f10fd7ec824c0711e9afd5f01a044891ee98bf0f487c1e1ede7abf9b9566fb261ac4329b371e507b139ca0d6c")
first_xor = xor(plaintext, encrypted_plaintext)
flag = xor(encrypted_flag, first_xor)
print (flag)
```
The flag was: `HTB{KnOWN_pla1N737x7_a77aCk_l19h75_7H3_wAY_7hroU9H_mANy_Mod3z}`
