from inventario import buscar_por_codigo
from validaciones import ErrorNegocio

UMBRAL_DESCUENTO_5 = 50000
UMBRAL_DESCUENTO_10 = 100000


def porcentaje_descuento(subtotal):
    if subtotal >= UMBRAL_DESCUENTO_10:
        return 0.10
    elif subtotal >= UMBRAL_DESCUENTO_5:
        return 0.05
    return 0.0


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    if cantidad <= 0:
        raise ErrorNegocio("La cantidad debe ser mayor que cero.")
    producto = buscar_por_codigo(inventario, codigo)
    ya_en_carrito = carrito.get(producto["codigo"], 0)
    if ya_en_carrito + cantidad > producto["stock"]:
        raise ErrorNegocio(
            f"Stock insuficiente de {producto['nombre']}: disponibles "
            f"{producto['stock']}, ya en carrito {ya_en_carrito}."
        )
    carrito[producto["codigo"]] = ya_en_carrito + cantidad


def calcular_totales(inventario, carrito):
    detalle = []
    subtotal = 0
    for codigo, cantidad in carrito.items():
        producto = inventario[codigo]
        valor = producto["precio"] * cantidad
        subtotal += valor
        detalle.append([producto["nombre"], cantidad, producto["precio"], valor])
    porcentaje = porcentaje_descuento(subtotal)
    descuento = round(subtotal * porcentaje, 2)
    total = round(subtotal - descuento, 2)
    return detalle, subtotal, porcentaje, descuento, total


def calcular_cambio(total, pago):
    if pago < total:
        raise ErrorNegocio(f"Pago insuficiente: faltan ${total - pago:,.0f}.")
    return round(pago - total, 2)


def confirmar_venta(inventario, carrito):
    for codigo, cantidad in carrito.items():
        if codigo not in inventario or cantidad > inventario[codigo]["stock"]:
            raise ErrorNegocio(f"No hay stock suficiente de {codigo}. Venta anulada.")
    for codigo, cantidad in carrito.items():
        inventario[codigo]["stock"] -= cantidad
