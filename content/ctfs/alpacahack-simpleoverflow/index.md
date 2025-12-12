+++
date = '2025-12-12T17:50:46+02:00'
draft = false
title = 'Alpacahack Simpleoverflow'
+++
# Alpacahack-simpleoverflow
### catergory : pwn
### difficulty : easy
### url : https://alpacahack.com/daily/challenges/simpleoverflow


overview : when we run the challenge we get a prompt that asks us who we are and then answers by saying youre not admin

lets look in the source code: 

```c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {

  char buf[10] = {0};
  int is_admin = 0;
  printf("name:");
  read(0, buf, 0x10);
  printf("Hello, %s\n", buf);
  if (!is_admin) {
    puts("You are not admin. bye");
  } else {
    system("/bin/cat ./flag.txt");
  }
  return 0;
}

__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(120);
}


```
we have a char buffer of 10 that is initialized to 0
after than we read from standard input 0x10 character... weird 0x10 and not 10 lets continue reading ,
we get a welcome message hello "yourname"
and if is_admin == 0 then we get a wrong answer
so this is indeed a basic buffer overflow challenge
the catch here is that instead of reading 10 chars we read 0x10 which is actually 16 in base 10 so this is very basic we just write A 11 times so we can overflow into is_admin and then we get the flag.
hope you enjoyed this little challenge

```ruby
'A'*11 solve this
```