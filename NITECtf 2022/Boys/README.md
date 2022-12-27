## Boys (Misc, easy)

This is an OSINT challenge, for starter we are only given a github username **sk1nnywh1t3k1d**. We search for the user, which only has one repository named **chat-app**. If we look at the past commits, we notice something written in the file chat.txt, which countains a link bit.ly/voughtencrypted that redirects us to a mega.nz folder.  The folder contains [the following](secret_message.wav) wav file. We open it with Audacity and add spectogram to get the following message:

![spec](spec.png)

Each part of the string separated by spaces in `thguovdne hsals drawrof yl tod tib` can be rearranged into a word. The result is `endvought slash forward ly dot bit`. We then have mix the words to get a valid bit.ly link **bit.ly/endvought**. The link again redirects us to a mega.nz folder, which contains an image. 

![email.png](email.png)

Inspecting the image we notice it contains parts of a string, written in red. We can split the image in painter (or ImageMagick) and assemble the pieces.
The string is actually an email **hughiecampbell392@gmail.com**. I used the [Epieos tool](https://epieos.com/) to find possible accounts linked to this gmail address and account information. Among the results there was also a link to a presonal [gmail google calendar](https://calendar.google.com/calendar/u/0/embed?src=hughiecampbell392@gmail.com), which contains the flag: `niteCTF{v0ught_n33ds_t0_g0_d0wn}`.