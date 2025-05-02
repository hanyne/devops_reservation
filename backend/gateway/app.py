from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://user-service:5001"
SALLE_SERVICE_URL = "http://salle-service:5002"
RESERVATION_SERVICE_URL = "http://reservation-service:5003"

def forward_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, **kwargs)
        resp.raise_for_status()  # Lève une exception pour 4xx ou 5xx
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"HTTP error from microservice: {str(e)}", "details": resp.text}), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON returned", "raw": resp.text}), 502

@app.route('/auth/<path:path>', methods=['GET'])
def auth_proxy(path):
    return forward_request("GET", f"{USER_SERVICE_URL}/auth/{path}", params=request.args)

@app.route('/users', methods=['GET', 'POST'])
def users_proxy():
    if request.method == 'GET':
        return forward_request("GET", f"{USER_SERVICE_URL}/users", headers=request.headers)
    else:
        return forward_request("POST", f"{USER_SERVICE_URL}/users", json=request.get_json(), headers=request.headers)

@app.route('/salles', methods=['GET', 'POST'])
def salles_proxy():
    if request.method == 'GET':
        return forward_request("GET", f"{SALLE_SERVICE_URL}/salles", headers=request.headers)
    else:
        return forward_request("POST", f"{SALLE_SERVICE_URL}/salles", json=request.get_json(), headers=request.headers)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations_proxy():
    if request.method == 'GET':
        return forward_request("GET", f"{RESERVATION_SERVICE_URL}/reservations", headers=request.headers)
    else:
        return forward_request("POST", f"{RESERVATION_SERVICE_URL}/reservations", json=request.get_json(), headers=request.headers)

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def reservation_delete_proxy(reservation_id):
    return forward_request("DELETE", f"{RESERVATION_SERVICE_URL}/reservations/{reservation_id}", headers=request.headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
