import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, abort, redirect
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(config.FILE_DIR)
app.secret_key = config.SECRET_KEY


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/')
def file_list():
	# Show directory contents
	files = os.listdir(config.FILE_DIR)
	return render_template('file_list.html', files=files)


@app.route('/display/<file>')
def display_file(file):
	# Return 404 if path doesn't exist
	if not os.path.exists(config.FILE_DIR):
		return abort(412, "problem with file directory")
	if file not in os.listdir(config.FILE_DIR):
		return redirect(url_for('file_list'))  # add custom error handlers
	# create df to display
	full_filepath = Path(f"{config.FILE_DIR}/{file}")
	df = pd.read_csv(full_filepath)
	html_df = df.to_html()
	shape = df.shape
	return render_template('file.html', file=file, shape=df.shape, table=html_df)


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
