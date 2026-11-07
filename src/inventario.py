from tabulate import tabulate
from validaciones import ErrorNegocio

CATEGORIAS = ["Lacteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"]


def crear_producto(codigo, nombre, categoria, precio, stock, stock_minimo, proveedor):
    if precio <= 0:
        raise ErrorNegocio("El precio debe ser mayor que cero.")
    if stock <= 0:
        raise ErrorNegocio("El stock debe ser mayor que cero.")
    if stock_minimo < 0:
        raise ErrorNegocio("El stock mínimo no puede ser negativo.")
    return {
        "codigo": codigo.upper(), "nombre": nombre, "categoria": categoria,
        "precio": float(precio), "stock": stock,
        "stock_minimo": stock_minimo, "proveedor": proveedor,
    }


def registrar_producto(inventario, producto):
    if producto["codigo"] in inventario:
        raise ErrorNegocio(f"Ya existe un producto con el código {producto['codigo']}.")
    inventario[producto["codigo"]] = producto


def buscar_por_codigo(inventario, codigo):
    producto = inventario.get(codigo.strip().upper())
    if producto is None:
        raise ErrorNegocio(f"No existe un producto con el código {codigo.upper()}.")
    return producto


def buscar_por_categoria(inventario, categoria):
    encontrados = []
    for producto in inventario.values():
        if producto["categoria"].lower() == categoria.lower():
            encontrados.append(producto)
    return encontrados


def modificar_precio(inventario, codigo, nuevo_precio):
    if nuevo_precio <= 0:
        raise ErrorNegocio("El precio debe ser mayor que cero.")
    buscar_por_codigo(inventario, codigo)["precio"] = float(nuevo_precio)


def modificar_stock(inventario, codigo, nuevo_stock):
    if nuevo_stock <= 0:
        raise ErrorNegocio("El stock debe ser mayor que cero.")
    buscar_por_codigo(inventario, codigo)["stock"] = nuevo_stock


def eliminar_producto(inventario, codigo):
    producto = buscar_por_codigo(inventario, codigo)
    return inventario.pop(producto["codigo"])


def mostrar_productos(productos):
    if not productos:
        print("  No hay productos para mostrar.")
        return
    filas = []
    for p in productos:
        filas.append([p["codigo"], p["nombre"], p["categoria"], f"${p['precio']:,.0f}",
                      p["stock"], p["stock_minimo"], p["proveedor"]])
    print(tabulate(filas, headers=["Código", "Nombre", "Categoría", "Precio",
                                   "Stock", "Mínimo", "Proveedor"], tablefmt="grid"))
