## Keybroke (Crypto, medium) - Team Europe Candidates CTF 2022

We get two files, a [key](key.pem) and an [encrypted file](flag.enc). If we look at the key contents, we can see that a part of it was redacted. 

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAx0JsV2KgfnHPLEaOV771Te+gIL/tBJGYaOaaZUDPynpn4SFk
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
fZJwsXdcbXFwvocS9ym9LtQjzM9ZzEEkN2SIqUZhxnpvdfenLf/gIFNNMKvU50b8
NF1Z4xK5l7Cs/RHMlAe66rclQa6VQ347rRr+qWMummccvK1BaCT+Tac6VnTg7GxL
ZI/tTR1yEKjs3OecYurSzn3/ASHcPKtJUgLzAwIDAQABAoIBABgtZxfzT6YICStG
JF9hPEKIoNVYdFnpkKSp1nISuyPGVnRqqN5R1nDDi8GAFzvbMMfYHdnGRMEqYDrt
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
54mAYBKdRoE0TgmldF5Z89vYOesXYNPn2V2ZvsyYMnDxqEcXCoNUK9yJdfqsgqaD
86Eo3v+tS0zr479MT7gv4WbZTeT8vzgtZJs+hgSXBd5jc06l2CMcrJGZgJd1uVuC
yyj+b4ECgYEA7Ur1WTOQkpEL/ZZYS1t/hV1NeCpRuXx4JCm3TF6HRY8Ez5BQid6o
WJ3IZv1+BS9xzh5R+celxUmhwEKosJjhPBl1OHQb3KMmOnVYFGMZRQ3KIi3mVpVB
Dm17kB/dtpHKTlS9YQbtg4j1xF4r2e/1BFkp1BViGRqfN+BZkNhSvrUCgYEA1vfg
0000000000000000000000000000000000000000000000000000000000000000
S2RgIYez934bQzE3uVop+OlM6K3nu4t9ZGuZq/C1Bm3RG0yB3VRM66TxigEauhiQ
oPHhNqwKfyo0ZD4JjfaKZ9tsslxDQnQjJc9mRdcCgYB6MHYkZ8QTZPNKsqdmrof8
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
ssIyPoyUJrxEFpeoWWxKXQKBgQDMLT2CO0MYC8q3OddnsqpIQiOI17UN44VOu/tZ
W/5XVeD1RfrlBVX+x1NnB84OhP22cHwwpJLl5gWaUc3FIS9DPo9VGwpwihTrPg8I
XWblN8hI5e9R1XYXaaVxwAWmxWvES+a652K40elaZRTEDWR30S4efPwd4KIFsVdc
50PFmw0000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
-----END RSA PRIVATE KEY-----
```
The private key is encoded in PEM (Privacy-Enhanced Mail) and the below parameters are encoded in this order:
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
By first decoding the base64 data we have, we can visualize the raw data and try to understand the whole structure. Then we can also decode it to hexadecimal. Each segment begins with the following two headers `02 82 ...` or `02 81 ...`.

1. `02` is the data type (integer),
2. `8n` meaning that the length of the integer value will be encoded in the n following bytes,
3. `81` the actual length of integer, it will be encoded in the following 129 bytes

This is our key, with section headers in red and whole sections in blue:

308204a3020100<span style="color:red">02820101</span>00c7426c5762a07e71cf2c468e57bef54defa020bfed04919868e69a6540cfca7a67e12164d34d34d...d34d347d9270b1775c6d7170be8712f729bd2ed423cccf59cc4124376488a94661c67a6f75f7a72dffe020534d30abd4e746fc345d59e312b997b0acfd11cc9407baeab72541ae95437e3bad1afea9632e9a671cbcad416824fe4da73a5674e0ec6c4b648fed4d1d7210a8ecdce79c62ead2ce7dff0121dc3cab495202f303<span style="color:red">0203</span><span style="color:blue">010001</span><span style="color:red">02820100</span>182d6717f34fa608092b46245f613c4288a0d5587459e990a4a9d67212bb23c656746aa8de51d670c38bc180173bdb30c7d81dd9c644c12a603aedd34d34d34d3...34d34e7898060129d4681344e09a5745e59f3dbd839eb1760d3e7d95d99becc983270f1a847170a83542bdc8975faac82a683f3a128deffad4b4cebe3bf4c4fb82fe166d94de4fcbf382d649b3e86049705de63734ea5d8231cac9199809775b95b82cb28fe6f81<span style="color:red">028181</span><span style="color:blue">00ed4af559339092910bfd96584b5b7f855d4d782a51b97c782429b74c5e87458f04cf905089dea8589dc866fd7e052f71ce1e51f9c7a5c549a1c042a8b098e13c197538741bdca3263a7558146319450dca222de65695410e6d7b901fddb691ca4e54bd6106ed8388f5c45e2bd9eff5045929d41562191a9f37e05990d852beb5</span><span style="color:red">028181</span>00d6f7e0d34d3...34d344b64602187b3f77e1b433137b95a29f8e94ce8ade7bb8b7d646b99abf0b5066dd11b4c81dd544ceba4f18a011aba1890a0f1e136ac0a7f2a34643e098df68a67db6cb25c4342742325cf6645d70281807a30762467c41364f34ab2a766ae87fcd34d34...34d34d34b2c2323e8c9426bc441697a8596c4a5d<span style="color:red">028181</span><span style="color:blue">00cc2d3d823b43180bcab739d767b2aa48422388d7b50de3854ebbfb595bfe5755e0f545fae50555fec7536707ce0e84fdb6707c30a492e5e6059a51cdc5212f433e8f551b0a708a14eb3e0f085d66e537c848e5ef51d5761769a571c005a6c56bc44be6bae762b8d1e95a6514c40d6477d12e1e7cfc1de0a205b1575ce743c59b</span>0d34d34d34d34d...


Looking at the key we can see that the only values that arent half redacted are: e, q and dp. Given this, we can recover p with a quick brute search using the following equation `e*dp = kp * (p - 1) + 1`. We can rearrange is as:
`p = (e * dp - 1) / kp + 1`. Using python, we find a potential prime very quickly:

```python
from Crypto.Util.number import *

q = 0x00ed4af559339092910bfd96584b5b7f855d4d782a51b97c782429b74c5e87458f04cf905089dea8589dc866fd7e052f71ce1e51f9c7a5c549a1c042a8b098e13c197538741bdca3263a7558146319450dca222de65695410e6d7b901fddb691ca4e54bd6106ed8388f5c45e2bd9eff5045929d41562191a9f37e05990d852beb5
dp = 0x00cc2d3d823b43180bcab739d767b2aa48422388d7b50de3854ebbfb595bfe5755e0f545fae50555fec7536707ce0e84fdb6707c30a492e5e6059a51cdc5212f433e8f551b0a708a14eb3e0f085d66e537c848e5ef51d5761769a571c005a6c56bc44be6bae762b8d1e95a6514c40d6477d12e1e7cfc1de0a205b1575ce743c59b
e = 0x10001

for kp in range(3, e):
    p_mul = dp * e - 1
    if p_mul % kp == 0:
        p = (p_mul // kp) + 1
        if isPrime(p):
            print(p)
```
And we find a possible p:
```
p = 150955850358574358001174780262558071526431688108889157159822461877858351493142406329454143458764999067491909126821094217698147322427673106810987186905063569304908696496888819511100068586974332968204802031848195953238675458341198624514153482433009521520356127963233751950558429994025238025625884267016291239383
```
With all our parameters recovered, the last step for total recovery means reconstructing the PEM: 

```python
...
n = p * q
phi = (p-1) * (q-1)
d = pow(e,-1,phi)
key = RSA.construct((n,e,d,p,q))
pem = key.export_key('PEM')
print(pem.decode())
```
We can decrypt the flag by running the command `openssl rsautl -decrypt -inkey key.pem -in flag.enc`.

The flag was: `ecsc{P@rt1@l_d15cl05ur3_15_full_d15cl05ur3}`



