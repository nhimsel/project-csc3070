import sys
import os
import time
from pathlib import Path
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QMovie, QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QSystemTrayIcon
from tray import TrayIcon

# ensure in correct directory
source_dir = Path(__file__).parent.resolve()
anim_dir = source_dir / "anims"

class ShapedWindow(QWidget):
    chatSignal = Signal(int, int)
    killSignal = Signal()
    cur_anim = "feesh"

    def __init__(self, animation):
        self.cur_anim=animation
        if self.cur_anim != "cat":
            anim_name=animation+".gif"
        else:
            anim_name=animation+".png"
        image_path=os.path.join(anim_dir, anim_name)
        super().__init__()

        self.idle_image = anim_dir / "cat.png"      # PNG first frame
        self.drag_gif   = anim_dir / "cat.gif"      # full GIF animation
        self.is_dragging = False

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = None

        self.movie = None
        self.set_image(image_path)

        self.tray = TrayIcon(self)

        self.move_to_bottom_right()

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

        if self.is_airborne:
            # gentle drag in air
            self.vx *= 0.97
        else:
            # strong friction on ground
            self.vx *= 0.80

        # threshold to stop micro-sliding
        if abs(self.vx) < 0.3:
            self.vx = 0

        # Vertical motion/apply gravity
        self.vy += self.gravity
        # Slight vertical drag so upward throws slow naturally
        self.vy *= 0.99
        new_y = y + self.vy

        # Collision with floor
        if new_y + self.height() >= self.floor_y:
            new_y = self.floor_y - self.height()
            self.vy = 0  # stop falling
            self.is_airborne = False
        else:
            self.is_airborne = True

        self.move(x, new_y)

    # --- Load and display a new image or GIF ---
    def set_image(self, image_path):
        """Switch the displayed image or animation dynamically."""
        self.image_path = image_path
        is_gif = image_path.lower().endswith(".gif")

        # Stop previous movie if it exists
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None

        if is_gif:
            self._init_gif()
        else:
            self._init_static()

    def _init_static(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        self.label.setMask(pixmap.mask())
        self.resize(pixmap.size())

    def _init_gif(self):
        self.movie = QMovie(self.image_path)
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

    def switch_gif(self, animation):
        if (self.cur_anim!=animation):
            self.cur_anim=animation
            if animation == "cat":
                self.set_image(str(self.idle_image))
            else:
                anim_name=animation+".gif"
                image_path=os.path.join(anim_dir, anim_name)
                self.set_image(image_path)


    # --- Dragging behavior ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.is_dragging = True
            self.vx = 0
            self.vy = 0
            self.last_drag_x = None   # reset drag tracking

            if self.cur_anim == "cat":
                self.set_image(str(self.drag_gif))

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

        if self.cur_anim == "cat":
            self.set_image(str(self.idle_image))


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
