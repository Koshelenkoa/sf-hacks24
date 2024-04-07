from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
with open('config.json') as config_file:
    config_data = json.load(config_file)

client = MongoClient(config_data['mongo_db_client'])  # Connecting to MongoDB
db = client['mydatabase']
records_collection = db['recors']
form_collection = db['forms']

@app.route('/records', methods=['GET'])
def get_items():
    # Get query parameters
    query_params = request.args.to_dict()

    # Retrieve items based on query parameters
    item = records_collection.find_one(query_params)

    if item:
        json = jsonify(item)
        return json['prod_id'], 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/forms', methods=['GET'])
def get_items():
    # Get query parameters
    query_params = request.args.to_dict()

    # Retrieve items based on query parameters
    items = form_collection.find(query_params)

    # Convert items to list of dictionaries
    items_list = [item for item in items]

    return jsonify(items_list)

@app.route('/records', methods=['POST'])
def add_item():
    data = request.json  
    try:
        records_collection.insert_one(data)  # Inserting data into MongoDB
        return jsonify({"message": "Item added successfully"}), 201
    except:
        return 500

@app.route('/forms', methods=['POST'])
def add_item():
    data = request.json 
    try:
        form_collection.insert_one(data)  # Inserting data into MongoDB
        return jsonify({"message": "Item added successfully"}), 201
    except:
        return 500
    
@app.route('/ips', methods=['GET'])
def update_ips():
    client_ip = request.remote_addr  # Get IP address of the client making the request
    try:
        with open('ips.json', 'r') as f:
            ips = json.load(f)  # Load the list of IPs from the JSON file
    except FileNotFoundError:
        ips = []  # If file doesn't exist yet, create an empty list

    ips.append(client_ip)  # Append client's IP to the list

    with open('ips.json', 'w') as f:
        json.dump(ips, f)  # Save the updated list back to the JSON file

    return ips, 200

if __name__ == '__main__':
    app.run(debug=True)
