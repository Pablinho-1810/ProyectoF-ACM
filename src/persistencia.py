import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RUTA_INVENTARIO = os.path.join(DATA_DIR, "inventario.txt")
RUTA_VENTAS = os.path.join(DATA_DIR, "ventas.txt")


def linea_a_producto(linea):
    partes = linea.strip().split("|")
    if len(partes) != 7:
        raise ValueError(f"se esperaban 7 campos y hay {len(partes)}")

    codigo, nombre, categoria, precio, stock, stock_minimo, proveedor = partes
    producto = {
        "codigo": codigo.strip().upper(),
        "nombre": nombre.strip(),
        "categoria": categoria.strip(),
        "precio": float(precio),
        "stock": int(stock),
        "stock_minimo": int(stock_minimo),
        "proveedor": proveedor.strip(),
    }

    if producto["precio"] <= 0 or producto["stock"] < 0 or producto["stock_minimo"] < 0:
        raise ValueError("valores numéricos fuera de rango")
    return producto


def cargar_inventario():
    inventario = {}
    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                try:
                    producto = linea_a_producto(linea)
                except ValueError as err:
                    print(f"  [ADVERTENCIA] Línea {numero} de inventario.txt omitida: {err}")
                    continue
                if producto["codigo"] in inventario:
                    print(f"  [ADVERTENCIA] Línea {numero}: código {producto['codigo']} duplicado, se omite.")
                    continue
                inventario[producto["codigo"]] = producto
    except FileNotFoundError:
        print("  [AVISO] No existe data/inventario.txt. Se crea y se inicia con inventario vacío.")
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(RUTA_INVENTARIO, "w", encoding="utf-8"):
            pass
    return inventario


def guardar_inventario(inventario):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
        for p in inventario.values():
            archivo.write(
                f"{p['codigo']}|{p['nombre']}|{p['categoria']}|{p['precio']}|"
                f"{p['stock']}|{p['stock_minimo']}|{p['proveedor']}\n"
            )


def registrar_venta(total, carrito, fecha=None):
    if fecha is None:
        fecha = date.today().isoformat()
    items = []
    for codigo, cantidad in carrito.items():
        items.append(f"{codigo}:{cantidad}")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RUTA_VENTAS, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}|{total}|{';'.join(items)}\n")


def cargar_ventas():
    ventas = []
    try:
        with open(RUTA_VENTAS, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                try:
                    fecha, total, texto_items = linea.strip().split("|")
                    items = {}
                    for par in texto_items.split(";"):
                        codigo, cantidad = par.split(":")
                        items[codigo] = items.get(codigo, 0) + int(cantidad)
                    ventas.append({"fecha": fecha, "total": float(total), "items": items})
                except ValueError as err:
                    print(f"  [ADVERTENCIA] Línea {numero} de ventas.txt omitida: {err}")
    except FileNotFoundError:
        print("  [AVISO] Aún no hay historial de ventas.")
    return ventas
