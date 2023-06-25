import os
import threading
import schedule
import time
import datetime
import csv
from flask import Flask, jsonify, request

app = Flask(__name__)

kv_store = {}

def sync_kvs_from_file():
    current_datetime = datetime.datetime.now()
    print("Starting to read file: " + str(current_datetime))
    kv_file_name = os.getenv("KV_FILE_PATH") + "/kv_file.csv"

    try:
        with open(kv_file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            i = 0
            for row in csvreader:
                i = i + 1
                print("readling line " + str(i))
                print (str(row))
                key = row[0]
                value = row[1]
                is_deleted = row[2]

                if is_deleted=='true':
                    if key in kv_store.keys():
                        kv_store.pop(key)
                    else: 
                        print(f"pop key {key} does not exist but we continue")
                else:
                    kv_store[key] = value
    except FileNotFoundError:
        print("file does not exist")

@app.route('/kvs/<string:key>', methods=['GET'])
def get_value(key):
    try:
        value = kv_store[key]
        return jsonify({ key: value})
    except KeyError:
        return jsonify({'error': 'Key not found'}), 404

@app.route('/kvs', methods=['PUT'])
def put_value():
    kvs = request.get_json()
    kvs_to_put = ""

    for kv in kvs:
        key= kv.get('key')
        value = kv.get('value')
        if key and value:
            kv_store[key] = value
            kvs_to_put += key + "," + value + ",false\n"
        else:
            return jsonify({'error': 'key or value is missing'}), 400
    
    write_kvs_to_file(kvs_to_put)

    return jsonify({'message': 'PUT successful'}), 200
    
@app.route('/kvs', methods=['DELETE'])
def delete_value():
    kvs = request.get_json()
    kvs_to_delete = ""

    for kv in kvs:
        try:
            key= kv.get('key')
            value = kv_store.pop(key)
            kvs_to_delete += key + "," + value + ",true\n"
        except KeyError:
            return jsonify({'error': 'Key not found'}), 404
    
    write_kvs_to_file(kvs_to_delete)

    return jsonify({'message': 'DELETE successful'}), 200

def write_kvs_to_file(kvs_to_delete):
    kv_file_name = os.getenv("KV_FILE_PATH") + "/kv_file.csv"
    with open(kv_file_name, "a") as file:
        file.write(kvs_to_delete)
    
@app.route('/kvs/debug', methods=['GET'])
def print_kv_store():
        return jsonify(kv_store), 200


def schedule_background_job():
    while True:
        sync_kvs_from_file()
        time.sleep(5)
 
if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=schedule_background_job)
    scheduler_thread.start()

    app.run(debug=True,host="0.0.0.0", port=5001)


