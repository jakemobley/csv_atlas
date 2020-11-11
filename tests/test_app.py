import pytest
import logging
from pytest import raises
import pandas as pd
import main
import config
import gen_utils as gu
from pathlib import Path

logger = logging.getLogger(__name__)
# TODO: add unittest mark however I need to to make the warning go away


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
def test_directory_lookup():
    assert gu.directory_lookup() is None


@pytest.mark.unittest
def test_get_fullpath():
    assert gu.get_fullpath('faster.csv') == Path(f"{config.FILE_DIR}/faster.csv")


@pytest.mark.unittest
def test_format_date():
    mock_csv = Path(r"C:\Users\jakem\projects\web-dev\csv_atlas\csv_atlas\tests\mock_data\mock.csv")
    df = pd.read_csv(mock_csv)
    formatted_df = gu.format_date(df)
    a = formatted_df['date'].dtype
    assert formatted_df['date'].dtype == "datetime64[ns]"