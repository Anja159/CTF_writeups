## Fast Carmichael (Crypto, easy)

We get a python [program](server.py)

By looking at this part of the program we can see that it outputs the flag only if the input number passes the Miller-Rabin primality test, but it’s not actually a prime number. 

```python
def _isPrime(p):
    ...
    if not millerRabin(p, 300):
        return False
    return True

if _isPrime(p) and not isPrime(p):
        sendMessage(s, FLAG)
 ```

This only happens if the number is a strong pseudoprime for the given set of bases. In our case, our number has to satisfy the bases of all prime numbers smaller than 300 (a total of 62 prime numbers).  I found a few examples of such numbers online, and supposedly there also exists some software to generate them.

An example of a strong pseudoprime:
`2887148238050771212671429597130393991977609459279722700926516024197432303799152733116328983144639225941977803110929349655578418949441740933805615113979999421542416933972905423711002751042080134966731755152859226962916775325475044445856101949404200039904432116776619949629539250452698719329070373564032273701278453899126120309244841494728976885406024976768122077071687938121709811322297802059565867`

If we send this number to the server we get the flag: `HTB{c42m1ch431_num8325_423_fun_p53ud0p21m35}`