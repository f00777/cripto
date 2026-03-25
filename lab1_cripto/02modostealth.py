#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import struct
from scapy.all import IP, ICMP, send

def main():
    # Validar argumentos
    if len(sys.argv) < 2:
        print(f"Uso: sudo python3 {os.path.basename(__file__)} \"mensaje a enviar\"")
        sys.exit(1)

    mensaje = sys.argv[1]
    destino = "8.8.8.8"  # Se exige enviar exclusivamente a 8.8.8.8
    
    # Mantener el ICMP ID constante (coherente) durante todo el flujo
    # Usamos el PID del programa
    icmp_id = os.getpid() & 0xFFFF
    
    # Iterar sobre cada carácter del mensaje
    for seq_num, caracter in enumerate(mensaje, start=1):
        # -------------------------------------------------------------
        # CONSTRUCCIÓN DEL PAYLOAD INDETECTABLE (56 bytes)
        # -------------------------------------------------------------
        
        # 1. (8 bytes) 'tv_sec' - Timestamp real
        # Cumple con "mantiene payload ICMP (8 primeros bytes)"
        timestamp_sec = struct.pack("<Q", int(time.time()))
        
        # 2. (8 bytes) 'tv_usec' - Acá "escondemos" el carácter
        # El primer byte de esta sección es el carácter secreto.
        # Los siguientes 7 aseguran que el número de microsegundos sea
        # creíble (ej. 0x00000000000960XX -> ~614 mil microsegundos).
        secret_byte = ord(caracter)
        timestamp_usec = bytes([secret_byte, 0x60, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00])
        
        # 3. (40 bytes) Padding estándar de ping Linux
        # Cumple con "mantiene payload ICMP (desde 0x10 a 0x37)"
        padding = bytes(range(0x10, 0x38))
        
        # Ensamblar payload
        payload_data = timestamp_sec + timestamp_usec + padding
        
        # Construir y enviar el paquete
        paquete = IP(dst=destino) / ICMP(type=8, id=icmp_id, seq=seq_num) / payload_data
        
        # Ocultar la salida intrínseca de Scapy y simular la salida del ping normal
        send(paquete, verbose=0)
        print("Sent 1 packets.")
        
        # Esperar 1 segundo simulando un ping normal
        time.sleep(1)

if __name__ == "__main__":
    main()
