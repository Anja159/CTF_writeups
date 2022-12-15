#!/usr/bin/env python3
from time import time
from struct import pack, unpack
from secrets import randbelow, token_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from ecdsa.ecdsa import generator_256, Public_key, Private_key, Signature

start_time = time()
G = generator_256
order = G.order()
d = randbelow(order) + 1
pubkey = Public_key(G, d*G)
privkey = Private_key(pubkey, d)

def menu():
    while True:
        sel = input("""
1. Test some ideas
2. Attempt solution
3. Reboot server
? """).strip()
        if sel == '1':
            hint()
        elif sel == '2':
            test()
        elif sel == '3':
            exit(0)

def hint():
    inp = input("Enter message to sign in hex: ")
    try:
        m = int.from_bytes(bytes.fromhex(inp), 'big')
        k = digest(privkey.secret_multiplier) + digest(m)
        sig = privkey.sign(m, k)
        print("r:", sig.r)
        print("s:", sig.s)
    except:
        print("Unable to sign the message")

def test():
    m = int.from_bytes(token_bytes(64), 'big')
    print("Please sign this for me: ", m)
    try:
        r = int.from_bytes(bytes.fromhex(input("Enter R in hex: ")), 'little')
        s = int.from_bytes(bytes.fromhex(input("Enter S in hex: ")), 'little')
        sig = Signature(r, s)
        if time() < start_time + 10.1 and pubkey.verifies(m, sig):
            done(m)
    except Exception:
        print("Unable to verify the signature")

def done(m):
    flag = open('flag.txt').read().strip().encode()
    key = bytes.fromhex("%032x" % digest(privkey.secret_multiplier))
    key += bytes.fromhex("%032x" % digest(m))
    iv = token_bytes(16)
    enc = AES.new(key, AES.MODE_CFB, iv).encrypt(pad(flag, 16))
    print("Encrypted flag:", enc.hex())
    print("IV:", iv.hex())

def u32(value): return value & ((1<<32)-1)
def lrot(value, n): return u32(value<<n) | (value>>(32-n))

def digest(m):
    Xi = [3, 7, 11, 19, 3, 5, 9, 13, 3, 9, 11, 15]
    Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    msg = bytes([(m & (0xff<<p*8))>>p*8 for p in range((m.bit_length()+7)//8)])
    ml = len(msg) * 8
    msg += b"\x80"
    msg += b"\x00" * (-(len(msg) + 8) % 64)
    msg += pack("<Q", ml)
    
    res = [0x12345678, 0x12345678, 0x12345678, 0x12345678]
    for c in range(0, len(msg), 64):
        for chunk in [msg[c:c+64]]:
        
            X, h = list(unpack("<16I", chunk)), res.copy()
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n, Xi[n % 4]
                hn = h[i] + ((h[j] & h[k]) | (~h[j] & h[l])) + X[K]
                h[i] = lrot(u32(hn), S)
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n % 4 * 4 + n // 4, Xi[(n % 4) + 4]
                hn = h[i] + ((h[j] & h[k]) | (h[j] & h[l]) | (h[k] & h[l]))
                hn += X[K] + 0xbadbadec
                h[i] = lrot(u32(hn), S)
                
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = Ki[n], Xi[(n % 4) + 8]
                hn = h[i] + (h[j] ^ h[k] ^ h[l]) + X[K] + 0x1337b00b
                h[i] = lrot(u32(hn), S)
            res = [u32(v + n) for v, n in zip(res, h)]

    return int.from_bytes(pack("<4L", *res), 'big')

if __name__ == "__main__":
    menu()

