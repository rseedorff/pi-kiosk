from flask import Flask, jsonify
app = Flask(__name__)

# This route will return a object in JSON format
@app.route('/')
def index():
    return jsonify(result='Hello World !')

if __name__ == '__main__':
    app.debug = True
    app.run()
