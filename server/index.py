from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
import json

app = Flask(__name__)

# Enable CORS
CORS(app)

with open('config.json') as config_file:
    config_data = json.load(config_file)

client = MongoClient(config_data['mongo_db_client'])  # Connecting to MongoDB
db = client['mydatabase']
records_collection = db['recors']
form_collection = db['forms']

@app.route('/records', methods=['GET'])
def get_record_items():
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
def get_form_items():
    # Get query parameters
    query_params = request.args.to_dict()

    # Retrieve items based on query parameters
    items = form_collection.find(query_params)

    # Convert items to list of dictionaries
    items_list = [item for item in items]

    return jsonify(items_list)

@app.route('/records', methods=['POST'])
def add_record_item():
    try:
        data = request.json 
        records_collection.insert_one(data)  # Inserting data into MongoDB
        return jsonify({"message": "Record added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/forms', methods=['POST'])
def add_form_item():
    try:
        data = request.json 
        form_collection.insert_one(data)  # Inserting data into MongoDB
        return jsonify({"message": "Form added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
