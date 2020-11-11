import os
from flask import abort
import pandas as pd
import config
import logging
from pathlib import Path

logger = logging.getLogger()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def directory_lookup(directory=config.FILE_DIR):
    try:
        assert os.path.exists(directory)
    except Exception as e:
        logger.error(e)
        abort(412, "problem reaching file directory; check config")


def get_fullpath(file):
    try:
        assert file in os.listdir(config.FILE_DIR)
    except Exception as e:
        logger.error(e)
        abort(404, "file not found in file directory")
    fullpath = Path(f"{config.FILE_DIR}/{file}")
    return fullpath


def format_date(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # infer_datetime_format is so very much faster.
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
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