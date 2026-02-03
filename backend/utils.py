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

def add_paper_texture(image, texture_intensity=0.1):
    """Add paper texture to the image"""
    height, width = image.shape[:2]

    # Create noise pattern
    noise = np.random.randint(240, 256, (height, width, 3), dtype=np.uint8)

    # Blend with original
    result = cv2.addWeighted(image, 1 - texture_intensity, noise, texture_intensity, 0)
    return result

def trace_contours(image):
    """Trace contours for smoother line drawing"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_stroke_with_pressure(canvas, points, start_idx, end_idx, color=(0, 0, 0)):
    """
    Draw stroke with varying pressure effect
    Simulates hand-drawn lines by varying thickness
    """
    if end_idx > len(points):
        end_idx = len(points)

    if end_idx <= start_idx:
        return

    segment = points[start_idx:end_idx]

    for i in range(len(segment) - 1):
        pt1 = tuple(segment[i][0])
        pt2 = tuple(segment[i + 1][0])

        # Vary stroke width based on position (pressure effect)
        progress = i / max(1, len(segment) - 1)
        thickness = max(1, int(3 + 2 * np.sin(progress * np.pi)))

        cv2.line(canvas, pt1, pt2, color, thickness, cv2.LINE_AA)

def create_animated_memo_frames(image_or_frames, output_dir, animation_style='memo'):
    """
    Create animated memo-style frames from image or video frames
    Returns list of frame paths

    animation_style:
      - 'memo': Hand-drawn memo notebook style with stroke animation
      - 'sketch': Sketch-like with lighter strokes
      - 'paint': Paint-like with blended colors
    """
    if isinstance(image_or_frames, str):
        # It's an image path
        img = cv2.imread(image_or_frames)
        img = cv2.resize(img, (800, 600))
        frames = [img]
    else:
        frames = image_or_frames

    animated_frames = []
    num_animation_steps = 25
    prev_canvas = None

    for frame_idx, frame in enumerate(frames):
        # Get contours for smoother line drawing
        contours = trace_contours(frame)

        # Get edges as fallback
        edges = apply_edge_detection(frame)
        edge_pixels = cv2.findNonZero(edges)

        # Create animated sequence - draw strokes gradually
        for step in range(num_animation_steps):
            progress = step / num_animation_steps

            # Create blank canvas with paper texture
            canvas = np.ones_like(frame, dtype=np.uint8) * 255
            canvas = add_paper_texture(canvas, texture_intensity=0.08)

            # Draw contours progressively (if available)
            if contours:
                total_points = sum(len(contour) for contour in contours)
                points_to_draw = int(total_points * progress)

                drawn = 0
                for contour in contours:
                    contour_len = len(contour)
                    if drawn + contour_len <= points_to_draw:
                        # Draw entire contour
                        draw_stroke_with_pressure(canvas, contour, 0, contour_len)
                        drawn += contour_len
                    else:
                        # Draw partial contour
                        remaining = points_to_draw - drawn
                        if remaining > 0:
                            draw_stroke_with_pressure(canvas, contour, 0, remaining)
                        break

            # Fallback: draw edges if no contours
            if not contours and edge_pixels is not None:
                num_pixels = len(edge_pixels)
                num_to_draw = int(num_pixels * progress)

                for i in range(num_to_draw):
                    pt = tuple(edge_pixels[i][0])
                    cv2.circle(canvas, pt, 2, (0, 0, 0), -1)

            # Add onion skin effect (show previous frame lightly)
            if prev_canvas is not None and step > 0:
                # Blend with previous frame at low alpha
                canvas = cv2.addWeighted(canvas, 0.7, prev_canvas, 0.15, 0)

            # Blend with original gradually for color preservation
            alpha = progress * 0.2
            result = cv2.addWeighted(canvas, 1 - alpha, frame, alpha, 0)

            # Save frame
            frame_path = os.path.join(output_dir, f'frame_{frame_idx:04d}_{step:02d}.png')
            cv2.imwrite(frame_path, result)
            animated_frames.append(frame_path)

            if step == num_animation_steps - 1:
                prev_canvas = canvas.copy()

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
