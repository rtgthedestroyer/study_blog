+++
date = '2025-12-13T22:56:24+02:00'
draft = false
title = 'Collision'
+++
### Coliision
the 2nd challenge in toddler's bottle
as the description says the hint is about md5 collisions lets seew what we have:
### source code analysis:

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
c

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		setregid(getegid(), getegid());
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```
Our goal here is to get the flag, in order to get the flag we need the hashcode to be equal to our input after its encoded by the check_password() function , we see that  our input should be at least 20 bytes.

about md5, i researched a bit, 
first what is a collision?
in cryptography, a collision occurs when two distinct inputs produce the exact same output hash. For MD5, which generates a 128-bit fingerprint, for now there is no need to dive into the math behind it, MD5 is no longer used as it is considered "broken" thus unsafe to use.

what check_password() does is basicaly it sums up our input array it converted our string into int so 20 bytes into 5 integers and sums it up , our goal is for it to be equal to the hashcode.

for example if your input p is "AAAABBBBCCCCDDDDEEEE":
Chunk 0: Takes "AAAA" $\rightarrow$ converts to integer 0x41414141.

Chunk 1: Takes "BBBB" $\rightarrow$ converts to integer 0x42424242....

and so on up to 20 characters.

Result: The sum of those hex values.

our goal is to find 5 values that their sum will be:
hashcode = 0x21DD09EC

using this pwntools script we managed to get the flag


```python

from pwn import *
import sys

#connect to remote process
s = ssh(user='col',host='pwnable.kr',port=2222,password='guest')

#what we need to achieve
target_hash = 0x21DD09EC
count = 5

# 4 times + (1 times + the remainder)
base_val = target_hash//count
remainder = target_hash%count

payload = p32(base_val)*4
payload += p32(base_val+remainder)

p = s.process(['./col',payload])

print(p.recvall().decode())

s.close()


```
and we get the flag 

Two_hash_c****