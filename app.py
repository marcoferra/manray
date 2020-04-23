import os
from flask import Flask, request, jsonify, url_for, send_from_directory

import logging
from werkzeug.utils import secure_filename

from utils import * 
from audio import * 

UPLOAD_FOLDER = os.path.abspath("static/manrayjs") + "/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__,
            static_url_path='/manray', 
            static_folder='static/manrayjs')

logging.basicConfig(filename='demo.log', level=logging.DEBUG)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def reponse_ko():
    return jsonify({"resp": "KO"}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['POST'])
def upload():
    
    if request.method == 'POST':
        if 'bImage' not in request.files:
            return reponse_ko()
        
        file = request.files['bImage']
        
        if file.filename == '':
            return reponse_ko()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
            return jsonify({
                "filePath" : url_for('uploaded_file', filename=filename) 
                }), 200
    
    app.logger.info('Add in successfully')
    data = request.form.to_dict(flat=False)
    app.logger.info(request.form)
    app.logger.info(request.files)

    return jsonify({"success": True}), 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/list', methods=['GET'])
def read():
    app.logger.info('List in successfully')

    return jsonify({"success": True}), 200
    

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)