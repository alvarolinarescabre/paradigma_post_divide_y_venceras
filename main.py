import os
import json
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializamos Flask, la Base de Datos SQLIte3 y el Marshmallow
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hello.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Declaramos el modelo de datos a utilizar
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(80), unique=True)

    def __init__(self, person):
      self.person = person

# Declaramos el esquema de Marshmallow a presentar cuando realizamos el GET
class PersonSchema(ma.Schema):
    class Meta:
      fields = ['person']

persons_schema = PersonSchema(many=True)

# Creamos el modelo
db.create_all()

# Consultamos todos los usuarios de la base de datos
@app.route("/hello/", methods=["GET"])
def get():
   query = Person.query.all()
   result = persons_schema.dump(query)
   
   return jsonify(result.data)
 
 # Insertamos usuarios en la base de datos
@app.route("/hello/", methods=["POST"])
def post():
   person = request.json['person']
   new_person = Person(person)
   db.session.add(new_person)
   db.session.commit()

   return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 

# Actualizamos usuarios en la base de datos
@app.route("/hello/<id>", methods=["PUT"])
def put(id):
   query = Person.query.get(id)
   person = request.json['person']
   query.person = person
   db.session.commit()
  
   return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 

# Eliminamos usuarios en la base de datos
@app.route("/hello/<id>", methods=["DELETE"])
def delete(id):
   query = Person.query.get(id)
   db.session.delete(query)
   db.session.commit()

   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
