## One Trick Pony (Crypto, easy)
### The source
We are given a c program file:
```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
    char* secret_msg = "<redacted>";
    size_t msg_len = strlen(secret_msg);


    unsigned char* random_bytes = malloc(msg_len);
    for (size_t i = 0; i < msg_len; i++) {
        random_bytes[i] = rand();
    }

    unsigned char* enc = malloc(msg_len);
    for (size_t i = 0; i < msg_len; i++) {
        enc[i] = secret_msg[i] ^ random_bytes[i];
    }

    printf("This is my message to you: ");
    for (size_t i = 0; i < msg_len; i++) {
        printf("%02X", enc[i]);
    }
    printf("\n");
}
```

#### Solution
From the source we can see that bytes of the flag are XORed with some random bytes. We notice that rand() is unseeded, that means it always produces the same byte sequence.

If we connect to the server we get the XORed flag:
```bash
 33AE0C532293259809A0DBC89A928D235CAB3AD86F8082AD15355C0D56EDE9F207412DC64431D73F053B6461379B3FB6C7D7EDA9FFD0273F2ED61C28521DB1EE17814A8124808E091E7811E2CAAF04FBEA183F4285C048DB46C01C279879A928226D973793C08A71B87D979D76544CE119BCE109BD8F39E4DDEA3CF1EEDFAEC036DC937D
```
Our string is 264 characters long,  that means we need to produce (at least) 132 random bytes. This is the function used to produce them:
```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
    int n = 132;
    unsigned char* random_bytes = malloc(n);
    for (size_t i = 0; i < n; i++) {
        random_bytes[i] = rand();
        printf("%02X", random_bytes[i]);
    }
}
```
The output of this function is:
```bash
67C6697351FF4AEC29CDBAABF2FBE3467CC254F81BE8E78D765A2E63339FC99A66320DB73158A35A255D051758E95ED4ABB2CDC69BB454110E827441213DDC8770E93EA141E1FC673E017E97EADC6B968F385C2AECB03BFB32AF3C54EC18DB5C021AFE43FBFAAA3AFB29D1E6053C7C9475D8BE6189F95CBBA8990F95B1EBF1B305EFF700
```
The only thing left is to XOR them together (in python):
```python
from pwn import *
from Crypto.Util.number import *

random = 0x67C6697351FF4AEC29CDBAABF2FBE3467CC254F81BE8E78D765A2E63339FC99A66320DB73158A35A255D051758E95ED4ABB2CDC69BB454110E827441213DDC8770E93EA141E1FC673E017E97EADC6B968F385C2AECB03BFB32AF3C54EC18DB5C021AFE43FBFAAA3AFB29D1E6053C7C9475D8BE6189F95CBBA8990F95B1EBF1B305EFF700
output = 0x33AE0C532293259809A0DBC89A928D235CAB3AD86F8082AD15355C0D56EDE9F207412DC64431D73F053B6461379B3FB6C7D7EDA9FFD0273F2ED61C28521DB1EE17814A8124808E091E7811E2CAAF04FBEA183F4285C048DB46C01C279879A928226D973793C08A71B87D979D76544CE119BCE109BD8F39E4DDEA3CF1EEDFAEC036DC937D

print(long_to_bytes((random ^ output)))
```

And the output is: `'The slot machine in the corner has quite favorable odds. This might earn you some chips to start with: KCTF{sh0uld_h4ve_us3d_4_s33d}'`
