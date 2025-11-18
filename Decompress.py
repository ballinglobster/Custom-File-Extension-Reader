import gzip
import shutil
from pathlib import Path
import py7zr

def decompress_file_from_gzip(input_path: Path, output_path: Path):
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def decompress_file_from_7z(input_path: Path, output_path: Path):
    with py7zr.SevenZipFile(input_path, 'r') as archive:
        archive.extractall(path=output_path.parent)