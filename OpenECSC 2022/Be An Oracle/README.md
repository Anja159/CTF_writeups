## Be An Oracle (Crypto, hard)

We are given a python [program](chall.py) and we can conect to the server, where we can choose from two options:

1. Send some payload to server which then decrypts
2. Reboot the server

Looking at the code we can see the server uses RSA encryption with the following parameters:

```python
KEYSIZE = 1024
q = gen_prime(KEYSIZE // 2 - KEYSIZE // 16)
p = gen_prime(KEYSIZE // 2 + KEYSIZE // 16, q)
phi = (p-1) * (q-1)
e = 65337
while True:
        d = inv(e, phi)
        if d and ((e * d) % phi) == 1:
            break
        e = gen_prime(16)
```
Server also takes our payload and decodes it using the following equations:
```python
m = pow(pow(int.from_bytes(flag, 'big'), e, p * q), vals[3], vals[1])
    return m.to_bytes((m.bit_length() + 7) // 8, 'big')
```
The inner function encrypts text and the outer decrypts it if we use the right parameters, so we can conclude that `flag = pow(pow(flag,e,n),d,n)`. That means we have to set `vals[3] = d` and `vals[1] = n`

The primes are generated with this seed:
```python
seed = (int(time.time()) & 0xfffffff0) + (os.getpid() & 0x65)
random.seed(seed)
```
It is a sum of time and the process pid. The time increases by blocks of 16 and there is only a limited number of possibilities for a process id. 

In order for the program to work you need to set the seed one interval in the future (+16) and the process id which I used was 4 (I'm still not sure why this worked). The server has to be rebooted before every try, so the pid stays in the same range. 

From our seed we can than compute p,q and d and send it to the server in payload, but are a certain conditions which we have to satisfy for the server to accept the string. Fortunately quickly enough I realised it is the same format which is used in private pem RSA keys.

This is how the PEM key format looks like:
```
PrivateKeyInfo ::= SEQUENCE {
   version Version,
   privateKeyAlgorithm AlgorithmIdentifier ,
   privateKey PrivateKey,
   attributes [0] Attributes OPTIONAL
}

RSAPrivateKey ::= SEQUENCE {
  version           Version,
  modulus           INTEGER,  -- n
  publicExponent    INTEGER,  -- e
  privateExponent   INTEGER,  -- d
  prime1            INTEGER,  -- p
  prime2            INTEGER,  -- q
  exponent1         INTEGER,  -- d mod (p-1)
  exponent2         INTEGER,  -- d mod (q-1)
  coefficient       INTEGER,  -- (inverse of q) mod p
  otherPrimeInfos   OtherPrimeInfos OPTIONAL
}
```

1. There are 10 sections,
2. The string has to start with byte 0x30, and each section has to start with 0x02 (the int data type)
```python
for typ in [48] + [2]*9
```
3. The second byte 0x82 means that the length of the section will be encoded in the following 2 bytes, 
4. The following bytes encode the length of the sections

And so on...

For vals[1] to take the value of n, we must put it in the third section and for vals[3] to take value of d we put it in the fifth section. 
This is an example of a string that bypasses all the restrictions:
```python
line="30820126020202020282008100"+p*q+"020203020282008100"+d+"0202020202020202020202020202020202020202"
```
The solve script:
```python
...
seed = (int(time.time()) & 0xfffffff0)+(4 & 0x65)
seed = seed + 16

q = gen_prime(KEYSIZE // 2 - KEYSIZE // 16)
    p = gen_prime(KEYSIZE // 2 + KEYSIZE // 16, q)
    phi = (p-1) * (q-1)
    e = 65337

    while True:
        d = inv(e, phi)
        if d and ((e * d) % phi) == 1:
            break
        e = gen_prime(16)
        
r.sendline(b"1")
line = "30820126020202020282008100" + p*q + "020203020282008100" + d + "0202020202020202020202020202020202020202"
print(r.recvline())
```

The server decrypts it and returns us the flag b'Decrypted: `d52fde26-1e71-4ba1-8a6d-990a2f4255cb`\n'.
