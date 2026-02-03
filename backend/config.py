import os
from datetime import timedelta

# Flask Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'public', 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'public', 'output')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Animation Settings
ANIMATION_SETTINGS = {
    'frame_duration': 100,  # milliseconds
    'drawing_speed': 0.3,   # 0-1, how fast to draw
    'pen_size': 3,
    'pen_color': (0, 0, 0),  # RGB
    'background_color': (255, 255, 255),  # RGB
}

# Video Settings
VIDEO_SETTINGS = {
    'fps': 30,
    'codec': 'libx264',
    'preset': 'medium',
}
