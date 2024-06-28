from flask import request, jsonify
from config import app, db
from models import Task
from datetime import datetime

# @app.route('/')
# def nothing_here():
#     return "Welcome to the backend database created"

# This is for posting in the database a new task, when the user creates a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        entity_name=data['entity_name'],
        task_type=data['task_type'],
        task_time=datetime.strptime(data['task_time'], '%Y-%m-%d %H:%M:%S'),
        contact_person=data['contact_person'],
        note=data.get('note', None),
        status=data.get('status', 'open')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created!'}), 201

# This is for Getting/Requesting all the data from the database to show the viewer and returns in the form of json
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{
        'id': task.id,
        'dateCreated': task.date_created,
        'entityName': task.entity_name,
        'taskType': task.task_type,
        'taskTime': task.task_time,
        'contactPerson': task.contact_person,
        'note': task.note,
        'status': task.status
    } for task in tasks]
    return jsonify(tasks_list)

# This goes for editing an existing task, when the user feels like editing a pre-existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found!'}), 404
    
    task.entity_name = data.get('entity_name', task.entity_name)
    task.task_type = data.get('task_type', task.task_type)
    task.task_time = datetime.strptime(data['task_time'], '%Y-%m-%d %H:%M:%S') if 'task_time' in data else task.task_time
    task.contact_person = data.get('contact_person', task.contact_person)
    task.note = data.get('note', task.note)
    task.status = data.get('status', task.status)

    db.session.commit()
    return jsonify({'message': 'Task updated!'})

# This is for deleting, when the user feels like deleting a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found!'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# endpoints
# /tasks/   -> POST
# /tasks/   -> GET
# /tasks/<int:id>   -> PUT
# /tasks/<int:id>   -> DELETE
