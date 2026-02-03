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

# Memo Style Presets (based on DS Ugoku Memo app)
# num_colors: how many colors (lower = more abstract)
# pixel_size: pixelation level (higher = more dotified)
MEMO_STYLES = {
    'classic': {
        'name': 'Classic Memo',
        'num_colors': 8,
        'pixel_size': 4,
        'description': 'Traditional DS memo app style - balanced colors and dots'
    },
    'minimalist': {
        'name': 'Minimalist Black & White',
        'num_colors': 2,
        'pixel_size': 3,
        'description': 'High contrast black and white only'
    },
    'detailed': {
        'name': 'Detailed Colors',
        'num_colors': 16,
        'pixel_size': 2,
        'description': 'More colors for better detail'
    },
    'heavy_dots': {
        'name': 'Heavy Dots',
        'num_colors': 6,
        'pixel_size': 6,
        'description': 'Large pixels for chunky dot effect'
    },
    'fine_dots': {
        'name': 'Fine Dots',
        'num_colors': 10,
        'pixel_size': 2,
        'description': 'Small pixels for finer detail'
    },
}

# Video Settings
VIDEO_SETTINGS = {
    'fps': 30,
    'codec': 'libx264',
    'preset': 'medium',
}
