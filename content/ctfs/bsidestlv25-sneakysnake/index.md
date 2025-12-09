+++
date = '2025-12-09T19:41:46+02:00'
draft = false
title = 'Bsidestlv25 Sneakysnake'
+++
# SneakySnake
### category : pwn
### difficulty : medium
### url : https://ctf25.bsidestlv.com/challenges#Sneaky%20Snake-92

overview :

we get a snake like game we can enter a direction and number of steps we can eat a fruit and grow our tail just like a real snake game  , we can download a file with the source code lets dive in this time we dont need to RE anything really.

```c
int main() {
    unsigned char rnd[RAND_POSITIONS];
    unsigned char flag[32 + 1];

    FILE *fp = fopen("flag.txt", "r");
    if (!fp) { fprintf(stderr, "Error: cannot open flag.txt\n"); return 1; }
    if (!fgets(flag, sizeof(flag), fp)) { fprintf(stderr, "Error: cannot read flag.txt\n"); fclose(fp); return 1; }
    fclose(fp);
    flag[strcspn(flag, "\n")] = '\0';

    // Initialize random positions
    FILE *ur = fopen("/dev/urandom", "rb");
    if (!ur) { fprintf(stderr, "Error: cannot open /dev/urandom\n"); return 1; }
    if (fread(rnd, 1, RAND_POSITIONS, ur) != RAND_POSITIONS) { fprintf(stderr, "Error: cannot read random data\n"); fclose(ur); return 1; }
    fclose(ur);
    unsigned char *ptr = rnd;

    // Initial game state
    int x = WIDTH/2, y = HEIGHT/2;
    int fruitX = *ptr % WIDTH;
    int fruitY = (*ptr / WIDTH) % HEIGHT;
    int tailX[MAX_TAIL], tailY[MAX_TAIL];
    int nTail = 0, score = 0, gameOver = 0, is_win = 0;
    enum Direction { STOP=0, LEFT, RIGHT, UP, DOWN } dir = STOP;

    // Apply state
    renderASCII(x, y, fruitX, fruitY, tailX, tailY, nTail, score);
    while (!gameOver) {
        printf("Direction [U | R | D | L]: "); fflush(stdout);
        char dch = getchar(); while (getchar()!='\n');
        switch (dch) {
            case 'U': case 'u': dir = UP; break;
            case 'D': case 'd': dir = DOWN; break;
            case 'L': case 'l': dir = LEFT; break;
            case 'R': case 'r': dir = RIGHT; break;
            default: continue;
        }
        printf("Steps: "); fflush(stdout);
        int steps = 0;
        if (scanf("%d", &steps) != 1) break;
        while (getchar()!='\n');
        // Perform steps
        for (int s = 0; s < steps && !gameOver; s++) {
            int prevX = x, prevY = y;
            switch (dir) { case LEFT: x--; break; case RIGHT: x++; break; case UP: y--; break; case DOWN: y++; break; default: break; }
            for (int i = 0; i < nTail; i++) { int tx = tailX[i], ty = tailY[i]; tailX[i] = prevX; tailY[i] = prevY; prevX = tx; prevY = ty; }
            if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) { gameOver = 1; break; }
            // for (int i = 0; i < nTail; i++) if (tailX[i]==x && tailY[i]==y) { gameOver = 1; break; }
            if (gameOver) break;
            if (x == fruitX && y == fruitY) {
                score += 10; if (nTail < MAX_TAIL) nTail++; else { gameOver = 1; break; } ptr++; fruitX = *ptr % WIDTH; fruitY = (*ptr / WIDTH) % HEIGHT;
                if (score >= WIN_SCORE) { is_win = 1; gameOver = 1; break; }
            }
        }
        // Update state
        renderASCII(x, y, fruitX, fruitY, tailX, tailY, nTail, score);
    }

    if (is_win) printf("Congratulations! You win! The flag is %s\n", flag);
    else printf("Game Over! Final score: %d\n", score);
    return 0;
}

```
in order to win this game we need to reach 100000 , we dont have time for this,
as we can see, we got a pointer that points to the buffer of the random values
which doesnt really check anything, which means we found a vector to play with
each time we eat a fruit our pointer grows by +1 , theoreticaly if we play 32 times the 33th time we will be in the flag buffer.
but the flag buffer will just be used the same way as the random buffer,
how do we know what are the characters of the flag are?

```c
// Initial game state
    int x = WIDTH/2, y = HEIGHT/2;
    int fruitX = *ptr % WIDTH;
    int fruitY = (*ptr / WIDTH) % HEIGHT;
    int tailX[MAX_TAIL], tailY[MAX_TAIL];
    int nTail = 0, score = 0, gameOver = 0, is_win = 0;
    enum Direction { STOP=0, LEFT, RIGHT, UP, DOWN } dir = STOP;
```
    right in this step we can see how each position is calculated
    we focus on the variables where *ptr is used,
    fruitX is *ptr%width which is 40
    fruitY is (*ptr/40)%height which is 20 so (*ptr/40)%20
    a byte is 0-255 so the maximum value of fruitY is 255/40 = 6
    and 6%20 is just 6 so fruitY is just [0,6]

    first 32 points we dont need to decodeanything just eat the fruits,
    after that we need to somehow reverse it so we can know what letter we get, 
    for example 'f' in the flag buffer
    its ASCII value is 102
    so,
    fruitX = 102%40 =22
    fruitY =(102/40)%20 = 2%20 = 2
    
    row : 2 col : 22 (x=22,y=2) 
    2*40=80 -> +22 = 102 we get 'f'

    using this script we can autoamte this process:

```python
from pwn import *


r = remote('0.cloud.chals.io', 18223)

fruits = 0 #we need to get 32 fruits
flag = ""

while True:
    try:
        data = r.recvuntil(b'Direction [U | R | D | L]: ').decode()
   
    hx = hy = fx = fy = 0
    lines = data.split('\n')
    
    for y, line in enumerate(lines):
        if 'O' in line:
            hy = y - 1
            hx = line.find('O') - 1
        if '*' in line:
            fy = y - 1
            fx = line.find('*') - 1

    if fruits >= 32:
        val = (fy * 40) + fx
        if val == 0: #if we reached the \0 means we got the flag
            print(f"\nFlag: {flag}")
            break
        flag += chr(val)
        print(flag)

    dx = fx - hx
    if dx != 0:
        r.sendline(b'R' if dx > 0 else b'L')
        r.recvuntil(b'Steps: ')
        r.sendline(str(abs(dx)).encode())
        if (fy - hy) != 0:
             r.recvuntil(b'Direction [U | R | D | L]: ')

    dy = fy - hy
    if dy != 0:
        r.sendline(b'D' if dy > 0 else b'U')
        r.recvuntil(b'Steps: ')
        r.sendline(str(abs(dy)).encode())

    fruits += 1
```
we get the flag BSidestlv{***}