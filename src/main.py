
from datetime import date

from tabulate import tabulate

from inventario import (CATEGORIAS, crear_producto, registrar_producto, buscar_por_codigo,
                        buscar_por_categoria, modificar_precio, modificar_stock,
                        eliminar_producto, mostrar_productos)
from ventas import agregar_al_carrito, calcular_totales, calcular_cambio, confirmar_venta
from reportes import mostrar_alertas, cierre_del_dia, mostrar_cierre
from persistencia import (cargar_inventario, guardar_inventario, registrar_venta,
                          cargar_ventas)
from validaciones import (ErrorNegocio, pedir_texto, pedir_entero, pedir_float,
                          pedir_opcion, confirmar)


def pedir_categoria():
    for i, categoria in enumerate(CATEGORIAS, start=1):
        print(f"   {i}. {categoria}")
    opciones = []
    for i in range(1, len(CATEGORIAS) + 1):
        opciones.append(str(i))
    return CATEGORIAS[int(pedir_opcion("  Categoría: ", opciones)) - 1]


def opcion_registrar(inventario):
    codigo = pedir_texto("  Código: ").upper()
    if codigo in inventario:
        raise ErrorNegocio(f"El código {codigo} ya existe. No se registró el producto.")
    nombre = pedir_texto("  Nombre: ")
    categoria = pedir_categoria()
    precio = pedir_float("  Precio (COP): ")
    stock = pedir_entero("  Stock inicial: ")
    stock_minimo = pedir_entero("  Stock mínimo: ", minimo=0)
    proveedor = pedir_texto("  Proveedor: ")
    producto = crear_producto(codigo, nombre, categoria, precio, stock, stock_minimo, proveedor)
    registrar_producto(inventario, producto)
    print(f"  Producto {codigo} registrado.")


def menu_inventario(inventario):
    while True:
        print("\n  --- GESTIÓN DE INVENTARIO ---")
        print("  1. Ver todo  2. Registrar  3. Buscar por código  4. Buscar por categoría")
        print("  5. Modificar precio  6. Modificar stock  7. Eliminar  0. Volver")
        opcion = pedir_opcion("  Opción: ", ["0", "1", "2", "3", "4", "5", "6", "7"])
        try:
            if opcion == "1":
                mostrar_productos(list(inventario.values()))
            elif opcion == "2":
                opcion_registrar(inventario)
            elif opcion == "3":
                mostrar_productos([buscar_por_codigo(inventario, pedir_texto("  Código: "))])
            elif opcion == "4":
                encontrados = buscar_por_categoria(inventario, pedir_categoria())
                if encontrados:
                    mostrar_productos(encontrados)
                else:
                    print("  No hay productos en esa categoría.")
            elif opcion == "5":
                codigo = pedir_texto("  Código: ")
                buscar_por_codigo(inventario, codigo)
                modificar_precio(inventario, codigo, pedir_float("  Nuevo precio: "))
                print("  Precio actualizado.")
            elif opcion == "6":
                codigo = pedir_texto("  Código: ")
                buscar_por_codigo(inventario, codigo)
                modificar_stock(inventario, codigo, pedir_entero("  Nuevo stock: "))
                print("  Stock actualizado.")
            elif opcion == "7":
                codigo = pedir_texto("  Código: ")
                producto = buscar_por_codigo(inventario, codigo)
                if confirmar(f"  ¿Eliminar {producto['nombre']}?"):
                    eliminar_producto(inventario, codigo)
                    print("  Producto eliminado.")
            else:
                return
        except ErrorNegocio as err:
            print(f"  [ERROR] {err}")


def opcion_vender(inventario):
    carrito = {}
    print("\n  --- NUEVA VENTA --- (deje el código vacío para terminar)")
    while True:
        codigo = input("  Código del producto: ").strip()
        if not codigo:
            break
        cantidad = pedir_entero("  Cantidad: ")
        try:
            agregar_al_carrito(inventario, carrito, codigo, cantidad)
            print("  Agregado al carrito.")
        except ErrorNegocio as err:
            print(f"  [ERROR] {err}")

    if not carrito:
        print("  Venta cancelada: carrito vacío.")
        return

    detalle, subtotal, porcentaje, descuento, total = calcular_totales(inventario, carrito)
    filas = []
    for nombre, cantidad, precio, valor in detalle:
        filas.append([nombre, cantidad, f"${precio:,.0f}", f"${valor:,.0f}"])
    print(tabulate(filas, headers=["Producto", "Cant.", "Precio", "Valor"], tablefmt="grid"))
    print(f"  Subtotal:  ${subtotal:,.0f}")
    print(f"  Descuento ({porcentaje * 100:.0f}%): -${descuento:,.0f}")
    print(f"  TOTAL:     ${total:,.0f}")

    if not confirmar("  ¿Confirmar venta?"):
        print("  Venta cancelada. El inventario no cambió.")
        return

    while True:
        pago = pedir_float("  Pago recibido: ")
        try:
            cambio = calcular_cambio(total, pago)
            break
        except ErrorNegocio as err:
            print(f"  [ERROR] {err} Intente de nuevo.")

    confirmar_venta(inventario, carrito)
    registrar_venta(total, carrito)
    guardar_inventario(inventario)  # guardar ya, por si se cierra el programa
    print(f"  Venta registrada. Cambio: ${cambio:,.0f}")


def main():
    print("=" * 45)
    print("   TiendaPy - Tienda Don Aurelio")
    print("=" * 45)
    inventario = cargar_inventario()
    print(f"  {len(inventario)} productos cargados.")

    try:
        while True:
            print("\n===== MENÚ PRINCIPAL =====")
            print("1. Inventario\n2. Nueva venta\n3. Alertas de stock")
            print("4. Cierre del día\n5. Guardar\n0. Salir")
            opcion = pedir_opcion("Opción: ", ["0", "1", "2", "3", "4", "5"])
            try:
                if opcion == "1":
                    menu_inventario(inventario)
                elif opcion == "2":
                    opcion_vender(inventario)
                elif opcion == "3":
                    mostrar_alertas(inventario)
                elif opcion == "4":
                    reporte = cierre_del_dia(inventario, cargar_ventas(), date.today().isoformat())
                    mostrar_cierre(inventario, reporte)
                elif opcion == "5":
                    guardar_inventario(inventario)
                    print("  Inventario guardado.")
                else:
                    guardar_inventario(inventario)
                    print("  Inventario guardado. ¡Hasta luego, Don Aurelio!")
                    break
            except ErrorNegocio as err:
                print(f"  [ERROR] {err}")
            except OSError as err:
                print(f"  [ERROR DE ARCHIVO] {err}")
    except KeyboardInterrupt:
        guardar_inventario(inventario)
        print("\n  Programa interrumpido. Inventario guardado.")


if __name__ == "__main__":
    main()
