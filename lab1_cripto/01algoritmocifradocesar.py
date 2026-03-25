texto = input("Ingrese el string a cifrar: ")
desplazamiento = int(input("Ingrese el desplazamiento: "))

# incluyendo la letra 'ñ' (tamaño 27) para que sea considerada en el cifrado.
alfabeto = "abcdefghijklmnñopqrstuvwxyz"
resultado = ""

for c in texto:
    if c.lower() in alfabeto:
        pos_original = alfabeto.index(c.lower())
        nueva_pos = (pos_original + desplazamiento) % len(alfabeto)
        nuevo_char = alfabeto[nueva_pos]
        
        # Mantiene minúscula o mayúscula según el texto original
        resultado += nuevo_char.upper() if c.isupper() else nuevo_char
    else:
        resultado += c

print("Texto cifrado:", resultado)
