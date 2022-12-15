## Crooked roulette (Crypto, easy)

#### Source code analysis
We are given the Python source code of the [server](Crooked_Roulette.py). From the source code we can see that the server uses standard textbook RSA scheme. 

If we connect to the server it prints out the modulus n and the desired roulette result (which is a random intenger 256 bits long).
```python
result = getRandomInteger(256)
print(f"Number of pockets: {hex(n)}")
print(f"The Manager told me, the roulette is crooked and will hit {hex(result)}")
```
Then we can send three strings the server. For the first one we can choose any hex string, which will be signed by the server function (`sign = pow(input, d, n)`) and printed out. The input will be signed only if `input % n` doesn't equal `result`.

We also need to send a message which has to be equal to the value of result and the signature of this same message. If the signature is correct we get the flag.
```python
message = int(input(f"What do you want to bet? "), base)
    signature = int(input(f"Please sign your bet "), base)
    if result == message and check(signature, message):
        print(f"You Win: {flag}")
```
#### Solution

We know that in RSA **pow(pow(message,d,n),e,n) == message**.
```python
def check(c, m):
    return pow(c, e, n) == m
if result == message and check(signature, message):
        print(f"You Win: {flag}")
```
So if we want the above `check` function to return true, signature would have to equal `pow(result,d,n)`. The only problem is we cannot directly sign the result value, as the server restricts us from signing anything that would equal result if divided by module n. 

We find a way to bypass it through this equality `sign(result) == -1*sign(-1*result)`. This can be made because d is always odd, so $(-1)^{d}$ == $-1$ will always hold true.

The answers to the questions should follow each other in this order:
1. _What should I bet?_ -> Let the server sign `-1*result` and obtain `sign(-result)`
2. _What do you want to bet?_ -> We send the value of `result`
3. _Please sign your bet_ -> We send the value `-1*sign(-result)`

Solution script in python:
```python
from pwn import *
r = remote("kitctf.me", 4545)

n = str(r.recvline()).split(" ")[3][:258]
result = str(r.recvline()).split(" ")[11][:66]

r.sendline("-"+result) # What should I bet?
signature = str(r.recvline()).split(" ")[7][:258]

r.sendline(result) # What do you want to bet?
r.sendline("-"+signature) # Please sign your bet
print(r.recvline())
```

And the flag was: `KITCTF{1nvers4_need_n0_k4y_101492}`