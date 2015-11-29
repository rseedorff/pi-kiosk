from flask import Flask, jsonify
app = Flask(__name__)

# This route will return a object in JSON format
@app.route('/')
def index():
    return jsonify(result='Hello World !')

# This route will toogle some cool functions :)
@app.route('/toggle')
def toggle():
    return jsonify(result='Toggle !')

if __name__ == '__main__':
    app.debug = True
    app.run()
