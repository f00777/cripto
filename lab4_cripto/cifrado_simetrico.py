from Crypto.Cipher import DES, AES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

# Tamaños requeridos (bytes)
KEY_SIZES = {"DES": 8, "AES-256": 32, "3DES": 24}
IV_SIZES  = {"DES": 8, "AES-256": 16, "3DES": 8}

def ajustar_clave(key_bytes, tam_requerido, nombre_algo):
    """Ajusta la clave al tamaño requerido por el algoritmo."""
    if len(key_bytes) < tam_requerido:
        relleno = get_random_bytes(tam_requerido - len(key_bytes))
        key_bytes = key_bytes + relleno
        print(f"[{nombre_algo}] Clave menor al tamaño requerido. Se agregaron {len(relleno)} bytes aleatorios.")
    elif len(key_bytes) > tam_requerido:
        key_bytes = key_bytes[:tam_requerido]
        print(f"[{nombre_algo}] Clave mayor al tamaño requerido. Se truncó a {tam_requerido} bytes.")
    else:
        print(f"[{nombre_algo}] La clave tiene el tamaño exacto ({tam_requerido} bytes).")
    return key_bytes

def ajustar_iv(iv_bytes, tam_requerido, nombre_algo):
    """Ajusta el IV al tamaño requerido."""
    if len(iv_bytes) < tam_requerido:
        relleno = get_random_bytes(tam_requerido - len(iv_bytes))
        iv_bytes = iv_bytes + relleno
        print(f"[{nombre_algo}] IV menor al requerido. Se completó a {tam_requerido} bytes.")
    elif len(iv_bytes) > tam_requerido:
        iv_bytes = iv_bytes[:tam_requerido]
        print(f"[{nombre_algo}] IV mayor al requerido. Se truncó a {tam_requerido} bytes.")
    return iv_bytes

def cifrar_des(texto, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto, DES.block_size))
    return ct

def descifrar_des(ct, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), DES.block_size)
    return pt

def cifrar_aes256(texto, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto, AES.block_size))
    return ct

def descifrar_aes256(ct, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def cifrar_3des(texto, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto, DES3.block_size))
    return ct

def descifrar_3des(ct, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), DES3.block_size)
    return pt

def ejecutar_algoritmo(nombre, key_raw, iv_raw, texto_bytes, fn_cifrar, fn_descifrar):
    """Ejecuta cifrado y descifrado para un algoritmo dado."""
    tam_key = KEY_SIZES[nombre]
    tam_iv = IV_SIZES[nombre]

    key = ajustar_clave(key_raw[:], tam_key, nombre)
    iv = ajustar_iv(iv_raw[:], tam_iv, nombre)

    print(f"[{nombre}] Clave final (hex): {binascii.hexlify(key).decode()}")
    print(f"[{nombre}] IV final (hex):    {binascii.hexlify(iv).decode()}")

    ct = fn_cifrar(texto_bytes, key, iv)
    print(f"[{nombre}] Texto cifrado (hex): {binascii.hexlify(ct).decode()}")

    pt = fn_descifrar(ct, key, iv)
    print(f"[{nombre}] Texto descifrado: {pt.decode()}")
    print(f"[{nombre}] ¿Coincide con el original? {'Sí' if pt == texto_bytes else 'No'}")
    print()

def main():
    print("=" * 60)
    print("  Cifrado Simétrico: DES, AES-256 y 3DES (modo CBC)")
    print("=" * 60)

    key_input = input("\nIngrese la clave (key): ")
    iv_input  = input("Ingrese el vector de inicialización (IV): ")
    texto     = input("Ingrese el texto a cifrar: ")

    key_bytes   = key_input.encode("utf-8")
    iv_bytes    = iv_input.encode("utf-8")
    texto_bytes = texto.encode("utf-8")

    print("\n" + "-" * 60)
    print("  Resultados")
    print("-" * 60 + "\n")

    # DES
    ejecutar_algoritmo("DES", key_bytes, iv_bytes, texto_bytes,
                       cifrar_des, descifrar_des)

    # AES-256
    ejecutar_algoritmo("AES-256", key_bytes, iv_bytes, texto_bytes,
                       cifrar_aes256, descifrar_aes256)

    # 3DES
    ejecutar_algoritmo("3DES", key_bytes, iv_bytes, texto_bytes,
                       cifrar_3des, descifrar_3des)

if __name__ == "__main__":
    main()
