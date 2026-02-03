import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from config import ANIMATION_SETTINGS, VIDEO_SETTINGS

def is_allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_video_file(filename):
    """Check if file is a video"""
    VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm'}
    return filename.rsplit('.', 1)[1].lower() in VIDEO_EXTENSIONS if '.' in filename else False

def extract_video_frames(video_path, max_frames=30):
    """Extract frames from video"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_interval = max(1, total_frames // max_frames)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Resize frame to standard size
            frame = cv2.resize(frame, (800, 600))
            frames.append(frame)

        frame_count += 1
        if len(frames) >= max_frames:
            break

    cap.release()
    return frames

def apply_edge_detection(image):
    """Apply edge detection to highlight important features"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def create_animated_memo_frames(image_or_frames, output_dir):
    """
    Create animated memo-style frames from image or video frames
    Returns list of frame paths
    """
    if isinstance(image_or_frames, str):
        # It's an image path
        img = cv2.imread(image_or_frames)
        img = cv2.resize(img, (800, 600))
        frames = [img]
    else:
        frames = image_or_frames

    animated_frames = []

    for frame_idx, frame in enumerate(frames):
        # Get edges
        edges = apply_edge_detection(frame)

        # Convert back to BGR for processing
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Create animated sequence - draw edges gradually
        num_animation_steps = 20
        for step in range(num_animation_steps):
            progress = step / num_animation_steps

            # Create blank canvas
            canvas = np.ones_like(frame, dtype=np.uint8) * 255

            # Draw edges progressively
            edge_pixels = cv2.findNonZero(edges)
            if edge_pixels is not None:
                num_pixels = len(edge_pixels)
                num_to_draw = int(num_pixels * progress)

                for i in range(num_to_draw):
                    pt = tuple(edge_pixels[i][0])
                    cv2.circle(canvas, pt, 2, (0, 0, 0), -1)

            # Also blend with original gradually
            alpha = progress * 0.3
            result = cv2.addWeighted(canvas, 1 - alpha, frame, alpha, 0)

            # Save frame
            frame_path = os.path.join(output_dir, f'frame_{frame_idx:04d}_{step:02d}.png')
            cv2.imwrite(frame_path, result)
            animated_frames.append(frame_path)

    return animated_frames

def create_gif_from_frames(frame_paths, output_path, duration=100):
    """Create GIF from list of frame paths"""
    images = []
    for frame_path in frame_paths:
        img = Image.open(frame_path)
        images.append(img)

    if images:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0,
            optimize=False
        )

    return output_path

def create_video_from_frames(frame_paths, output_path, fps=30):
    """Create video from list of frame paths using OpenCV"""
    if not frame_paths:
        return None

    # Read first frame to get dimensions
    first_frame = cv2.imread(frame_paths[0])
    height, width = first_frame.shape[:2]

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write frames
    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    return output_path
