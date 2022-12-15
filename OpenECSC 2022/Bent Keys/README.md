## Be An Oracle (Web-Crypto, hard)

We are given a server we can connect to. 
First we run the command `'openssl s_client -connect 152.96.7.2:8443'` in terminal. The results show that the server could be TLS vulnerable.  We can use a TLS-Attacker tool to scan for vulnerabilities. It turns out that the server is vulnerable to invalid curve attack.

TLS-Attacker can also be used to attack, so we run it. After some time it prints out the private key, which has to be saved into a file private.key. 

Private key: `MEECAQAwEwYHKoZIzj0CAQYIKoZIzj0DAQcEJzAlAgEBBCAKdMqpHYIjXHdgUSTirDBfpkD7zw2ktsS7YfhcKr+TwQ==`

The only thing we still need is the public key. It can be obtained by running command `'openssl s_client -connect 152.96.7.2:8443 | openssl x509 -pubkey -noout'`, and save it to the file public.key. 

Public key:
`MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEd/F3OeGTaZcfeQ3GEYV0f6V6DNrU2chTrbPmt0ygKYyBYH+JGacPr39Z4N5Vh4jc71gnIcyHr2kzrXCxb8rxKw==`

Now that we have both keys we only need to run the command:
`openssl pkeyutl -derive -inkey private.key -peerkey public.key | sha1sum`

The flag is the sha1sum: `e7bf2f86896ebbd5795336dc5a2d901c4dbfd714`

