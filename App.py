import tkinter as tk
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


# root = tk.Tk(
# root.title("Tk test"
# root.geometry("1920x1080"

def load_file_into_view(view, path: Path):
    html = path.read_text(encoding='utf-8')
    base = QUrl.fromLocalFile(str(path.parent) + '/')
    view.setHtml(html, base)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    web_view = QWebEngineView()
    base_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) 
    file_path = base_dir / "test.lobsterdev"

    if file_path.exists():
        load_file_into_view(web_view, file_path)
    else:
        web_view.setHtml("<h1>File not found</h1>")
    web_view.resize(1200, 800)
    web_view.show()
    # web_view.showFullScreen()
    sys.exit(app.exec_())



