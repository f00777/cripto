import sys, os, time, struct
from scapy.all import IP, ICMP, wrpcap

mensaje = "criptografia y seguridad en redes"
# shift with rot 9
shifted = ""
for c in mensaje:
    if c in "abcdefghijklmnopqrstuvwxyz":
        idx = "abcdefghijklmnopqrstuvwxyz".index(c)
        shifted += "abcdefghijklmnopqrstuvwxyz"[(idx + 9) % 26]
    else:
        shifted += c

print("Generando pcap con mensaje:", shifted)

pkts = []
for seq_num, caracter in enumerate(shifted, start=1):
    timestamp_sec = struct.pack("<Q", int(time.time()))
    secret_byte = ord(caracter)
    timestamp_usec = bytes([secret_byte, 0x60, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00])
    padding = bytes(range(0x10, 0x38))
    payload_data = timestamp_sec + timestamp_usec + padding
    paquete = IP(dst="8.8.8.8") / ICMP(type=8, id=1234, seq=seq_num) / payload_data
    pkts.append(paquete)

wrpcap("test.pcapng", pkts)
