import json
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)
DNS_FILE = "dns_records.json"

def load_dns_records():
    try:
        with open(DNS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_dns_records(records):
    with open(DNS_FILE, "w") as file:
        json.dump(records, file)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    value = data.get('value')
    record_type = data.get('type')

    if not (name and value and record_type == 'A'):
        return jsonify({"error": "Invalid registration request"}), 400

    dns_records = load_dns_records()
    dns_records[name] = {"value": value, "type": record_type, "ttl": 10}
    save_dns_records(dns_records)

    return jsonify({"message": "Registration successful"}), 200

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    name = data.get('name')
    record_type = data.get('type')

    if not (name and record_type):
        return jsonify({"error": "Invalid DNS query"}), 400

    dns_records = load_dns_records()
    record = dns_records.get(name)

    if record and record['type'] == record_type:
        return jsonify({
            "type": record['type'],
            "name": name,
            "value": record['value'],
            "ttl": record['ttl']
        }), 200
    else:
        return jsonify({"error": "Record not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)
