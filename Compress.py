import gzip
import shutil
from pathlib import Path
import py7zr
import zipfile

def compress_file_as_gzip(input_path: Path, output_path: Path):
    with open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            with gzip.GzipFile(fileobj=f_out, mode='wb') as gz_out:
                shutil.copyfileobj(f_in, gz_out)

def compress_file_as_7z(input_path: Path, output_path: Path, arcname: str = None):
    with py7zr.SevenZipFile(output_path, 'w') as archive:
        archive.writeall(str(input_path), arcname or Path(input_path).name)

def compress_file_as_zip(input_path: Path, output_path: Path, arcname: str = None):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_path, arcname or Path(input_path).name)