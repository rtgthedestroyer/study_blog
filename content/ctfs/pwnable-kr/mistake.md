+++
date = '2025-12-17T18:50:12+02:00'
draft = false
title = 'Mistake'
+++
# pwnable.kr - Mistake

"We all make mistakes, let's move on.
(don't take this too seriously, no fancy hacking skill is required at all)
This task is based on real event"

we run the binary we basicaly get asked for a password after some waiting time.
lets look at the code


### source code analysis :

```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
	int i;
	for(i=0; i<len; i++){
		s[i] ^= XORKEY;
	}
}

int main(int argc, char* argv[]){
	
	int fd;
	if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}

	printf("do not bruteforce...\n");
	sleep(time(0)%20);

	char pw_buf[PW_LEN+1]; //11
	int len;
	if(!(len=read(fd,pw_buf,PW_LEN) > 0)){ //read from password
		printf("read error\n");
		close(fd);
		return 0;		
	}

	char pw_buf2[PW_LEN+1]; //11
	printf("input password : ");
	scanf("%10s", pw_buf2);

	// xor your input
	xor(pw_buf2, 10);

	if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
		printf("Password OK\n");
		setregid(getegid(), getegid());
		system("/bin/cat flag\n");
	}
	else{
		printf("Wrong Password\n");
	}

	close(fd);
	return 0;
}
```
as always we want to get the flag,
in order to get it we need to pass a few "checkpoints"

the first if block checks if we can get an fd successfuly and if the user has read permission aka 00400 symbolic constant (read the man),

```c
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}
```
    this is the problem in this if block '<' runs before '='
    so if open returns 3 then 3<0 is evaluated which is then 0
    so fd gets assigned 0
    fd = 0 is our standard input
    we read the password from our input
    now we just need a second input that when XORed by one matches
    the original password
    xoring by 1 actually does the following thing:
    if youre even then you get n+1
    if youre odd then you get n-1

    lets set the password to "1111111111"
    then our input must be "0000000000"

"do not bruteforce...
1111111111
input password : 0000000000
Password OK"

and we get the flag Mommy_the_0perator_priority_confuse*****