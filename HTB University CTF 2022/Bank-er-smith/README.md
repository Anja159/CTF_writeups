## Bank-er-smith (Crypto, easy)

I managed to get first blood on this one🩸

We are given the Python source code of the [server](server.py):

```python
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse, GCD
from secret import FLAG, KEY

WELCOME = """
************** Welcome to the Gringatts Bank. **************
*                                                          *
*                  Fortius Quo Fidelius                    *
*                                                          *
************************************************************
"""


class RSA():

    def __init__(self, key_length):
        self.e = 0x10001
        phi = 0
        prime_length = key_length // 2

        while GCD(self.e, phi) != 1:
            self.p, self.q = getPrime(prime_length), getPrime(prime_length)
            phi = (self.p - 1) * (self.q - 1)
            self.n = self.p * self.q

        self.d = inverse(self.e, phi)

    def encrypt(self, message):
        message = bytes_to_long(message)
        return pow(message, self.e, self.n)

    def decrypt(self, encrypted_message):
        message = pow(encrypted_message, self.d, self.n)
        return long_to_bytes(message)


class Bank:

    def __init__(self, rsa):
        self.options = "[1] Get public certificate.\n[2] Calculate Hint.\n[3] Unlock Vault.\n"  
        self.shift = 256
        self.vaults = {
            f"vault_{i}": [b"passphrase", b"empty"]
            for i in range(100)
        }
        self.rsa = rsa

    def initializeVault(self, name, passphrase, data):
        self.vaults[name][0] = passphrase
        self.vaults[name][1] = data

    def calculateHint(self):
        return (self.rsa.p >> self.shift) << self.shift

    def enterVault(self, vault, passphrase):
        vault = self.vaults[vault]
        if passphrase.encode() == vault[0]:
            return vault[1].decode()
        else:
            print("\nFailed to open the vault!\n")
            exit(1)


if __name__ == "__main__":
    rsa = RSA(2048)
    bank = Bank(rsa)

    vault = "vault_68"
    passphrase = KEY
    bank.initializeVault(vault, passphrase, FLAG)

    encrypted_passphrase = rsa.encrypt(bank.vaults[vault][0])
    print(f"You managed to retrieve: {hex(encrypted_passphrase)[2:]}")
    print("\nNow you are ready to enter the bank.")
    print(WELCOME)

    while True:
        try:
            print("Hello, what would you like to do?\n")
            print(bank.options)
            option = int(input("> "))

            if option == 1:
                print(f"\n{bank.rsa.n}\n{bank.rsa.e}\n")
            elif option == 2:
                print(f"\n{bank.calculateHint()}\n")
            elif option == 3:
                vault = input("\nWhich vault would you like to open: ")
                passphrase = input("Enter the passphrase: ")
                print(f"\n{bank.enterVault(vault, passphrase)}\n")
            else:
                "Abort mission!"
                exit(1)
        except KeyboardInterrupt:
            print("Exiting")
            exit(1)
        except Exception as e:
            print(f"An error occurred while processing data: {e}")
            exit(1)
```

#### Source code analysis

Upon further inspection we notice the server uses RSA encryption. It creates a vault, which stores the FLAG, with an identifier `"vault_68"` and sets the key KEY as its password. The key is later encrypted with RSA under the name encrypted_passphrase. If we want to access the flag we need to decrypt the password which unlocks the vault.

```python
vault = "vault_68"
passphrase = KEY

bank.initializeVault(vault, passphrase, FLAG)
encrypted_passphrase = rsa.encrypt(bank.vaults[vault][0])
```
The server gives us three options to choose from:
1. Get public certificate (public RSA key, parameters n and e)
2. Calculate Hint
3. Unlock Vault

```python
if option == 1:
    print(f"\n{bank.rsa.n}\n{bank.rsa.e}\n")
elif option == 2:
    print(f"\n{bank.calculateHint()}\n")
elif option == 3:
    vault = input("\nWhich vault would you like to open: ")
    passphrase = input("Enter the passphrase: ")
    print(f"\n{bank.enterVault(vault, passphrase)}\n")
```

By looking at the hint function we can see that the function shifts p 256 bits to the right and then back. We know 768 most significant bits out of 1024 of prime number p. 

```python
self.shift = 256
...
def calculateHint(self):
        return (self.rsa.p >> self.shift) << self.shift
```

### Solution

We are going to use the Coppersmith attack to get the rest of the bits of p. 
Lets assume a are the known bits of p. With this value of a, the polynomial **f(x) = a + x** 
has a small root r modulo p, where r is the least significant 256 bits of p. This means that both, f(x) and N are divisible by p, and of course also any multiple or power of f(x).
The lattice we construct satisfies that every vector is zero mod p. Applying LLL we will get a small element of that lattice which matches r.

Here is how we set up the lattice in Sage:

```python
N = <N from public key>
a = <hint>

X = 2^256
M = matrix([[X^2, 2*X*a, a^2], [0, X, a], [0, 0, N]])
B = M.LLL()
Q = B[0][0]*x^2/X^2+B[0][1]*x/X+B[0][2]

p = a+Q.roots(ring=ZZ)[0][0]
```
We take the needed paramaters from the server:

```bash
$ nc 178.62.21.211 31474
You managed to retrieve: 6e03e9795ba67e61b92fd8dd7732bc48866d3dc1bbf4f5fa6a01d0445cb2b0f6c099a2ab186e884be5fae0086bd8246c138729fe0bdaa010777dbafc45b960e624fcac162a2cafdd63b03be210d5cb3fe63beb7099be1d52a5fb9f688f0a77256fe09bf765450a9e79a36d58519e120104cb9f9409514c80bf8d6ac5097c16bd7a6c43f8afa4bde2c2cb6de421a7d5dc4d71d564af934d4dddedb6adf39ba5ac0e8ed1d9fd2beff76f69ba1c9d1875e07566ff588f0fbeaede0b628683d6dfbd9037fd15b3c84128dd5b659eac9c2939ebd0f5b7d0c826aec270be131d384bdf18dd9154e92d357cad2da0d422efbbfcd28173824a511ebed608e3e2d19cf495

Now you are ready to enter the bank.

************** Welcome to the Gringatts Bank. **************
*                                                          *
*                  Fortius Quo Fidelius                    *
*                                                          *
************************************************************

Hello, what would you like to do?

[1] Get public certificate.
[2] Calculate Hint.
[3] Unlock Vault.

> 1

26272664590454787317352428900080135303036824329225668215899235395498371297220608915287247882099527866486908073714840896632505356593849938005661416313626842832910157870436577746226539583105246910746160039315084401138202814320559979029681260701154933068691946494411441272586267469555487746306431018592741482920298785785255459140818521237201072165071775175131477347714978523756346220471825385097972523551714989714821491387719163336371620584125033335582245505841966988256943130882728184301092573790447077431924690832924860672052042187861402010412129161498191219460963008705942492258678022361012754018835298970470223897723  
65537

Hello, what would you like to do?

[1] Get public certificate.
[2] Calculate Hint.
[3] Unlock Vault.

> 2

165827368659014322049070097492184363669461448162202433107877051902713529917252355235212811191092876543125397226502677845569204467693133285626314402419242502597722363061603851825594894065632491081621172917189807107692715075418759526342409775702830301217139670416277399241044094329521480527431296677621650161664
```

The sage solution looks like this:

```python
N = 26272664590454787317352428900080135303036824329225668215899235395498371297220608915287247882099527866486908073714840896632505356593849938005661416313626842832910157870436577746226539583105246910746160039315084401138202814320559979029681260701154933068691946494411441272586267469555487746306431018592741482920298785785255459140818521237201072165071775175131477347714978523756346220471825385097972523551714989714821491387719163336371620584125033335582245505841966988256943130882728184301092573790447077431924690832924860672052042187861402010412129161498191219460963008705942492258678022361012754018835298970470223897723
a = 165827368659014322049070097492184363669461448162202433107877051902713529917252355235212811191092876543125397226502677845569204467693133285626314402419242502597722363061603851825594894065632491081621172917189807107692715075418759526342409775702830301217139670416277399241044094329521480527431296677621650161664

X = 2^256
M = matrix([[X^2, 2*X*a, a^2], [0, X, a], [0, 0, N]])
B = M.LLL()
Q = B[0][0]*x^2/X^2+B[0][1]*x/X+B[0][2]

p = a+Q.roots(ring=ZZ)[0][0]
print(p)
```

Now that we have all the required parameters we can also write the final solution script in python (or sage):

```python
from Crypto.Util.number import long_to_bytes

N = 26272664590454787317352428900080135303036824329225668215899235395498371297220608915287247882099527866486908073714840896632505356593849938005661416313626842832910157870436577746226539583105246910746160039315084401138202814320559979029681260701154933068691946494411441272586267469555487746306431018592741482920298785785255459140818521237201072165071775175131477347714978523756346220471825385097972523551714989714821491387719163336371620584125033335582245505841966988256943130882728184301092573790447077431924690832924860672052042187861402010412129161498191219460963008705942492258678022361012754018835298970470223897723
p = 165827368659014322049070097492184363669461448162202433107877051902713529917252355235212811191092876543125397226502677845569204467693133285626314402419242502597722363061603851825594894065632491081621172917189807107692715075418759526371940664692344449730544565326144150720049589472795369462748074425394212260139
e = 65537
ciphertext = 0x6e03e9795ba67e61b92fd8dd7732bc48866d3dc1bbf4f5fa6a01d0445cb2b0f6c099a2ab186e884be5fae0086bd8246c138729fe0bdaa010777dbafc45b960e624fcac162a2cafdd63b03be210d5cb3fe63beb7099be1d52a5fb9f688f0a77256fe09bf765450a9e79a36d58519e120104cb9f9409514c80bf8d6ac5097c16bd7a6c43f8afa4bde2c2cb6de421a7d5dc4d71d564af934d4dddedb6adf39ba5ac0e8ed1d9fd2beff76f69ba1c9d1875e07566ff588f0fbeaede0b628683d6dfbd9037fd15b3c84128dd5b659eac9c2939ebd0f5b7d0c826aec270be131d384bdf18dd9154e92d357cad2da0d422efbbfcd28173824a511ebed608e3e2d19cf495

q = N // p
phi = (p-1)*(q-1)
d = pow(e, -1, phi)

password = long_to_bytes(pow(ciphertext, d, N))
print(password)
```

The password we retrieve is **The_horcrux_is_Helga_Hufflepuff's_cup**. If we choose the third option and log in with the vault_name: "vault_68" and passphrase: "The_horcrux_is_Helga_Hufflepuff's_cup", we get the following flag `HTB{LLL_4nd_c00p325m17h_15_57111_m491c_70_my_3y35}`.
