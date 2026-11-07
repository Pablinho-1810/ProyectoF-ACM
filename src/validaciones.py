

class ErrorNegocio(Exception):
    """Se lanza cuando se viola una regla de negocio de TiendaPy."""


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        
        if texto and "|" not in texto:
            return texto
        print("  El dato no puede estar vacío ni contener '|'.")


def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("   Debe ingresar un número entero.")
            continue
        if valor < minimo:
            print(f"   El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def pedir_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("   Debe ingresar un número válido.")
            continue
        if valor <= 0:
            print("  El valor debe ser mayor que cero.")
            continue
        return valor


def pedir_opcion(mensaje, opciones):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print(f"   Opción inválida. Opciones: {', '.join(opciones)}")


def confirmar(mensaje):
    return pedir_opcion(mensaje + " (s/n): ", ["s", "n", "S", "N"]).lower() == "s"
