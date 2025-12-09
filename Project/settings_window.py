"""
Settings Editor UI for PySide6.
--------------------------------

This widget loads and saves config.json using config.py,
displays editable fields, and allows saving updates back to disk.

You can embed this widget inside a main window or reuse it as a dialog.
"""

import json
from pathlib import Path
from typing import Any, Dict

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
)
from PySide6.QtGui import QScreen
import config


class SettingsUI(QWidget):
    """
    A JSON settings editor integrated with config.py.

    Loads defaults from config.DEFAULTS and reads/writes to config.json.
    """

    def __init__(self, parent=None):
        super().__init__()

        # Use the script directory (Project/) to locate config.json
        script_dir = Path(__file__).resolve().parent
        self.config_path = script_dir / "config.json"
        self.config: Dict[str, Any] = {}

        # --------------------------------------------------
        # Main Layout
        # --------------------------------------------------
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # --------------------------------------------------
        # Fields (from config.DEFAULTS)
        # --------------------------------------------------
        self.api_url_field = QLineEdit()
        self.hide_on_fullscreen_field = QCheckBox()
        self.outfit_field = QLineEdit()

        form.addRow("API URL:", self.api_url_field)
        form.addRow("Hide on Fullscreen:", self.hide_on_fullscreen_field)
        form.addRow("Outfit:", self.outfit_field)

        layout.addLayout(form)

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_config)

        """
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self.load_config)
        """

        layout.addWidget(self.save_btn)
        """
        layout.addWidget(self.reload_btn)
        """

        # Load config immediately
        self.load_config()

    # ======================================================
    # JSON Loading / Saving
    # ======================================================

    def load_config(self):
        """Load config.json using config.py and fill UI with values.
        
        Creates a default config file if one doesn't exist.
        """
        # Create default config if file doesn't exist
        if not self.config_path.exists():
            self._create_default_config()
        
        try:
            with self.config_path.open("r", encoding="utf-8") as f:
                self.config = json.load(f)

        except FileNotFoundError:
            # File doesn't exist, create it with defaults
            self._create_default_config()
            self.config = dict(config.DEFAULTS)
        except json.JSONDecodeError as e:
            # Invalid JSON, load defaults
            QMessageBox.warning(
                self,
                "Load Error",
                f"Invalid JSON in config file:\n{e}\n\nUsing defaults."
            )
            self.config = dict(config.DEFAULTS)
        except Exception as e:
            # Other errors
            QMessageBox.warning(
                self,
                "Load Error",
                f"Failed to load config:\n{e}\n\nUsing defaults."
            )
            self.config = dict(config.DEFAULTS)

        # Ensure missing keys still use defaults
        for key, default_value in config.DEFAULTS.items():
            if key not in self.config:
                self.config[key] = default_value

        # Fill UI fields
        self.api_url_field.setText(str(self.config["api_url"]))
        self.hide_on_fullscreen_field.setChecked(bool(self.config["hide_on_fullscreen"]))
        self.outfit_field.setText(str(self.config["outfit"]))

    def _create_default_config(self):
        """Create a config.json file with default values."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("w", encoding="utf-8") as f:
                json.dump(config.DEFAULTS, f, indent=4)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Config Creation Error",
                f"Failed to create default config file:\n{e}"
            )

    def save_config(self):
        """Save modified settings to config.json."""
        try:
            self.config["api_url"] = self.api_url_field.text()
            self.config["hide_on_fullscreen"] = self.hide_on_fullscreen_field.isChecked()
            self.config["outfit"] = self.outfit_field.text()

            with self.config_path.open("w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)

            QMessageBox.information(self, "Saved", "Configuration saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save config:\n{e}")