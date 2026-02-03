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
    'frame_duration': 80,  # milliseconds
    'animation_steps': 25,  # Number of frames per image/frame
    'drawing_speed': 0.3,   # 0-1, how fast to draw
    'pen_size': 3,
    'pen_color': (0, 0, 0),  # RGB (BGR in OpenCV)
    'background_color': (255, 255, 255),  # RGB
    'texture_intensity': 0.08,  # Paper texture intensity (0-1)
    'onion_skin_intensity': 0.15,  # Previous frame visibility (0-1)
    'color_blend_alpha': 0.2,  # Blend with original image (0-1)
    'animation_style': 'memo',  # 'memo', 'sketch', 'paint', 'bold'
}

# Memo Style Presets
MEMO_STYLES = {
    'memo': {
        'name': 'Classic Memo Notebook',
        'texture_intensity': 0.08,
        'onion_skin_intensity': 0.15,
        'pen_color': (0, 0, 0),
        'animation_steps': 25,
        'description': 'Traditional hand-drawn memo notebook style'
    },
    'sketch': {
        'name': 'Light Sketch',
        'texture_intensity': 0.12,
        'onion_skin_intensity': 0.1,
        'pen_color': (50, 50, 50),
        'animation_steps': 30,
        'description': 'Light and airy sketch style'
    },
    'paint': {
        'name': 'Watercolor Paint',
        'texture_intensity': 0.15,
        'onion_skin_intensity': 0.2,
        'pen_color': (40, 40, 40),
        'animation_steps': 20,
        'description': 'Soft watercolor painting style'
    },
    'bold': {
        'name': 'Bold Drawing',
        'texture_intensity': 0.05,
        'onion_skin_intensity': 0.08,
        'pen_color': (0, 0, 0),
        'animation_steps': 20,
        'description': 'High contrast bold drawing'
    },
}

# Video Settings
VIDEO_SETTINGS = {
    'fps': 30,
    'codec': 'libx264',
    'preset': 'medium',
}
