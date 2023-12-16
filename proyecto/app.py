from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/proyecto"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://cuelloni:Siempreeshoy02@cuelloni.mysql.pythonanywhere-services.com/cuelloni$default"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

# Defino la tabla

class Producto(db.Model):  
    
    id = db.Column(db.Integer, primary_key=True) # Defino los campos de la tabla
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre, precio, stock, imagen): # Constructor de la clase
        
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

   

with app.app_context():
    db.create_all()     # Creacion de todas las tablas


class ProductoSchema(ma.Schema):
   
    class Meta:
        fields = ("id", "nombre", "precio", "stock", "imagen")

producto_schema = ProductoSchema()                  # Trae un producto  
productos_schema = ProductoSchema(many=True)        # Trae multiples registros de productos

# Decorador inicial

@app.route('/')         
def hello_world():
    return 'Hello from Flask!'

@app.route("/productos", methods=["GET"])
def get_Productos():
   
    all_productos = Producto.query.all()  
    result = productos_schema.dump(all_productos)  # Trae todos los registros de la tabla 
    return jsonify(result)  


@app.route("/productos/<id>", methods=["GET"])
def get_producto(id):
   
    producto = Producto.query.get(id)  
    return producto_schema.jsonify(producto)  

@app.route("/productos/<id>", methods=["DELETE"])
def delete_producto(id):
   
    producto = Producto.query.get(id) 
    db.session.delete(producto)  
    db.session.commit()  
    return producto_schema.jsonify(producto)  

@app.route("/productos", methods=["POST"])  
def create_producto():
   
    nombre = request.json["nombre"]  
    precio = request.json["precio"]  
    stock = request.json["stock"]  
    imagen = request.json["imagen"]  
    new_producto = Producto(nombre, precio, stock, imagen)  
    db.session.add(new_producto)  
    db.session.commit()  
    return producto_schema.jsonify(new_producto)  

@app.route("/productos/<id>", methods=["PUT"])  
def update_producto(id):
   
    producto = Producto.query.get(id)  

    
    producto.nombre = request.json["nombre"]
    producto.precio = request.json["precio"]
    producto.stock = request.json["stock"]
    producto.imagen = request.json["imagen"]

    db.session.commit()  
    return producto_schema.jsonify(producto)  

# Decorador para despedirse 

@app.route('/bye')         
def hello_world():
    return 'Bye from Flask!'

if __name__ == "__main__":
    
    app.run(debug=True, port=5000)

   