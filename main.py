import os
from flask import Flask, flash, request, url_for, render_template, send_file, abort, redirect
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
import config
import logging
import gen_utils as gu

logger = logging.getLogger()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(config.FILE_DIR)
app.secret_key = config.SECRET_KEY


@app.route('/')
def landing():
    gu.directory_lookup()
    # Show directory contents
    files = os.listdir(config.FILE_DIR)
    return render_template('file_list.html', files=files)


@app.route('/<file>')
def file_actions(file):
    gu.directory_lookup()
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory.")
    return render_template('actions.html', file=file)


@app.route('/download/<file>')
def download_file(file):
    fullpath = gu.get_fullpath(file)
    return send_file(fullpath)


@app.route('/display/<file>')
def display_file(file):
    # make sure file and path exist
    fullpath = gu.get_fullpath(file)

    df = None
    try:
        df = pd.read_csv(fullpath, parse_dates=True)
    except Exception as e:
        logger.error(e)
        abort(412, "Error parsing CSV file. Please check the file and try again.")

    # pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(df)
    page_df = gu.get_page_of_data(df, offset=offset, per_page=1000)
    page_df['state'].fillna("BLANK", inplace=True)
    pagination = Pagination(page=page, per_page=1000, total=total,
                            css_framework='bootstrap4')

    # create html table from df and display
    html_df = page_df.to_html()
    return render_template('file.html', file=file, shape=df.shape, table=html_df, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/stats/<file>')
def display_stats(file):
    # make sure file and path exist
    fullpath = gu.get_fullpath(file)

    # read df and run stats
    df = None
    try:
        df = pd.read_csv(fullpath, parse_dates=True)
    except Exception as e:
        logger.error(e)
        abort(412, "Error parsing CSV file. Please check the file and try again.")

    # format and run date statistics
    df = gu.format_date(df)
    stats_df = gu.run_stats(df)

    # pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(df)
    page_df = gu.get_page_of_data(stats_df, offset=offset, per_page=1000)
    pagination = Pagination(page=page, per_page=1000, total=total,
                            css_framework='bootstrap4')

    # create html table from df and display
    html_df = page_df.to_html(index=False)
    return render_template('stats.html', file=file, table=html_df, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if post request has the file info
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']

        # flash message if no file selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # do the thing
        if file and gu.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            gu.directory_lookup()
            try:
                file.save(Path(f"{app.config['UPLOAD_FOLDER']}/{filename}"))
            except Exception as e:
                logger.error(e)
                abort(500, "Oops! Something went wrong. Please try again.")
            return redirect(url_for("landing"))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
