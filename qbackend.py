import threading
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from pathlib import Path
import base64
from Compress import compress_file_as_gzip, compress_file_as_7z, compress_file_as_zip
from Decompress import decompress_file_from_gzip, decompress_file_from_7z, decompress_file_from_zip
import subprocess
import sys
import os
import tempfile

class Backend(QObject):
    compressionFinished = pyqtSignal(str)
    compressionFailed = pyqtSignal(str)
    frameReady = pyqtSignal(bytes, int, int)

    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = Path(base_dir)

    @pyqtSlot(str, str, str)
    def receiveFileForCompression(self, filename, data_b64, method):
        try:
            incoming = self.base_dir / "incoming"
            incoming.mkdir(exist_ok=True)
            # target = incoming / filename
            # with open(target, 'wb') as f:
            #     f.write(base64.b64decode(data_b64))
            fd, tmp = tempfile.mkstemp(prefix="upload_", suffix=".tmp", dir=str(incoming))
            os.close(fd)
            temp_path = Path(tmp)
            try:
                with open(temp_path, 'wb') as f:
                    f.write(base64.b64decode(data_b64))
            
                method = (method or "gzip").lower()
                if method in ("7z", "7zip"):
                    output_path = incoming / (filename + ".7z")
                    compress_file_as_7z(temp_path, output_path, arcname=filename)
                elif method in ("zip",):
                    output_path = incoming / (filename + ".zip")
                    compress_file_as_zip(temp_path, output_path, arcname=filename)
                else:
                    output_path = incoming / (filename + ".gz")
                    compress_file_as_gzip(temp_path, output_path)

                self.compressionFinished.emit(str(output_path))
            finally:
                try:
                    if temp_path.exists():
                        temp_path.unlink()
                except Exception:
                    pass
        except Exception as e:
            self.compressionFailed.emit(str(e))

    @pyqtSlot(str, str, str)
    def receiveFileForDecompression(self, filename, data_b64, method):
        try:
            incoming = self.base_dir / "incoming"
            incoming.mkdir(exist_ok=True)
            target = incoming / filename
            with open(target, 'wb') as f:
                f.write(base64.b64decode(data_b64))
            
            method = (method or "gzip").lower()
            if method in ("7z", "7zip"):
                output_path = target.with_suffix("")
                decompress_file_from_7z(target, output_path)
            elif method in ("zip",):
                output_path = target.with_suffix("")
                decompress_file_from_zip(target, output_path)
            else:
                output_path = target.with_suffix("")
                decompress_file_from_gzip(target, output_path)

            self.compressionFinished.emit(str(output_path))
        except Exception as e:
            self.compressionFailed.emit(str(e))
    

    @pyqtSlot()
    def launchDoom(self):
        print("Launching Doom...")
        try:
            iwad = str(self.base_dir / "Secrets" / "Doom" / "freedoom2.wad")
            exe_candidates = [ 
                str(self.base_dir / "Secrets" / "Doom" / "gzdoom.exe"),
                "gzdoom"
            ]

            import shutil
            for name in ["gzdoom.exe", "gzdoom"]:
                path = shutil.which(name)
                if path and path not in exe_candidates:
                    exe_candidates.append(path)

            last_exc = None
            for exe in exe_candidates:
                try:
                    print(f"Trying to launch Doom with: {exe}")
                    subprocess.Popen([exe, '-iwad', iwad], cwd=str(self.base_dir))
                    print("Doom launched successfully.", exe)
                    return
                except FileNotFoundError as fnf:
                    last_exc = fnf
                    print(f"Could not find executable: {exe}")
                    continue
                except Exception as e:
                    last_exc = e
                    print(f"Failed to launch Doom with {exe}: {e}")
                    continue
            
            msg = f"No DOOM engine found or all launches failed. Last error: {last_exc}"
            print(msg)
            self.compressionFailed.emit(msg)
        except Exception as e:
            print(f"Unexpected error launching Doom: {e}")
            self.compressionFailed.emit(str(e))