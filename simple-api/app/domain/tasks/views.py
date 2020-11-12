from flask import Blueprint, jsonify, request
from app.domain.tasks.models import Task
from app.domain.tasks.actions import \
                                get as get_tasks, \
                                create as create_task, \
                                update as update_task, \
                                get_by_id as get_task_by_id, \
                                delete as delete_task

app_tasks = Blueprint('app.tasks', __name__)

@app_tasks.route('/tasks', methods=['GET'])
def get():
    filters = request.args
    tasks = get_tasks()
    return jsonify([task.serialize() for task in tasks]), 200


@app_tasks.route('/tasks', methods=['POST'])
def post():
    payload = request.get_json()
    return jsonify(create_task(payload).serialize()), 201


@app_tasks.route('/tasks/<id>', methods=['GET'])
def get_by_id(id):
    filters = request.args
    return jsonify(get_task_by_id(id).serialize()), 200


@app_tasks.route('/tasks/<id>', methods=['PUT'])
def put(id):
    payload = request.get_json()
    task = update_task(id, payload)
    return (jsonify(task.serialize()), 200)


@app_tasks.route('/tasks/<id>', methods=['DELETE'])
def delete(id):
    task = delete_task(id)
    return 'task deleted', 200
