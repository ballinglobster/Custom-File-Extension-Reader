import threading
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from pathlib import Path
import base64
from Compress import compress_file_as_gzip
import subprocess
import sys

class Backend(QObject):
    compressionFinished = pyqtSignal(str)
    compressionFailed = pyqtSignal(str)
    frameReady = pyqtSignal(bytes, int, int)

    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = Path(base_dir)

    @pyqtSlot(str, str)
    def receiveFile(self, filename, data_b64):
        try:
            incoming = self.base_dir / "incoming"
            incoming.mkdir(exist_ok=True)
            target = incoming / filename
            with open(target, 'wb') as f:
                f.write(base64.b64decode(data_b64))
            out = target.with_suffix(target.suffix + '.gz')
            compress_file_as_gzip(target, out)
            self.compressionFinished.emit(str(out))
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