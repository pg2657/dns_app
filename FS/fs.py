from flask import Flask, request, jsonify
import requests
import json
import socket
import struct

app = Flask(__name__)


registration_data = {
    "hostname": "",
    "ip": "",
    "as_ip": "",
    "as_port": ""
}


def register_with_authoritative_server(hostname, ip, as_ip, as_port):
    dns_message = {
        "type": "A",
        "name": hostname,
        "value": ip,
        "ttl": 10
    }

    dns_request = struct.pack('!B', len(json.dumps(dns_message))) + json.dumps(dns_message).encode()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(dns_request, (as_ip, int(as_port)))


@app.route('/register', methods=['PUT'])
def register_hostname():
    data = request.json

    
    if not all(key in data for key in ["hostname", "ip", "as_ip", "as_port"]):
        return jsonify({"error": "Invalid registration request"}), 400

    
    registration_data["hostname"] = data["hostname"]
    registration_data["ip"] = data["ip"]
    registration_data["as_ip"] = data["as_ip"]
    registration_data["as_port"] = data["as_port"]

    
    register_with_authoritative_server(**data)

    return jsonify({"message": "Registration successful"}), 201


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    try:
        number = int(request.args.get('number'))
        result = calculate_fibonacci(number)
        return jsonify({"result": result}), 200
    except ValueError:
        return jsonify({"error": "Invalid format for 'number'"}), 400


def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
