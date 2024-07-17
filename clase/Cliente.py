class Cliente:
    def __init__(
        self, p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_password
    ):
        self.id = p_id
        self.nombre = p_nombre
        self.apellido = p_apellido
        self.dni = p_dni
        self.lugar_procedencia = p_lugar_procedencia
        self.password = p_password

        self.midic = {
            "id": p_id,
            "nombre": p_nombre,
            "apellido": p_apellido,
            "dni": p_dni,
            "lugar_procedencia": p_lugar_procedencia,
            # Include the password in midic
        }
