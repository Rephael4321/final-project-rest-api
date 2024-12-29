from flask import Flask, request, jsonify

ID = 1

app = Flask(__name__)

tasks = {}


@app.route('/tasks', methods=['GET'])
def getTasks() -> tuple[dict, int]:
    return jsonify(tasks), 200


@app.route('/tasks/<int:id>', methods=['GET'])
def getTask(id: int) -> tuple[dict, int]:
    try:
        return jsonify(tasks[id]), 200
    except KeyError:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks', methods=['POST'])
def addTask() -> tuple[dict, int]:
    global ID
    data = request.get_json()
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Bad request, data must include 'title' and 'description'"}), 400
    new_task = {'title': data['title'], 'description': data['description'], 'id': ID, 'complete': False}
    tasks[ID] = new_task
    ID += 1
    return jsonify(new_task), 201


@app.route('/tasks/<int:id>', methods=['DELETE'])
def deleteTask(id: int) -> tuple[dict, int]:
    try:
        return jsonify(tasks.pop(id)), 200
    except KeyError:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def updateTask(id: int) -> tuple[dict, int]:
    data = request.get_json()
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Bad request, data must include 'title' and 'description'"}), 400
    try:    
        tasks[id]['title'] = data['title']
        tasks[id]['description'] = data['description']
        return jsonify(tasks[id]), 200
    except KeyError:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:id>/complete', methods=['GET'])
def completeTask(id: int) -> tuple[dict, int]:
    try:
        tasks[id]['complete'] = True
        return jsonify(tasks[id]), 200
    except KeyError:
        return jsonify({"error": "Task not found"}), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
