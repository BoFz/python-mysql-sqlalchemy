from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# se crea la conexion con la base de datos en mysql
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Se crea la clase Task donde se crea la tabla con el mismo nombre
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

# se crea todo
db.create_all()

# se crea el squema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# metodo para insertar una tarea
@app.route('/tasks', methods=['POST'])
def create_task():

# se reciben los datos y se guardan en una variable
    title = request.json['title']
    description = request.json['description']

# se crea la tarea
    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

# metodo para mostrar las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# metodo para mostrar una tarea, por su id
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# metodo para actualizar
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

# metodo para eliminar
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# ruta de inicio
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API Hijo de Puta'})


# se inicialisa la api 
if __name__ == "__main__":
    app.run(debug=True)



