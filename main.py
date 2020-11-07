import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, abort
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(config.FILE_DIR)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/')
def display():
	file = Path(f"{config.FILE_DIR}/example.csv")
	df = pd.read_csv(request.files.get(file))
	return render_template('index.html', shape=df.shape)


@app.route('/files/<file>')
def dir_listing(file):
	file_dir = Path(config.FILE_DIR)
	# Return 404 if path doesn't exist
	if not os.path.exists(file_dir):
		return abort(404, "problem with file directory")

	if file:
		return render_template('file.html', file=file)

	else:
		# Show directory contents
		files = os.listdir(file_dir)
		return render_template('file_list.html', files=files)

"""
		# Check if path is a file and serve
		if os.path.isfile(abs_path):
			return send_file(abs_path)"""


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(Path(f"{app.config['UPLOAD_FOLDER']}/{filename}"))
			return redirect(url_for('upload_file', filename=filename))
	return render_template('upload.html')


if __name__ == '__main__':
	app.run(debug=True)
