import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from pathlib import Path

FILE_DIR = r"C:\Users\jakem\projects\web-dev\csv_atlas\csv_atlas\uploaded_files"
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FILE_DIR


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def dir_listing():

	# Joining the base and the requested path
	abs_path = FILE_DIR

	# Return 404 if path doesn't exist
	if not os.path.exists(abs_path):
		return abort(404, "problem with file directory")

	"""
	# Check if path is a file and serve
	if os.path.isfile(abs_path):
		return send_file(abs_path)
	"""

	# Show directory contents
	files = os.listdir(abs_path)
	return render_template('index.html', files=files)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
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
