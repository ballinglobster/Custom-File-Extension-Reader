# import tkinter as tk
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWebChannel import QWebChannel
from qbackend import Backend
import subprocess

# root = tk.Tk(
# root.title("Tk test"
# root.geometry("1920x1080"

class StyledWebEnginePage(QWebEnginePage):
    def javaScriptAlert(self, securityOrigin, msg):
        box = QMessageBox()
        box.setWindowTitle("Alert")
        box.setText(msg)
        box.setStyleSheet("QMessageBox{ background: #ffd; text-align: left; } QMessageBox QLabel { color: #000; text-align: left; }")
        box.setIcon(QMessageBox.Information)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()


QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)


def load_file_into_view(view, path: Path):
    html = path.read_text(encoding='utf-8')
    base = QUrl.fromLocalFile(str(path.parent) + '/')
    view.setHtml(html, base)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) 
    file_path = base_dir / "test.lobsterdev"

    main_window = QWidget()
    layout = QVBoxLayout(main_window)


    web_view = QWebEngineView()
    # layout.addWidget(web_view)

    web_view.setPage(StyledWebEnginePage(web_view))
    layout.addWidget(web_view)
    

    # add QWebChannel bridge
    channel = QWebChannel()
    backend = Backend(base_dir)
    channel.registerObject("backend", backend)
    web_view.page().setWebChannel(channel)

    # Set same background colour for page and view
    page_bg = QColor(20, 20, 20)
    web_view.page().setBackgroundColor(page_bg)
    web_view.setStyleSheet("background: rgb(20, 20, 20);")
    web_view.setAttribute(Qt.WA_OpaquePaintEvent, True)

    web_view.setWindowTitle("Custom Extension File Reader")
    

    if file_path.exists():
        load_file_into_view(web_view, file_path)
    else:
        web_view.setHtml("<h1>File not found</h1>")

    backend.compressionFinished.connect(lambda p: QMessageBox.information(main_window, "Success", f"File compressed to: {p}"))
    backend.compressionFailed.connect(lambda e: QMessageBox.critical(main_window, "Error", f"Compression failed: {e}"))

    # web_view.resize(1200, 800)
    # web_view.show()
    # window.resize(1200, 800)
    # window.show()
    # web_view.showFullScreen()

    main_window.resize(1200, 800)
    main_window.setWindowTitle("Custom Extension File Reader")
    main_window.show()

    sys.exit(app.exec_())



