import os
from pathlib import Path

# top-level project folder
PROJ_ROOT_DIR = Path(os.getcwd())

# directory to store uploaded files
FILE_DIR = Path(f"{PROJ_ROOT_DIR}/uploaded_files")

# mock data for unit tests
MOCK_DATA_DIR = Path(f"{PROJ_ROOT_DIR}/tests/mock_data")

# allowed extensions for files
ALLOWED_EXTENSIONS = {"csv"}

SECRET_KEY = "sunshine"