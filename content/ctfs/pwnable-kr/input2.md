+++
date = '2025-12-15T11:37:19+02:00'
draft = false
title = 'Input2'
+++

# Input2 

Let's begin by running the program
seem's like we cant get an input directly to the program 
the ctf description gives us a hint "how can i pass my input into a computer program?"
...
lets look at the source code

### source code analysis

```c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
	printf("Welcome to pwnable.kr\n");
	printf("Let's see if you know how to give input to program\n");
	printf("Just give me correct inputs then you will get the flag :)\n");

	// argv
	if(argc != 100) return 0;
	if(strcmp(argv['A'],"\x00")) return 0;
	if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
	printf("Stage 1 clear!\n");	

	// stdio
	char buf[4];
	read(0, buf, 4);
	if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
	read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
	printf("Stage 2 clear!\n");
	
	// env
	if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
	printf("Stage 3 clear!\n");

	// file
	FILE* fp = fopen("\x0a", "r");
	if(!fp) return 0;
	if( fread(buf, 4, 1, fp)!=1 ) return 0;
	if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
	fclose(fp);
	printf("Stage 4 clear!\n");	

	// network
	int sd, cd;
	struct sockaddr_in saddr, caddr;
	sd = socket(AF_INET, SOCK_STREAM, 0);
	if(sd == -1){
		printf("socket error, tell admin\n");
		return 0;
	}
	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons( atoi(argv['C']) );
	if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
		printf("bind error, use another port\n");
    		return 1;
	}
	listen(sd, 1);
	int c = sizeof(struct sockaddr_in);
	cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
	if(cd < 0){
		printf("accept error, tell admin\n");
		return 0;
	}
	if( recv(cd, buf, 4, 0) != 4 ) return 0;
	if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
	printf("Stage 5 clear!\n");

	// here's your flag
	setregid(getegid(), getegid());
	system("/bin/cat flag");	
	return 0;
}

```
Our goal is to get the flag.. seems like we need to clear stages to pass each filter,
stage,


### stage 1

```c
// argv
	if(argc != 100) return 0;
	if(strcmp(argv['A'],"\x00")) return 0;
	if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
	printf("Stage 1 clear!\n");	
```
we need an argc of 100 , argv['A'] aka argv[0x41]="\x00"
and argv['B'] aka argv[0x42] = "\0x20\x0a\x0d"
lets try it :

```python
from pwn import *

executable = './input2'

# satisfy argc = 100

argv = [executable] * 100

# satisfy argv['A'] (Index 65)

argv[ord('A')] = ""

#sastisfy argv['B']
argv[ord('B')] = "\x20\x0a\x0d"


p = process(argv, executable=executable)

try:
    print(p.recv()) 
except EOFError:
    print("Process died unexpectedly. Arguments might be wrong.")

```

lets move on to stage 2

### stage 2

```c
// stdio
	char buf[4];
	read(0, buf, 4);
	if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
	read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
	printf("Stage 2 clear!\n");
```

we now read from standard input (fd=0) 4 bytes into the buffer buf[4]
it compares the buffer to \0x00\0x0a\0x00\0xff .. and then reads from stedrror , we need to write to stderr somehow the value \x00\x0a\x02\xff how do we that ?

using the os module in python we can create a read/write pipe into sterror

```python
p = process(argv, executable=executable,stderr=r_pipe)

stage2_payload1 = b"\x00\x0a\x00\xff" # first check in stage 2

# Check if we passed Stage 1
try:
    print(p.recv()) 
except EOFError:
    print("Process died unexpectedly. Arguments might be wrong.")

p.send(stage2_payload1)

stage2_payload2 = b"\x00\x0a\x02\xff" #second payload for stage 2 (read into stderror)
os.write(w_pipe,stage2_payload2)

#check for stage 2
try:
    print(p.recv())
except EOFError:
    print("error on stage 2")

```

adding this we sucessfuly get past stage 2

lets look at stage 3

### stage 3

```c
// env
	if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
	printf("Stage 3 clear!\n");
```

inside our pwntool script we can to the following to set an enviromental variable

```python
env_setup = {
    b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe'
}
p = process(argv, executable=executable, stderr=r_pipe, env=env_setup)
```

and... we sucessfuly cleared stage 3
moving on to stage 4

### stage 4

```c

FILE* fp = fopen("\x0a", "r");
	if(!fp) return 0;
	if( fread(buf, 4, 1, fp)!=1 ) return 0;
	if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
	fclose(fp);
	printf("Stage 4 clear!\n");
```
we need a file named \x0a to read from then read to a buffer and check if the values we
read into the buffer are \x00\x00\x00\x00
lets add the neceseary steps into our pwntools script
this stage was a little more tricky as we dont have permission to r/w in the correct directory, so we have to create a new file in temp while also running the correct executable from the right directory
after a lil bit of research i managed to make it work

```python
os.chdir('/tmp') # move into the temp directory
executable = "/home/input2/input2" #absolute path to the directory

```
we now succesfuly solved stage 4
lets move on

### stage 5

```c
	// network
	int sd, cd;
	struct sockaddr_in saddr, caddr;
	sd = socket(AF_INET, SOCK_STREAM, 0);
	if(sd == -1){
		printf("socket error, tell admin\n");
		return 0;
	}
	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons( atoi(argv['C']) );
	if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
		printf("bind error, use another port\n");
    		return 1;
	}
	listen(sd, 1);
	int c = sizeof(struct sockaddr_in);
	cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
	if(cd < 0){
		printf("accept error, tell admin\n");
		return 0;
	}
	if( recv(cd, buf, 4, 0) != 4 ) return 0;
	if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
	printf("Stage 5 clear!\n");

	// here's your flag
	setregid(getegid(), getegid());
	system("/bin/cat flag");	
	return 0;
```
this uses socket programming, first we create a standard af_inet address , tcp ipv4 socket
we gotta pass a port on arv['C'] and connect to the server and send the payload \xde\xed\xbe\xef

the final script is

```python

from pwn import *
import os
import time

#so we can read/write/ex new files
os.chdir('/tmp')
target_port = "55555" #port for socket

executable = './input2'
r_pipe,w_pipe = os.pipe() # so we can write to stderr
env_setup = {
    b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe' #to setup the env variable for stage3
}
new_filename=b"\x0a"
file_content=b"\x00\x00\x00\x00"
executable = "/home/input2/input2"
 #satisfy argc = 100
# we create a list of 100 items. 
# Index 0 is the executable name. The rest are filler.
argv = [executable] * 100

# satisfy argv['A'] (Index 65)
# strcmp(argv['A'], "\x00") checks for an empty string.
argv[ord('A')] = ""

argv[ord('C')] = target_port
# stisfy argv['B'] (Index 66)
# needs to be \x20\x0a\x0d
argv[ord('B')] = "\x20\x0a\x0d"

with open(new_filename,"wb") as f:
    f.write(file_content)
#check for stage 2
# 4. Spawn the process with this specific environment
p = process(argv, executable=executable,stderr=r_pipe,env=env_setup)

stage2_payload1 = b"\x00\x0a\x00\xff"


#so we can read the flag after we solve this challenge otherwise we
#will not get anything since our program launches from /tmp
try:
    os.symlink("/home/input2/flag","/tmp/flag")
except FileExistsError:
    pass



try:
    print(p.recv()) 
except EOFError:
    print("Process died unexpectedly. Arguments might be wrong.")

p.send(stage2_payload1)

stage2_payload2 = b"\x00\x0a\x02\xff"
os.write(w_pipe,stage2_payload2)
#for the last stage
print('server is starting')

time.sleep(1)

try:
    conn = remote('localhost',int(target_port))
    conn.send(b"\xde\xad\xbe\xef")
    conn.close()
    print("sent packet")

except Exception as e:
    printf(f"network faile {e}")

print(p.recvall().decode())

```
this is was a little bit messy.. but we got the flag
Mommy_now_I_know_how_to_pa5s_inputs_*******