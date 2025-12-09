+++
date = '2025-12-09T23:49:25+02:00'
draft = false
title = 'New_orleans'
+++
# New Orleans challenge

this is the second challenge on microcorruption
the first one is just a tutorial so i skipped it

!(img1.png)[img1.png]

We are greeted by this prompt as shown above
this is a fairly basic challenge i have a feeling for that
we browse the assembly code and see that there is a check_password section
lets put a break there and go  through it,

!(img2.png)[img2.png]

As we can see the password length is supposed to be 8,
and theres a loop mechanism with r14 as its index,
the intersting part is that the password validation is performed here

```c
44c2:  ee9d 0024      cmp.b	@r13, 0x2400(r14)
```
it validates something from memory which means that if we go to 
address 0x2400
we'll find the password so we did and we got it