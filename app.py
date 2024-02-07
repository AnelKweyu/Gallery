from flask import Flask, flash, request, redirect, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
	if 'uploadFile[]' not in request.files:
		return redirect(request.url)
	files = request.files.getlist('uploadFile[]')
	file_names = []
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			msg  = 'Images successfully uploaded'
		else:
			msg  = 'Invalid Uplaod only png, jpg, jpeg, gif'
	return jsonify({'htmlresponse': render_template('response.html', msg=msg, filenames=file_names)})

if __name__ == "__main__":
    app.run(debug=True)
