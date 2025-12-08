# what you likely want out of here is get_windows, get_windows_containing, find_video_players

import win32gui
import win32api
import psutil
from pycaw.pycaw import AudioUtilities
import win32process
from config import load

from PySide6.QtCore import QThread, Signal

HIDE_ON_FULLSCREEN_DEFAULT = False
try:
    hide_on_fullscreen = load("hide_on_fullscreen")
except Exception:
    hide_on_fullscreen = HIDE_ON_FULLSCREEN_DEFAULT


class VideoScanner(QThread):
    found = Signal(str)
    

    def run(self):
        if(hide_on_fullscreen):
            while True:
                match = find_fullscreen_windows()
                if match:
                    self.found.emit("hide")
                else:
                    self.found.emit("restore")
                self.sleep(1)
        else:
            while True:
                title = find_video_players()
                if title:
                    self.found.emit("popcorn.gif")
                else:
                    self.found.emit("default.gif")
                self.sleep(1)

# Callback function for EnumWindows
def enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd).strip()
        if title:
            windows.append((hwnd, title))

def get_windows():
    # Get all visible windows
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    
    # Extract window titles
    window_titles = [title for hwnd, title in all_windows]
    return window_titles
    
    """
    # Print all window titles
    print("Open Window Titles (pywin32):")
    for idx, title in enumerate(window_titles, 1):
        print(f"{idx}. {title}")
    """

def get_windows_containing(win_title:str):
    # Get all visible windows
    all_windows = []
    win32gui.EnumWindows(enum_windows_callback, all_windows)
    
    # Extract window titles
    window_titles = [title for hwnd, title in all_windows]

    # Filter windows containing win_title
    matching_windows = [(hwnd, title) for hwnd, title in all_windows if win_title in title]
    return matching_windows


def is_fullscreen(hwnd):
    # Get the screen width and height
    screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    # Get window rectangle (left, top, right, bottom)
    rect = win32gui.GetWindowRect(hwnd)
    window_width = rect[2] - rect[0]
    window_height = rect[3] - rect[1]
    
    # Check if the window dimensions match screen size (considering a small tolerance)
    return window_width == screen_width and window_height == screen_height

def enum_windows(hwnd, result):
    # Filter only visible windows
    if win32gui.IsWindowVisible(hwnd):
        # Check if the window is fullscreen
        if is_fullscreen(hwnd):
            result.append(hwnd)


def find_fullscreen_windows():
    """Return the first non-desktop fullscreen window as a tuple
    (hwnd, title, pid, proc_name) or None if none found.
    Uses `enum_windows`/`is_fullscreen` and filters out desktop/explorer windows.
    """
    fullscreen_hwnds = []
    win32gui.EnumWindows(enum_windows, fullscreen_hwnds)

    for hwnd in fullscreen_hwnds:
        # skip common desktop/shell classes
        try:
            cls = win32gui.GetClassName(hwnd).lower()
        except Exception:
            cls = ""
        if cls in ("progman", "workerw"):
            continue

        title = get_window_title_from_hwnd(hwnd)
        if not title or not str(title).strip():
            continue
        if title.strip().lower() == "program manager":
            continue

        pid = get_process_id_from_hwnd(hwnd)
        proc_name = None
        try:
            proc = psutil.Process(pid) if pid else None
            proc_name = proc.name().lower() if proc else None
        except Exception:
            proc_name = None

        # skip explorer (desktop) windows
        if proc_name == 'explorer.exe':
            continue

        return (hwnd, title, pid, proc_name)

    return None

def is_audio_playing(hwnd):
    # Use PyCaw to check for audio playing applications
    sessions = AudioUtilities.GetAllSessions()
    hwnd_pid = get_process_id_from_hwnd(hwnd)

    for session in sessions:
        # Check if the audio session is active (playing) and associated with the right process
        if session.Process and session.Process.pid != 0 and session.Process.name().lower() != 'audiodg.exe':
            if session.State == 1:  # Active
                # Check if the session's process matches the window's process
                if session.Process.pid == hwnd_pid:
                    return True
    return False

def get_process_id_from_hwnd(hwnd):
    """Retrieve the process ID associated with a window handle."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        return None

def get_window_title_from_hwnd(hwnd):
    try:
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return None

def is_video_player(hwnd):
    # List of known processes that typically play videos
    known_video_processes = ['chrome.exe', 'firefox.exe', 'librewolf.exe', 'edge.exe', 'vlc.exe', 'mspmsnsv.dll', 'mpc-hc.exe', 'potplayer.exe', 'mpv.exe']
    
    try:
        # Get the process ID of the window
        pid = get_process_id_from_hwnd(hwnd)
        # Get the process name from psutil
        process = psutil.Process(pid)
        process_name = process.name().lower()
        
        return any(video_player in process_name for video_player in known_video_processes)
    except Exception as e:
        return False

def find_video_players():
    # List of fullscreen windows
    fullscreen_windows = []
    win32gui.EnumWindows(enum_windows, fullscreen_windows)

    # Check if any fullscreen windows are playing audio and are likely video players
    for hwnd in fullscreen_windows:
        #if is_audio_playing(hwnd) and is_video_player(hwnd):
        if is_audio_playing(hwnd):
            window_title = get_window_title_from_hwnd(hwnd)
            #print(f"Window '{window_title}' is fullscreen and playing audio.")
            return window_title
        else:
            window_title = get_window_title_from_hwnd(hwnd)
            #print(f"Window '{window_title}' is fullscreen but not playing audio.")
