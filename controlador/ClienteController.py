from bd import obtener_conexion
import bcrypt


class ClienteController:
    @classmethod
    def insertar_cliente(
        cls, p_nombre, p_apellido, p_dni, p_lugar_procedencia, password
    ):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, apellido, dni, lugar_procedencia, password) VALUES (%s, %s, %s, %s, %s)",
                (p_nombre, p_apellido, p_dni, p_lugar_procedencia, hashed_password),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_cliente(cls, p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE clientes SET nombre = %s, apellido = %s, dni = %s, lugar_procedencia = %s WHERE id = %s",
                (p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_id),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_cliente_por_id(cls, p_id):
        conexion = obtener_conexion()
        cliente = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, apellido, dni, lugar_procedencia FROM clientes WHERE id = %s",
                (p_id,),
            )
            cliente = cursor.fetchone()
        conexion.close()
        return cliente

    @classmethod
    def eliminar_cliente(cls, p_id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (p_id,))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_clientes(cls):
        conexion = obtener_conexion()
        clientes = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, apellido, dni, lugar_procedencia FROM clientes"
            )
            clientes = cursor.fetchall()
        conexion.close()
        return clientes

    @classmethod
    def validar_credenciales(cls, p_dni, password):
        conexion = obtener_conexion()

        try:
            # Ensure data types and trim whitespaces
            p_dni = str(p_dni).strip()
            password = str(password).strip()

            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes WHERE dni=%s", (p_dni,))
                usuario = cursor.fetchone()
                if usuario:
                    print(f"encontro {usuario[0]}")  # Assuming id is at index 0
                    hashed_password = usuario[5].encode(
                        "utf-8"
                    )  # Assuming password is at index 5

                    password = password.encode("utf-8")
                    if bcrypt.checkpw(password, hashed_password):
                        return {
                            "id": usuario[0],
                            "nombre": usuario[1],
                            "apellido": usuario[2],
                            "dni": usuario[3],
                            "lugar_procedencia": usuario[4],
                        }  # Adjust indices as needed
                    else:
                        return None
                else:
                    return None
        except Exception as e:
            return None
        finally:
            conexion.close()
