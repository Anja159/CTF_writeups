## Crypto: AHS512 (Crypto, medium)

We are provided with a [server](server.py) python file that implements our own hash function. In order for the server to return the flag we need to find a string different to `"pumpkin_spice_latte"` that has the same hash value.

```python
if ((original_digest == digest) and (message != original_message)):
    sendMessage(s, f"\n{FLAG}\n") 
```
The algorithm in the file transposes, rotates and hashes (sha512) the input string. 

The value of the key, in our case, can be either 2, 4, 5 or 10 (although it also depends on the string length). I noticed that hashed values start to repeat for some permutations of the string `"pumpkin_spice_latte"`. 

So I made a short list of some of the most basic transpositions:
```python
b'pumpkin_spice_latte!'
b'piucmep_kliant_tsep!'
b'piiaunctm_etps_ekpl!'
b'pksetuip_tmnilep_ca!'
...
b'pta_cp_ipuetleisnkm!'
b'ppest_tnailk_pemcui!'
b'plpke_spte_mtcnuaii!'
b'pettal_ecips_nikpmu!'
```
and sent them to the server. This was a bit of guessing and I believe there has to be a more detailed mathematical explanation of why the collisions occur. In most cases the server returns the flag `HTB{533_7h47_w45n'7_50_5c42y_4f732_411}` for at least one of the permutations.