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


def store_df(filename):
	# Return 404 if path doesn't exist
	if not os.path.exists(config.FILE_DIR):
		return abort(412, "problem with file directory")
	if not os.path.exists(config.DF_DIR):
		return abort(412, "problem with serialized df directory")
	full_filepath = Path(f"{config.FILE_DIR}/{filename}")
	file_stem = full_filepath.stem
	df = pd.read_csv(full_filepath)
	df.to_parquet(f'{config.DF_DIR}/{file_stem}.parquet.gzip', compression='gzip')


@app.route('/')
def file_landing():
	# Show directory contents
	files = os.listdir(config.FILE_DIR)
	return render_template('file_list.html', files=files)


@app.route('/<file>')
def file_list(file):
	# Return 404 if path doesn't exist
	if not os.path.exists(config.FILE_DIR):
		return abort(412, "problem with file directory")
	if file not in os.listdir(config.FILE_DIR):
		return redirect(url_for('file_list'))  # add custom error handlers
	return render_template('actions.html', file=file)


@app.route('/download/<file>')
def download_file(file):
	# Return 404 if path doesn't exist
	if not os.path.exists(config.FILE_DIR):
		return abort(412, "problem with file directory")
	if file not in os.listdir(config.FILE_DIR):
		return redirect(url_for('file_list'))  # add custom error handlers
	# create df to display
	full_filepath = Path(f"{config.FILE_DIR}/{file}")
	return send_file(full_filepath)


@app.route('/display/<file>')
def display_file(file):
	# Return 404 if path doesn't exist
	if file not in os.listdir(config.FILE_DIR):
		abort(404,"file not found.")  # TODO: add custom error handlers
	# create df to display
	file = file.split(".")[0]
	df_filepath = Path(f"{config.DF_DIR}/{file}.parquet.gzip")
	df = pd.read_parquet(df_filepath)
	# html_df = df.to_html()
	shape = df.shape
	return render_template('file.html', file=file, shape=df.shape, table=df)


"""

@app.route('/display/<file>')
def display_file(file):
	# Return 404 if path doesn't exist
	if file not in os.listdir(config.DF_DIR):
		return redirect(url_for('file_list'))  # add custom error handlers
	# create df to display
	full_filepath = Path(f"{config.FILE_DIR}/{file}")
	df = pd.read_csv(full_filepath)
	html_df = df.to_html()
	shape = df.shape
	return render_template('file.html', file=file, shape=df.shape, table=html_df)

"""

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
			store_df(filename)
			return redirect(url_for('upload_file', filename=filename))  # TODO: need success page
	return render_template('upload.html')


if __name__ == '__main__':
	app.run(debug=True)
