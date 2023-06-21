from flask import Flask, jsonify, request

app = Flask(__name__)

memory_store = {}

@app.route('/get', methods=['GET'])
def get_value():
    key = request.args.get('key')
    try:
        value = memory_store[key]
        return jsonify({ key: value})
    except:
        return jsonify({ key: None})

@app.route('/put', methods=['PUT'])
def put_value():
    key = request.args.get('key')
    value = request.args.get('value')

    if key and value:
        memory_store[key] = value
        return jsonify({'message': f'Key "{key}" updated with value "{value}"'}), 201
    else:
        return jsonify({'error': 'key or value is missing'}), 400

        



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001) 
