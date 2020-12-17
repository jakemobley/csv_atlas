import pytest
import os
import logging
from pytest import raises
import pandas as pd
import config
import gen_utils as gu
from pathlib import Path
from pandas.util.testing import assert_frame_equal

logger = logging.getLogger(__name__)

mock_csv = Path(f"{config.MOCK_DATA_DIR}/mock.csv")


@pytest.mark.unittest
def test_allowed_file_success():
    file1, file2 = "something.csv", "yet_another_csv.csv"
    assert gu.allowed_file(file1) is True
    assert gu.allowed_file(file2) is True


@pytest.mark.unittest
def test_allowed_file_failure():
    file1, file2 = "something_else.jpg", "csv.jpg"

    assert gu.allowed_file(file1) is False
    assert gu.allowed_file(file2) is False


@pytest.mark.unittest
def test_directory_lookup_success():
    assert gu.directory_lookup() is None


@pytest.mark.unittest
def test_directory_lookup_failure():
    with raises(Exception):
        gu.directory_lookup(r"C:\not_there")


@pytest.mark.unittest
def test_get_fullpath_success():
    assert gu.get_fullpath('mock.csv', directory=config.MOCK_DATA_DIR) == Path(f"{config.MOCK_DATA_DIR}/mock.csv")


@pytest.mark.unittest
def test_get_fullpath_failure():
    with raises(Exception):
        gu.get_fullpath(r"C:\not_there")


@pytest.mark.unittest
def test_format_date():
    df = pd.read_csv(mock_csv)
    formatted_df = gu.format_date(df)
    assert formatted_df['date'].dtype == "datetime64[ns]"


@pytest.mark.unittest
def test_run_stats_success():
    expected_stats = pd.read_csv(f"{config.MOCK_DATA_DIR}/expected_stats.csv")
    df = pd.read_csv(mock_csv)
    formatted_df = gu.format_date(df)
    stats = gu.run_stats(formatted_df)
    assert_frame_equal(stats.reset_index(drop=True), expected_stats.reset_index(drop=True))


@pytest.mark.unittest
def test_run_stats_failure():
    expected_stats = pd.read_csv(f"{config.MOCK_DATA_DIR}/expected_stats.csv")
    df = pd.read_csv(mock_csv)
    formatted_df = gu.format_date(df)
    stats = gu.run_stats(formatted_df)
    try:
        assert_frame_equal(stats.reset_index(drop=True), df.reset_index(drop=True))
    except AssertionError:
        pass


@pytest.mark.unittest
def test_landing(client):
    res = client.get('/')
    assert res.status_code == 200


@pytest.mark.unittest
def test_landing_file_good(client):
    res = client.get('/example.csv')
    assert res.status_code == 200
    assert b'example.csv' in res.data


@pytest.mark.unittest
def test_landing_file_bad_filename(client):
    res = client.get('/nonexistent.csv')
    assert res.status_code == 404
    assert b'file not found in file directory' in res.data


@pytest.mark.unittest
def test_download(client):
    res = client.get('/download/example.csv')
    assert res.status_code == 200
    assert b'name,first,last,email' in res.data


@pytest.mark.unittest
def test_display(client):
    res = client.get('/display/fast.csv')
    assert res.status_code == 200
    x = res.data
    assert b'Guerrero' in res.data


@pytest.mark.unittest
def test_display_file_no_filename(client):
    res = client.get('/display/nonexistent.csv')
    assert res.status_code == 404
    assert b'file not found in file directory' in res.data

@pytest.mark.unittest
def test_display_file_bad_file(client):
    os.rename(Path(f"{config.MOCK_DATA_DIR}/bad.PNG"), Path(f"{config.FILE_DIR}/bad.PNG"))
    res = client.get('/display/bad.PNG')
    assert res.status_code == 502
    assert b'Error parsing CSV file' in res.data
    os.rename(Path(f"{config.FILE_DIR}/bad.PNG"), Path(f"{config.MOCK_DATA_DIR}/bad.PNG"))


@pytest.mark.unittest
def test_stats(client):
    res = client.get('/stats/fast.csv')
    assert res.status_code == 200
    assert b'Count date Year' in res.data and b'2050' in res.data


@pytest.mark.unittest
def test_stats_file_bad_file(client):
    os.rename(Path(f"{config.MOCK_DATA_DIR}/bad.PNG"), Path(f"{config.FILE_DIR}/bad.PNG"))
    res = client.get('/stats/bad.PNG')
    assert res.status_code == 502
    assert b'Error parsing CSV file' in res.data
    os.rename(Path(f"{config.FILE_DIR}/bad.PNG"), Path(f"{config.MOCK_DATA_DIR}/bad.PNG"))


@pytest.mark.unittest
def test_upload_file(client):

    def setup_and_teardown():
        for root, dir, files in os.walk(config.FILE_DIR):
            if "mock.csv" in files:
                os.remove(Path(f"{config.FILE_DIR}/mock.csv"))
        for root, dir, files in os.walk(config.FILE_DIR):
            assert "mock.csv" not in files

    setup_and_teardown()
    csv = Path(f"{config.MOCK_DATA_DIR}/mock.csv")
    data = {
        'file': (open(csv, 'rb'), csv)
    }
    res = client.post('/upload', data=data)
    assert res.status_code == 302
    for root, dir, files in os.walk(config.FILE_DIR):
        assert "mock.csv" in files
    setup_and_teardown()
