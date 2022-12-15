## Dump3 (Forensics, medium)

#### Questions
1. What OS was the machine running? 
2. How many processes were running in the machine? (result = int)
3. What is the SHA-1 of /var/run/utx.active
4. What user is logged in graphical desktop? 
5. What file was used as desktop background (full path)?
6. What flag was on the screen?

#### Solution

At first I analysed the .bin file with strings command and I found the OS which the dump was captured from. It is `FreeBSD 12.3-RELEASE`. I also used strings and grep to find the user `»pampa«` and the background image `»/home/pampa/.background.gif«`.

To obtain the number of processes I used volatility. Because volatility doesn't have this profile we have to create our own. I set up a virtual machine in Virtualbox and downloaded the FreeBSD iso file to set it up. Then I created a custom volatility profile and captured the kernel. Then I transferred the zip and set up the volatility on host. By running »pslist« command I saw all the processes and counted them, there were `68` of them.

The sha1sum of utx.acitve can be found by knowing the hex header of utx.active file on my VM 01/00/05. Then I searched the dump file for the header, which must be followed by »pampa« string (as this is the user, and utx.active includes users). I found out that one user entry is 179 bytes, and there are four, so the full length is 788 bytes. At last I extracted the hex data and hashed it with sha1.

For the last part I figured out the flag could be in the background .gif file. So I looked up the gif header and searched for it in hexdump. There was only one in the right format, then I downloaded the hex file. It is an image of a barcode. I scanned with an online scanner and got an UUID – `c7b42f16-b904-429d-8abb-90fcaedc91fa`.

And then we run the below to get the flag 
```bash
echo -n "FreeBSD 12.3-RELEASE:68:3a62d3098f8ba55e1f7a190a95d814cf24dc031c:pampa:/home/pampa/.background.gif:c7b42f16-b904-429d-8abb-90fcaedc91fa" | tr '[:upper:]' '[:lower:]' | md5sum
``` 
