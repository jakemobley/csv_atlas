import pytest
import logging
from pytest import raises
import pandas as pd
# import main
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
    with raises(Exception) as e:
        gu.directory_lookup(r"C:\not_there")


@pytest.mark.unittest
def test_get_fullpath_success():
    assert gu.get_fullpath('mock.csv', directory=config.MOCK_DATA_DIR) == Path(f"{config.MOCK_DATA_DIR}/mock.csv")


@pytest.mark.unittest
def test_get_fullpath_failure():
    with raises(Exception) as e:
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
