import os
from pathlib import Path

PROJ_ROOT_DIR = Path(os.getcwd())
FILE_DIR = Path(f"{PROJ_ROOT_DIR}/uploaded_files")
MOCK_DATA_DIR = Path(f"{PROJ_ROOT_DIR}/tests/mock_data")
ALLOWED_EXTENSIONS = {"csv"}
SECRET_KEY = "sunshine"