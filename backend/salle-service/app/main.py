from flask import Flask, jsonify

app = Flask(__name__)

rooms = [
    {"id": 1, "name": "Salle 1", "capacity": 10},
    {"id": 2, "name": "Salle 2", "capacity": 20},
]

@app.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify(rooms)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
