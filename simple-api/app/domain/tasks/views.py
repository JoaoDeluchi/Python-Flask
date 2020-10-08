from flask import Blueprint, jsonify, request

app_tasks = Blueprint('app.tasks', __name__)

@app_tasks.route('/tasks', methods=['GET'])
def get():
    tasks = {
        "title": "title",
        "updated_at": "updatedat",
        "created": "created",
        "state": "on Development",
    }
    return jsonify(tasks), 200
