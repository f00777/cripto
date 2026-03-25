#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
try:
    from scapy.all import rdpcap, ICMP
except ImportError:
    print("Por favor, instale scapy: pip install scapy")
    sys.exit(1)

def extraer_mensaje(pcap_path):
    """
    Lee un archivo pcapng y extrae el mensaje oculto en el timestamp
    del payload de los paquetes ICMP (tipo 8).
    """
    try:
        paquetes = rdpcap(pcap_path)
    except Exception as e:
        print(f"Error al leer pcap: {e}")
        sys.exit(1)

    mensaje = ""
    for pkt in paquetes:
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8:
            # Replicamos el proceso inverso de 02modostealth.py
            # El caracter secreto se encuentra en el primer byte de tv_usec,
            # lo que corresponde al byte 8 (índice 8) del payload de ICMP.
            payload = bytes(pkt[ICMP].payload)
            if len(payload) >= 16:
                secreto = payload[8]
                mensaje += chr(secreto)
                
    return mensaje

def rot_decode(texto, desfase):
    """
    Decodifica usando cifrado César. Se asume el alfabeto español (27 l.).
    El carácter ñ se incluye y por tanto un rot-27 dará el texto original.
    """
    resultado = ""
    for c in texto:
        if c.islower() and c in "abcdefghijklmnñopqrstuvwxyz":
            idx = "abcdefghijklmnñopqrstuvwxyz".index(c)
            resultado += "abcdefghijklmnñopqrstuvwxyz"[(idx - desfase) % 27]
        elif c.isupper() and c in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ":
            idx = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ".index(c)
            resultado += "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"[(idx - desfase) % 27]
        else:
            # Dejamos cualquier otro caracter intacto (incluyendo espacios o símbolos)
            resultado += c
    return resultado

def evaluar_mensaje(texto):
    """
    Evalúa la probabilidad de que el texto sea español mediante
    un análisis de frecuencia de letras, asignando pesos según popularidad.
    """
    # Frecuencia aproximada del español de mayor a menor
    letras_frecuentes = "eaosrnidlcptmbuqyvhgñjfzkwx"
    
    # Asignamos un puntaje: 'e' vale 27, 'a' vale 26, ..., 'x' vale 1
    pesos = {letra: (27 - i) for i, letra in enumerate(letras_frecuentes)}
    
    score = 0
    for c in texto.lower():
        if c in pesos:
            score += pesos[c]
            
    return score

def main():
    if len(sys.argv) < 2:
        print(f"Uso: sudo python3 {os.path.basename(__file__)} archivo.pcapng")
        sys.exit(1)
        
    pcap_file = sys.argv[1]
    
    mensaje_cifrado = extraer_mensaje(pcap_file)
    if not mensaje_cifrado:
        print("No se encontraron mensajes ocultos en el pcap provisto.")
        sys.exit(1)
        
    opciones = []
    mejor_score = -1
    mejor_rot = -1
    
    # El enunciado pide probar las combinaciones posibles "hasta rot 27".
    # Iteramos desde 0 a 27 = 28 iteraciones.
    for rot in range(28):
        descifrado = rot_decode(mensaje_cifrado, rot)
        score = evaluar_mensaje(descifrado)
        opciones.append((rot, descifrado, score))
        
        # Encontramos la configuración más probable de forma sencilla
        if score > mejor_score:
            mejor_score = score
            mejor_rot = rot
            
    # Imprimir todas las combinaciones generadas
    for rot, texto, score in opciones:
        # Formato alineado como en el ejemplo proporcionado
        linea = f"{rot:<11}{texto}"
        
        if rot == mejor_rot and mejor_score > 0:
            # Imprimir en verde (\033[92m) el resultado más probable
            print(f"\033[92m{linea}\033[0m")
        else:
            print(linea)

if __name__ == "__main__":
    main()
