import cydoomgeneric as cdg
import numpy as np
from typing import Optional, Tuple
import threading
from PyQt5.QtCore import pyqtSignal

resx = 640
resy = 400

frame_ready_callback = None  # type: Optional[callable]

def set_frame_ready_callback(cb):
    global frame_ready_callback
    frame_ready_callback = cb

def draw_frame(pixels: np.ndarray):
    arr = pixels.astype(np.uint8)
    if frame_ready_callback is not None:
        frame_ready_callback(arr.tobytes(), arr.shape[1], arr.shape[0])
    else:
        # No callback registered; ignore the frame or add logging if desired.
        pass

def get_key() -> Optional[tuple[int, int]]:
    return None

# Optional functions
# def sleep_ms(ms: int) -> None:
# def set_window_title(t: str) -> None:
# def get_ticks_ms() -> int:

def start_doom(iwad_path: str | None = None):
    args = []
    if iwad_path:
        args.extend(['-iwad', iwad_path])
    cdg.init(resx,
    resy,
    draw_frame,
    get_key,
    # sleep_ms=sleep_ms,
    # get_ticks_ms=get_ticks_ms,
    # set_window_title=set_window_title)
    )
    cdg.main(argv=args if args else None)  # Optional parameter argv=[...]