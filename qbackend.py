from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from pathlib import Path
import base64
from Compress import compress_file_as_gzip

class Backend(QObject):
    compressionFinished = pyqtSignal(str)
    compressionFailed = pyqtSignal(str)

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