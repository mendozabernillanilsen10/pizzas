# PizzaController.py

from bd import obtener_conexion

class PizzaController:
    @classmethod
    def insertar_pizza(cls, p_nombre, p_descripcion, p_precio, p_tamano, image_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pizzas (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
                (p_nombre, p_descripcion, p_precio, image_url)
            )
        conexion.commit()
        conexion.close()
    @classmethod
    def obtener_pizzas(cls):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, name, description, price, image_url FROM pizzas")
            result = cursor.fetchall()
        conexion.close()
        
        pizzas = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "image_url": row[4]
            }
            for row in result
        ]
        return pizzas

# Dentro de PizzaController.py

    @classmethod
    def eliminar_pizza(cls, pizza_id):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM pizzas WHERE id = %s", (pizza_id,))
            conexion.commit()
        except Exception as e:
            print(f"Error eliminando pizza: {e}")
            conexion.rollback()
            raise
        finally:
            conexion.close()


        

    @classmethod
    def obtener_pizza_por_id(cls, p_id):
        conexion = obtener_conexion()
        pizza = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, price, image_url FROM pizzas WHERE id = %s",
                (p_id,)
            )
            pizza_tuple = cursor.fetchone()
            if pizza_tuple:
                pizza = {
                    'id': pizza_tuple[0],
                    'nombre': pizza_tuple[1],
                    'descripcion': pizza_tuple[2],
                    'precio': pizza_tuple[3],
                    'image_url': pizza_tuple[4]  # Asegúrate de que image_url coincida con el nombre del campo en tu base de datos
                }
        conexion.close()
        return pizza



    @classmethod
    def actualizar_pizza(cls, p_id, p_nombre, p_descripcion, p_precio, p_tamano, image_url):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE pizzas SET name = %s, description = %s, price = %s, image_url = %s WHERE id = %s",
                    (p_nombre, p_descripcion, p_precio, image_url, p_id)
                )
            conexion.commit()
        except Exception as e:
            print(f"Error actualizando pizza: {e}")
            conexion.rollback()
        finally:
            conexion.close()

