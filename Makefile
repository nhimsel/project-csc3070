.PHONY: build clean run help

# Build the executable
build:
	pyinstaller --noconfirm --windowed --name buddy --add-data "Project/anims;anims" --collect-all PySide6 Project/main.py

# Help target
help:
	@echo "Available targets:"
	@echo "  make build   - Build executable with PyInstaller (default)"
	@echo "  make clean   - Remove build artifacts (build/, dist/, *.spec)"
	@echo "  make run     - Run the built executable"
	@echo "  make help    - Show this help message"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@powershell -command "Remove-Item -Path 'build', 'dist', '*.spec' -Recurse -Force -ErrorAction SilentlyContinue"
	@echo "Clean complete."

# Run the built executable
run:
	.\dist\buddy\buddy.exe

.DEFAULT_GOAL := build
