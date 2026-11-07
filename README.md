# TiendaPy

Aplicación de consola para controlar el inventario y las ventas de la tienda de barrio "Don Aurelio".

## Funcionalidades
- Inventario: registrar, consultar (por código o categoría), modificar y eliminar productos.
- Ventas con carrito, descuentos (5 % desde $50.000 y 10 % desde $100.000), pago y cambio.
- Alertas de stock agrupadas por proveedor, con los productos agotados marcados.
- Cierre del día: total vendido, número de ventas, ticket promedio, producto más vendido y productos sin ventas.
- Datos guardados en `data/inventario.txt` y `data/ventas.txt`.

## Instalación

python -m venv venv
# Windows: venv\Scripts\activate    Linux/Mac: source venv/bin/activate
pip install -r requirements.txt


## Ejecución

python src/main.py


## Decisiones de diseño
- Los productos son diccionarios dentro de un diccionario cuya clave es el código, así la búsqueda es O(1) y los códigos no se repiten.
- Las reglas de negocio se señalan con `raise ErrorNegocio` y se capturan en el flujo principal.
- No se usan clases para los productos (no era obligatorio). Solo se define una excepción propia.
- Se usa `tabulate` para mostrar las tablas en consola.
