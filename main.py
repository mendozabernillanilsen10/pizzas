import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    send_from_directory,
)
from datetime import date
from flask import redirect, url_for


from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from controlador.PizzaController import PizzaController
from controlador.ClienteController import ClienteController

import bcrypt
import traceback
import base64
import os

app = Flask(__name__)
app.secret_key = 'my_super_secret_key'  # Ensure this line is set early in your script
app.config["JWT_SECRET_KEY"] = "msii3jjkjkkkdmmdmkfkf"  # Aquí configuras tu clave secreta JWT
jwt = JWTManager(app)

UPLOAD_FOLDER = "imagen"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/imagen/<path:filename>")
def mostrar_imagen(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/")
@app.route("/index")
def obtener_clientes():
    return render_template("index.html")


@app.route("/listado_pizzas")
def listado_pizzas():
    pizzas = PizzaController.obtener_pizzas()
    return render_template("listado_pizzas.html", pizzas=pizzas)

@app.route("/formulario_agregar_pizza")
def formulario_agregar_pizza():
    return render_template("agregar_pizza.html")


@app.route("/editar_pizza/<int:pizza_id>", methods=["GET", "POST"])
def editar_pizza(pizza_id):
    pizza = PizzaController.obtener_pizza_por_id(pizza_id)
    if not pizza:
        return "Pizza no encontrada", 404

    if request.method == "POST":
        try:
            p_nombre = request.form["nombre"]
            p_descripcion = request.form["descripcion"]
            p_precio = request.form["precio"]
            p_tamano = request.form["tamano"]
            foto = request.files.get("foto")

            if foto:
                nombre_archivo = secure_filename(foto.filename)
                ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
                foto.save(ruta_guardado)
            else:
                nombre_archivo = pizza["image_url"]  # Mantener la imagen existente si no se sube una nueva

            PizzaController.actualizar_pizza(
                pizza_id, p_nombre, p_descripcion, p_precio, p_tamano, nombre_archivo
            )

            return redirect(url_for("listado_pizzas"))

        except Exception as e:
            return jsonify({"Estado": False, "Mensaje": str(e)})

    return render_template("editar_pizza.html", pizza=pizza)

@app.route("/eliminar_pizza/<int:pizza_id>", methods=["POST"])
def eliminar_pizza(pizza_id):
    try:
        PizzaController.eliminar_pizza(pizza_id)
        return redirect(url_for("listado_pizzas"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_guardar_pizzaplantilla", methods=["POST"])
def api_guardar_pizzaplantilla():
    try:
        p_nombre = request.form["nombre"]
        p_descripcion = request.form["descripcion"]
        p_precio = request.form["precio"]
        time = request.form["time"]
        energy = request.form["energy"]
        score = request.form["score"]

        foto = request.files.get("foto")
        if foto:
            # Guardar la foto
            nombre_archivo = secure_filename(foto.filename)
            ruta_guardado = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            foto.save(ruta_guardado)
        else:
            nombre_archivo = "default.png"

        # Insertar la pizza en la base de datos
        PizzaController.insertar_pizza(p_nombre, p_descripcion, p_precio, time, nombre_archivo, energy, score)

        return redirect(url_for("listado_pizzas"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})




@app.route("/listado_pizzasApi", methods=["GET"])
@jwt_required()
def listado_pizzas_api():
    pizzas = PizzaController.listar_pizzas()
    
    # Crear una lista para almacenar las pizzas con el formato deseado
    pizzas_list = []

    for pizza in pizzas:
        # Construir un diccionario con los datos deseados para cada pizza
        pizza_dict = {
            "id": pizza["id"],
            "nombre": pizza["name"],
            "descripcion": pizza["description"],
            "time": pizza["time"],
            "precio": pizza["price"],
            "energy": pizza["energy"],
            "score": pizza["score"],

            
            "imagen_url": f"{request.url_root}imagen/{pizza['image_url']}"  # URL completa de la imagen
        }
        
        # Agregar el diccionario de la pizza a la lista
        pizzas_list.append(pizza_dict)
    
    # Retornar la lista de pizzas en formato JSON
    return jsonify({"Estado": True, "Mensaje": "OK", "Pizzas": pizzas_list})






@app.route("/api_eliminar_clientePlantilla", methods=["POST"])
def api_eliminar_cliente_plantilla():
    try:
        ClienteController.eliminar_cliente(request.form["id"])
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})

@app.route("/api_actualizar_cliente", methods=["POST"])
def api_actualizar_cliente():
    try:
        p_id = request.json["id"]
        p_nombre = request.json["nombre"]
        p_apellido = request.json["apellido"]
        p_dni = request.json["dni"]
        p_lugar_procedencia = request.json["lugar_procedencia"]

        ClienteController.actualizar_cliente(
            p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia
        )

        return jsonify({"Estado": True, "Mensaje": "Cliente actualizado correctamente"})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_obtener_cliente/<int:id>")
def api_obtener_cliente(id):
    try:
        cliente = ClienteController.obtener_cliente_por_id(id)
        listaserializable = []

        miobj = ClienteController(
            cliente[0], cliente[1], cliente[2], cliente[3], cliente[4]
        )
        listaserializable.append(miobj.midic.copy())
        return jsonify({"Estado": True, "Mensaje": "OK", "Datos": listaserializable})

    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})



@app.route("/listadoclientes")
def listadoclientes():
    # Lógica para obtener datos si es necesario
    clientes = ClienteController.obtener_clientes()
    return render_template("listadoclientes.html", clientes=clientes)

@app.route("/api_guardar_clienteplantilla", methods=["POST"])
def api_guardar_clienteplantilla():
    try:
        p_nombre = request.form["nombre"]
        p_apellido = request.form["apellido"]
        p_dni = request.form["dni"]
        p_lugar_procedencia = request.form["lugar_procedencia"]
        p_password = request.form["password"]
        ClienteController.insertar_cliente(
            p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_password
        )
        # Redirigir a la pantalla principal
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})



@app.route("/formulario_agregar_cliente")
def formulario_agregar_cliente():
    # Lógica para manejar el formulario de agregar cliente
    return render_template("agregar_Cliente.html")


@app.route("/editar_cliente/<int:id>")
def editar_cliente(id):
    # Logic to retrieve client information by ID
    cliente = ClienteController.obtener_cliente_por_id(id)
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    try:
        # Logic to delete a client using the request data
        ClienteController.eliminar_cliente(request.json["id"])
        return jsonify({"Estado": True, "Mensaje": "Cliente eliminado correctamente"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})


@app.route("/api_actualizar_cliente_y_redirigir/<int:id>", methods=["POST"])
def api_actualizar_cliente_y_redirigir(id):
    try:
        p_id = id
        p_nombre = request.form["nombre"]
        p_apellido = request.form["apellido"]
        p_dni = request.form["dni"]
        p_lugar_procedencia = request.form["lugar_procedencia"]

        ClienteController.actualizar_cliente(
            p_id, p_nombre, p_apellido, p_dni, p_lugar_procedencia
        )

        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("listadoclientes"))
    except Exception as e:
        flash(f"Error al actualizar el cliente: {str(e)}", "error")
        return redirect(url_for("editar_cliente", id=id))



@app.route("/api_login", methods=["POST"])
def api_login():
    try:
        p_dni = request.json.get("dni")
        password = request.json.get("password")
        usuario = ClienteController.validar_credenciales(p_dni, password)
        if usuario:
            # Generar un token JWT
            token = create_access_token(identity=usuario["id"])
            return jsonify(
                {
                    "Estado": True,
                    "Mensaje": "Inicio de sesión exitoso",
                    "Usuario": usuario,
                    "token": token,
                }
            )
        else:
            return jsonify({"Estado": False, "Mensaje": "Credenciales incorrectas"})
    except Exception as e:
        return jsonify({"Estado": False, "Mensaje": str(e)})

@app.route("/api_guardar_cliente", methods=["POST"])
def api_guardar_cliente():
    try:
        # Obtener datos del cuerpo de la solicitud en formato JSON
        data = request.json
        # Extraer datos del JSON
        p_nombre = data.get("nombre")
        p_apellido = data.get("apellido")
        p_dni = data.get("dni")
        p_lugar_procedencia = data.get("lugar_procedencia")
        p_password = data.get("password")
        # Insertar cliente utilizando el controlador
        ClienteController.insertar_cliente(
            p_nombre, p_apellido, p_dni, p_lugar_procedencia, p_password
        )
        # Retornar una respuesta exitosa en formato JSON
        return jsonify({"Estado": True, "Mensaje": "Cliente registrado correctamente"})
    except Exception as e:
        # Retornar un mensaje de error en caso de excepción
        return jsonify({"Estado": False, "Mensaje": str(e)})




if __name__ == '__main__':
    app.run(host='192.168.1.7', port=8000, debug=True)  # Cambia el puerto según necesites
