from flask import Flask, jsonify, request

app = Flask(__name__)

kv_store = {}

@app.route('/kv-store', methods=['GET'])
def get_value():
    key = request.args.get('key')
    try:
        value = kv_store[key]
        return jsonify({ key: value})
    except KeyError:
        return jsonify({'error': 'Key not found'}), 404

@app.route('/kv-store', methods=['PUT'])
def put_value():
    key = request.args.get('key')
    value = request.args.get('value')

    if key and value:
        kv_store[key] = value
        msg = 'Key ' + key + ' updated with value ' + value
        return jsonify({'message': msg}), 200
    else:
        return jsonify({'error': 'key or value is missing'}), 400
    
@app.route('/kv-store', methods=['DELETE'])
def delete_value():
    key = request.args.get('key')
    if key:
        try:
            value = kv_store.pop(key)
            msg = 'Key ' + key + ' with value ' + value + ' was deleted'
            return jsonify({'message': msg}), 204
        except KeyError:
            return jsonify({'error': 'Key not found'}), 404
    else:
        return jsonify({'error': 'key or value is missing'}), 404
    
@app.route('/kv-store/debug', methods=['GET'])
def print_kv_store():
        return jsonify(kv_store), 200
   
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001) 
