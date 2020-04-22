import os
from flask import Flask, request, jsonify

from utils import * 
from audio import * 

app = Flask(__name__,
            static_url_path='/manray', 
            static_folder='static/manrayjs')

@app.route('/add', methods=['POST'])
def upload():
    app.logger.info('Add in successfully')

    return jsonify({"success": True}), 200

@app.route('/list', methods=['GET'])
def read():
    app.logger.info('List in successfully')

    return jsonify({"success": True}), 200
    

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)