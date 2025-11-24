import os
import time
import random
from pathlib import Path
from PySide6.QtCore import Qt, Signal, QTimer, QObject
from PySide6.QtGui import QMovie, QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QSystemTrayIcon
from tray import TrayIcon

# ensure in correct directory
source_dir = Path(__file__).parent.resolve()
anim_dir = source_dir / "anims"

class ShapedWindow(QWidget):
    chatSignal = Signal(int, int)
    killSignal = Signal()
    cur_anim = anim_dir / "default.gif"

    def __init__(self):
        image_path=os.path.join(anim_dir, self.cur_anim)
        super().__init__()

        self.idle_image = anim_dir / "default.gif"
        self.drag_gif   = anim_dir / "CrazyThrow.gif"
        self.is_dragging = False

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = None

        self.movie = None
        self.switch_gif(str(image_path))

        self.tray = TrayIcon(self)

        image_path = os.path.join(anim_dir, "talk.gif")
        self.play_gif_once(image_path)
        self.move_to_bottom_right()

        # to randomly have the buddy blink
        self.blinker = blink_timer()
        self.blinker.blinkEmitter.connect(self.one_blink)
        self.blinker.start()

        # --- Gravity variables ---
        self.vx = 0
        self.vy = 0
        self.gravity = 0.9
        self.friction = 0.7
        self.is_airborne = False

        # --- Momentum variables ---
        self.last_drag_x = None
        self.last_drag_time = None
        # Velocity history for better throw detection
        self.drag_history = []  # list of (timestamp, x, y)
        self.drag_history_window = 0.05  # seconds to look back (~100 ms)

        # Determine the floor position (screen bottom)
        screen = QGuiApplication.primaryScreen().geometry()
        self.floor_y = screen.bottom()

        # Physics timer (60 FPS)
        self.physics_timer = QTimer()
        self.physics_timer.timeout.connect(self.update_physics)
        self.physics_timer.start(16)  # ~60 FPS# --- Gravity variables ---
        self.vx = 0
        self.vy = 0
        self.gravity = 0.9
        self.friction = 0.8
        self.is_airborne = False

        # Determine the floor position (screen bottom)
        screen = QGuiApplication.primaryScreen().geometry()
        self.floor_y = screen.bottom()

        # Physics timer (60 FPS)
        self.physics_timer = QTimer()
        self.physics_timer.timeout.connect(self.update_physics)
        self.physics_timer.start(16)  # ~60 FPS

    def move_to_bottom_right(self):
        # Get desktop widget (screen size)
        screen_rect = QGuiApplication.primaryScreen().geometry()
        
        # Calculate x and y for lower right corner
        x = screen_rect.right() - self.width()
        y = screen_rect.bottom() - self.height()
        
        # Move the window
        self.move(x, y)

        self.vx = 0
        self.vy = 0
        self.is_airborne = False

    def update_physics(self):
        # No gravity while dragging
        if self.is_dragging:
            self.vy = 0
            self.vx = 0
            return

        x = self.x()
        y = self.y()

        # --- Horizontal motion ---
        x += self.vx

        # Bounce off left/right edges
        screen_geom = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geom.width()
        obj_width = self.width()

        # Hit left edge
        if x <= 0:
            x = 0
            self.vx = -self.vx * 0.8  # bounce with damping

        # Hit right edge
        elif x + obj_width >= screen_width:
            x = screen_width - obj_width
            self.vx = -self.vx * 0.8  # bounce with damping

        # Air friction vs ground friction
        if self.is_airborne:
            self.vx *= 0.97
        else:
            self.vx *= 0.80

        # threshold to stop micro-sliding
        if abs(self.vx) < 0.3:
            self.vx = 0

        # --- Vertical motion/apply gravity ---
        self.vy += self.gravity
        self.vy *= 0.99  # slight vertical drag

        new_y = y + self.vy

        # Collision with floor
        if new_y + self.height() >= self.floor_y:
            new_y = self.floor_y - self.height()
            self.vy = 0
            self.is_airborne = False

            if str(self.cur_anim) == str(self.drag_gif):
                self.switch_gif(self.idle_image)
        else:
            self.is_airborne = True

        self.move(x, new_y)

    # --- Load and display a new image or GIF ---
    def set_image(self, image_path:str):
        """Switch the displayed image or animation dynamically."""
        self.image_path = str(image_path)
        #is_gif = str(image_path).lower().endswith(".gif")

        # Stop previous movie if it exists
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None

        #if is_gif:
        self._init_gif()
        """
        else:
            self._init_static()
        """

    """
    def _init_static(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        region = self.alpha_region_from_pixmap(pixmap)
        self.setMask(region)
        self.label.setMask(pixmap.mask())
        self.resize(pixmap.size())
    """

    def _init_gif(self):
        self.movie = QMovie(str(self.image_path))
        self.label.setMovie(self.movie)
        self.movie.frameChanged.connect(self._update_mask)
        self.movie.start()

        first_frame = self.movie.currentPixmap()
        if not first_frame.isNull():
            self.resize(first_frame.size())

    def _update_mask(self):
        pix = self.movie.currentPixmap()
        if not pix.isNull():
            self.label.resize(pix.size())
            self.label.setMask(pix.mask())
            self.resize(pix.size())

    def switch_gif(self, animation:str):
        """
        this has been refactored and usage has changed.
        animation must now include the file extension
        ex "default.gif" instead of "default"
        
        DO NOT USE PNG. the mask renderer ain't working right; 
        I can't figure out why
        single frame gifs are fine tho
        """
        if (self.cur_anim!=animation):
            image_path=os.path.join(anim_dir, animation)
            self.cur_anim=image_path
            self.set_image(image_path)

    def play_gif_once(self, animation: str):
       """Play a GIF once, then revert to the previous animation."""
       if self.cur_anim == animation:
           return

       prev_anim = self.cur_anim
       image_path = os.path.join(anim_dir, animation)
       self.cur_anim = image_path

       if self.movie:
           self.movie.stop()
           self.movie.deleteLater()
           self.movie = None

       self.movie = QMovie(image_path)
       self.movie.setCacheMode(QMovie.CacheAll)
       self.label.setMovie(self.movie)
       self.movie.frameChanged.connect(self._update_mask)

       # Wait until the movie is valid and frame count is known
       def check_last_frame(frame_number):
           if self.movie.frameCount() > 0 and frame_number == self.movie.frameCount() - 1:
               # Stop movie and revert to previous animation
               self.movie.stop()
               self.switch_gif(prev_anim)

       self.movie.frameChanged.connect(check_last_frame)
       self.movie.start()
 
    
    # for exclusive use by blinker. blinks once
    def one_blink(self):
        # only send if less important anim
        if str(self.cur_anim) == str(self.idle_image):
            self.play_gif_once("blink.gif")
    
    # --- Dragging behavior ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.is_dragging = True
            self.vx = 0
            self.vy = 0
            self.last_drag_x = None   # reset drag tracking
            self.cur_anim = self.drag_gif
            self.switch_gif(str(self.drag_gif))

        # send message to open chat on right click
        if event.button() == Qt.RightButton:
            x=self.pos().x()+self.width()
            y=self.pos().y()+self.height()
            self.chatSignal.emit(x,y)

    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.LeftButton:
            new_pos = self.pos() + event.pos() - self.offset

            now = time.time()

            # Record drag history (t, x, y)
            self.drag_history.append((now, new_pos.x(), new_pos.y()))

            # Keep only the last N ms
            cutoff = now - self.drag_history_window
            self.drag_history = [(t, x, y) for (t, x, y) in self.drag_history if t >= cutoff]

            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        self.offset = None
        self.is_dragging = False
        self.is_airborne = True

        if len(self.drag_history) > 1:
            t0, x0, y0 = self.drag_history[0]
            t1, x1, y1 = self.drag_history[-1]

            dx = x1 - x0
            dy = y1 - y0

            # --- FIX: Only displacement, not velocity spikes ---
            throw_scale = 0.15   # tweak between 0.1–0.25
            vx = dx * throw_scale
            vy = dy * throw_scale

            # --- FIX: Cap velocities to prevent extreme motion ---
            max_speed = 30
            vx = max(-max_speed, min(max_speed, vx))
            vy = max(-max_speed, min(max_speed, vy))

            self.vx = vx
            self.vy = vy

        self.drag_history.clear()

        """
        if self.cur_anim == self.drag_gif:
            self.set_image(str(self.idle_image))
        """
        # instead use physics func to wait until buddy lands to switch
        # self.set_image(self.idle_image)        

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.raise_()
                self.activateWindow()

    def closeEvent(self, event):
        self.killSignal.emit()
        event.accept()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

class blink_timer(QObject):
    blinkEmitter = Signal()
    def __init__(self):
        super().__init__()

        self.blink_timer = QTimer()
        self.blink_timer.setSingleShot(True)
        self.blink_timer.timeout.connect(self.on_timeout)
    def start(self):
        self.schedule_time_random()
    def schedule_time_random(self):
        # time between 5s and 2m
        time = random.randint(5*1000, 2*60*1000)
        self.blink_timer.start(time)
    def on_timeout(self):
        self.blinkEmitter.emit()
        self.schedule_time_random()