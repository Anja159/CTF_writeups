import sys
import typing
import random
import time
import os

from helpers import is_prime, inv
from flag import flag

KEYSIZE = 1024


def validate_answer(answer: bytes) -> bytes:
    vals = []
    key = bytes.fromhex('0' * (len(answer) % 2) + str(answer, 'ascii'))

    pos = 0
    for typ in [48] + [2]*9:
        if key[pos] != typ or len(key[pos:]) < 2:
            return b'Error decoding your key'

        ln = 0
        pos += 1
        if ~key[pos] & 0x80:
            ln = int(key[pos])
        else:
            if (num := key[pos] & 0x7f) == 0x7f or len(key[pos:]) <= num:
                return b'Error decoding your key'
            last = pos + num
            while pos < last:
                pos += 1
                ln = (ln * 256) + int(key[pos])

        pos += 1
        if len(key[pos:]) < ln:
            return b'Error decoding your key'

        if typ == 48:
            key = key[pos:pos+ln]
            pos = 0
        else:
            vals.append(int.from_bytes(key[pos:pos+ln], "big", signed=True))
            pos += ln

    if pos != len(key):
        return b'Error decoding your key'

    q = gen_prime(KEYSIZE // 2 - KEYSIZE // 16)
    p = gen_prime(KEYSIZE // 2 + KEYSIZE // 16, q)
    phi = (p-1) * (q-1)
    e = 65337

    while True:
        d = inv(e, phi)
        if d and ((e * d) % phi) == 1:
            break
        e = gen_prime(16)

    m = pow(pow(int.from_bytes(flag, 'big'), e, p * q), vals[3], vals[1])
    return m.to_bytes((m.bit_length() + 7) // 8, 'big')


seed = (int(time.time()) & 0xfffffff0) + (os.getpid() & 0x65)
random.seed(seed)


def gen_prime(bits: int, mn: int=0) -> int:
    while True:
        r = random.getrandbits(bits)
        r |= (1 << bits - 1) | 1
        if r > mn and is_prime(r):
            return r
