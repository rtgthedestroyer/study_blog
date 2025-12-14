+++
date = '2025-12-14T23:42:45+02:00'
draft = false
title = 'Random'
+++
# Random


lets run this program
it asks us for a key , we get it wrong and it wants us to bruteforce is 2^32 times..
lol how about no, lets read the source code

### source code analysis

```c

#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

	unsigned int key=0;
	scanf("%d", &key);

	if( (key ^ random) == 0xcafebabe ){
		printf("Good!\n");
		setregid(getegid(), getegid());
		system("/bin/cat flag");
		return 0;
	}

	printf("Wrong, maybe you should try 2^32 cases.\n");
	return 0;
}
```
random() is psuedorandom because you can predict its next value
from the man
"If no seed value is provided, the random() function is automatically seeded  with  a
       value of 1."
therefore the random value will be "1804289383",
we need an input that when we xor it with 1804289383 we get 0xcafebabe
well xor is reversible so lets find the desired input,

```python

known_val = 1804289383

target = 0xcafebabe

x = known_val ^ target

print(f"Decimal: {x}")
print(f"Hex:     {hex(x)}")

```
we run the program with the output and we get the flag
m0mmy_I_can_predict_rand0m_****