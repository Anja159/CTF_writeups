## Gonna-Lift-Em-All (Crypto, easy)

We get a python  [program](server.py) and its [output](data.txt)
```python
from Crypto.Util.number import bytes_to_long, getPrime
import random

FLAG = b'HTB{??????????????????????????????????????????????????????????????????????}'

def gen_params():
  p = getPrime(1024)
  g = random.randint(2, p-2)
  x = random.randint(2, p-2)
  h = pow(g, x, p)
  return (p, g, h), x

def encrypt(pubkey):
  p, g, h = pubkey
  m = bytes_to_long(FLAG)
  y = random.randint(2, p-2)
  s = pow(h, y, p)
  return (g * y % p, m * s % p)

def main():
  pubkey, privkey = gen_params()
  c1, c2 = encrypt(pubkey)

  with open('data.txt', 'w') as f:
    f.write(f'p = {pubkey[0]}\ng = {pubkey[1]}\nh = {pubkey[2]}\n(c1, c2) = ({c1}, {c2})\n')

if __name__ == "__main__":
  main()
```

We notice that c1 = `g * y mod p`and c2  = `m * s mod p`.  We can extract y out of the first equation by using the following divideresidues function:
```python 
def divideresidues(dividend, divisor, modulus):
    r, newr = modulus, divisor
    t, newt = 0, 1
    while newr != 0:
        quotient, remainder = divmod(r, newr)
        r, newr = newr, remainder
        t, newt = newt, t - quotient * newt
    if t < 0:
        t = t + modulus
    quotient, remainder = divmod(dividend, r)
    return t * quotient % modulus
```
Once we have y, we can calculate the value of `s = pow(h, y, p)`. Next we can use the divideresidues function again to get m out of the equation `m * s mod p = c2` and we have the flag `HTB{b3_c4r3ful_wh3n_1mpl3m3n71n6_cryp705y573m5_1n_7h3_mul71pl1c471v3_6r0up}`

The solution written in python:

```python
from Crypto.Util.number import *

def divideresidues(dividend, divisor, modulus):
    r, newr = modulus, divisor
    t, newt = 0, 1
    while newr != 0:
        quotient, remainder = divmod(r, newr)
        r, newr = newr, remainder
        t, newt = newt, t - quotient * newt
    if t < 0:
        t = t + modulus
    quotient, remainder = divmod(dividend, r)
    return t * quotient % modulus

p = 163096280281091423983210248406915712517889481034858950909290409636473708049935881617682030048346215988640991054059665720267702269812372029514413149200077540372286640767440712609200928109053348791072129620291461211782445376287196340880230151621619967077864403170491990385250500736122995129377670743204192511487
g = 90013867415033815546788865683138787340981114779795027049849106735163065530238112558925433950669257882773719245540328122774485318132233380232659378189294454934415433502907419484904868579770055146403383222584313613545633012035801235443658074554570316320175379613006002500159040573384221472749392328180810282909
h = 36126929766421201592898598390796462047092189488294899467611358820068759559145016809953567417997852926385712060056759236355651329519671229503584054092862591820977252929713375230785797177168714290835111838057125364932429350418633983021165325131930984126892231131770259051468531005183584452954169653119524751729
(c1, c2) = (159888401067473505158228981260048538206997685715926404215585294103028971525122709370069002987651820789915955483297339998284909198539884370216675928669717336010990834572641551913464452325312178797916891874885912285079465823124506696494765212303264868663818171793272450116611177713890102083844049242593904824396, 119922107693874734193003422004373653093552019951764644568950336416836757753914623024010126542723403161511430245803749782677240741425557896253881748212849840746908130439957915793292025688133503007044034712413879714604088691748282035315237472061427142978538459398404960344186573668737856258157623070654311038584)

y = divideresidues(c1, g, p)
s = pow(h, y, p)
print(long_to_bytes(divideresidues(c2, s, p)))
```