+++
date = '2025-12-18T00:14:57+02:00'
draft = false
title = 'Coin1'
+++

pwnable.kr - Coin

"Mommy, I wanna play a game!"
"nc 0 9007 to get flag!"


```obdjump
    ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------

        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 60 seconds.

        - How to play -
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer

        - Example -
        [Server] N=4 C=2        # find counterfeit among 4 coins with 2 trial
        [Client] 0 1            # weigh first and second coin
        [Server] 20                     # scale result : 20
        [Client] 3                      # weigh fourth coin
        [Server] 10                     # scale result : 10
        [Client] 2                      # counterfeit coin is third!
        [Server] Correct!

        - Ready? starting in 3 sec... -
```
we are in some kind of a mini-game lets probe our way out

when i give an input of strings we get format error,
when i give input of a long string/number we get format error as well.

i cant seem a way to solve this so how about we play the game so fast to solve it 100 times,
in order to do that lets create script that utilizes binary search,
if the wight from 1 to n is odd then continue at n/2
else do n+m/2

```python
ffrom pwn import *

r = remote('localhost', 9007)

r.recvuntil(b'3 sec... -')
r.recvline()

for i in range(100):
    r.recvuntil(b'N=')
    N = int(r.recvuntil(b' ')[:-1])
    
    r.recvuntil(b'C=')
    C = int(r.recvuntil(b'\n')[:-1])
    
    low = 0
    high = N - 1
    
    for _ in range(C):
        mid = (low + high) // 2
        
        if low < high:
            query_list = [str(x) for x in range(low, mid + 1)]
            payload = ' '.join(query_list)
        else:
            payload = str(low)
        
        r.sendline(payload.encode())
        
        result = r.recvline().decode().strip()
        weight = int(result)
        
        if low < high:
            expected_weight = len(query_list) * 10
            if weight == expected_weight:
                low = mid + 1
            else:
                high = mid
    
    r.sendline(str(low).encode())
    r.recvline()

r.interactive()
```

basicaly we just found a more efficient game to bruteforce the game using binary search which as you know
its O-notation is O(logn) compared to normal
sort -> find which is O(n^2)