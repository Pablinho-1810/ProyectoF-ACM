from tabulate import tabulate


def productos_en_alerta(inventario):
    por_proveedor = {}
    for p in inventario.values():
        if p["stock"] <= p["stock_minimo"]:
            lista = por_proveedor.get(p["proveedor"], [])
            lista.append(p)
            por_proveedor[p["proveedor"]] = lista
    return por_proveedor


def mostrar_alertas(inventario):
    grupos = productos_en_alerta(inventario)
    if not grupos:
        print("  Ningún producto está por debajo del stock mínimo.")
        return
    for proveedor in sorted(grupos):
        print(f"\n  Proveedor: {proveedor}")
        filas = []
        for p in grupos[proveedor]:
            estado = "AGOTADO" if p["stock"] == 0 else "Stock bajo"
            sugerido = max(p["stock_minimo"] * 2 - p["stock"], 1)
            filas.append([p["codigo"], p["nombre"], p["stock"], p["stock_minimo"], estado, sugerido])
        print(tabulate(filas, headers=["Código", "Producto", "Stock", "Mínimo",
                                       "Estado", "Pedir"], tablefmt="grid"))


def cierre_del_dia(inventario, ventas, fecha):
    ventas_dia = []
    for v in ventas:
        if v["fecha"] == fecha:
            ventas_dia.append(v)

    total_vendido = 0
    unidades = {}
    for v in ventas_dia:
        total_vendido += v["total"]
        for codigo, cantidad in v["items"].items():
            unidades[codigo] = unidades.get(codigo, 0) + cantidad

    numero_ventas = len(ventas_dia)
    ticket_promedio = total_vendido / numero_ventas if numero_ventas > 0 else 0
    mas_vendido = max(unidades, key=unidades.get) if unidades else None

    sin_ventas = []
    for codigo in inventario:
        if codigo not in unidades:
            sin_ventas.append(codigo)

    categorias = set()
    for codigo in unidades:
        if codigo in inventario:
            categorias.add(inventario[codigo]["categoria"])

    return {
        "fecha": fecha, "total": total_vendido, "numero_ventas": numero_ventas,
        "ticket_promedio": ticket_promedio, "mas_vendido": mas_vendido,
        "unidades_mas_vendido": unidades.get(mas_vendido, 0),
        "sin_ventas": sin_ventas, "categorias": categorias,
    }


def mostrar_cierre(inventario, reporte):
    print(f"\n  ===== CIERRE DEL DÍA {reporte['fecha']} =====")
    if reporte["mas_vendido"] is None:
        texto_mas = "Sin ventas"
    else:
        nombre = inventario.get(reporte["mas_vendido"], {}).get("nombre", reporte["mas_vendido"])
        texto_mas = f"{nombre} ({reporte['unidades_mas_vendido']} und.)"
    filas = [
        ["Total vendido", f"${reporte['total']:,.0f}"],
        ["Número de ventas", reporte["numero_ventas"]],
        ["Ticket promedio", f"${reporte['ticket_promedio']:,.0f}"],
        ["Producto más vendido", texto_mas],
        ["Categorías con movimiento", ", ".join(sorted(reporte["categorias"])) or "Ninguna"],
    ]
    print(tabulate(filas, tablefmt="grid"))
    print("\n  Productos sin ventas hoy:")
    nombres = []
    for codigo in reporte["sin_ventas"]:
        nombres.append([codigo, inventario[codigo]["nombre"]])
    print(tabulate(nombres, headers=["Código", "Producto"], tablefmt="grid") if nombres else "  Ninguno")
