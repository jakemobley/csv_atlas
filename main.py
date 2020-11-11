import os
from flask import Flask, flash, request, url_for, render_template, send_file, abort, redirect
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
import config
import logging

logger = logging.getLogger()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(config.FILE_DIR)
app.secret_key = config.SECRET_KEY


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def directory_lookup():
    try:
        assert os.path.exists(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(412, "problem reaching file directory; check config")


def format_date(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except ValueError:
                pass
    return df


def get_page_of_data(df, offset=0, per_page=10000):
    return df.iloc[offset: offset + per_page]


def run_stats(df):
    # find columns with datetime data types
    date_cols = df.select_dtypes(include=['datetime64'])
    new_df = pd.DataFrame()
    # loop through datetime column
    for col in date_cols:
        # convert datetime objects to just years
        df[col] = df[col].dt.year
        # create a series with a count of values for each year
        series = df[col].value_counts().reset_index().rename(columns={'index': f'{col}',
                                                                          'date': f'Count {col} Year'})
        series.sort_values(by=[f'{col}'], inplace=True)
        # add years in column as well as counts for each year to a new df
        new_df[col] = series[col]
        new_df[f"Count {col} Year"] = series[f"Count {col} Year"]
    print("hello")
    return new_df


@app.route('/')
def landing():
    directory_lookup()
    # Show directory contents
    files = os.listdir(config.FILE_DIR)
    return render_template('file_list.html', files=files)


@app.route('/<file>')
def file_list(file):
    directory_lookup()
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory.")
    return render_template('actions.html', file=file)


@app.route('/download/<file>')
def download_file(file):
    directory_lookup()
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory")
    full_filepath = Path(f"{config.FILE_DIR}/{file}")
    return send_file(full_filepath)


@app.route('/display/<file>')
def display_file(file):
    directory_lookup()
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory")
    fullpath = Path(f"{config.FILE_DIR}/{file}")

    df = None
    try:
        df = pd.read_csv(fullpath, parse_dates=True)
    except Exception as e:
        logger.error(e)
        abort(412, "Error parsing CSV file. Please check the file and try again.")

    # pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(df)
    page_df = get_page_of_data(df, offset=offset, per_page=1000)
    page_df['state'].fillna("BLANK", inplace=True)
    pagination = Pagination(page=page, per_page=1000, total=total,
                            css_framework='bootstrap4')
    # create html table from df and display
    html_df = page_df.to_html()
    return render_template('file.html', file=file, shape=df.shape, table=html_df, page=page, per_page=per_page,
                           pagination=pagination)


@app.route('/stats/<file>')
def display_stats(file):
    directory_lookup()
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory")
    fullpath = Path(f"{config.FILE_DIR}/{file}")

    df = None
    try:
        df = pd.read_csv(fullpath, parse_dates=True)
    except Exception as e:
        logger.error(e)
        abort(412, "Error parsing CSV file. Please check the file and try again.")
    df = format_date(df)
    stats_df = run_stats(df)
    # pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(df)
    page_df = get_page_of_data(stats_df, offset=offset, per_page=1000)
    pagination = Pagination(page=page, per_page=1000, total=total,
                            css_framework='bootstrap4')
    html_df = page_df.to_html(index=False)
    # create html table from df and display
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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory_lookup()
            try:
                file.save(Path(f"{app.config['UPLOAD_FOLDER']}/{filename}"))
            except Exception as e:
                logger.error(e)
                abort(500, "Oops! Something went wrong. Please try again.")
            return redirect(url_for("landing"))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
