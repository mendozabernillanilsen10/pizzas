class Pizza:
    def __init__(self, p_id, p_nombre, p_descripcion, p_precio, p_tamano, image_url=None):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.precio = p_precio
        self.tamano = p_tamano
        self.image_url = image_url
    
    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "tamano": self.tamano,
            "image_url": self.image_url
        }
