import gzip
import shutil
from pathlib import Path

def compress_file_as_gzip(input_path: Path, output_path: Path):
    with open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            with gzip.GzipFile(fileobj=f_out, mode='wb') as gz_out:
                shutil.copyfileobj(f_in, gz_out)

