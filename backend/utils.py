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

def posterize_image(image, num_colors=8):
    """
    Reduce color palette (posterization)
    Converts image to limited color palette like classic memo app
    """
    # Convert to appropriate color space
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    # K-means clustering to reduce colors
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit
    centers = np.uint8(centers)
    result = centers[labels.flatten()]
    result = result.reshape(image.shape)

    return result

def pixelate_image(image, pixel_size=4):
    """
    Pixelate/dot-ify the image
    Reduces resolution for classic memo style appearance
    """
    small = cv2.resize(image, (image.shape[1] // pixel_size, image.shape[0] // pixel_size),
                       interpolation=cv2.INTER_LINEAR)
    result = cv2.resize(small, (image.shape[1], image.shape[0]),
                        interpolation=cv2.INTER_NEAREST)
    return result

def convert_to_memo_style(image, num_colors=8, pixel_size=4):
    """
    Convert image to memo notebook style
    - Reduce colors to limited palette
    - Pixelate for dot-like appearance
    """
    # Reduce colors
    memo_image = posterize_image(image, num_colors)
    # Pixelate
    memo_image = pixelate_image(memo_image, pixel_size)
    return memo_image

def detect_frame_difference(frame1, frame2, threshold=30):
    """
    Detect differences between two frames
    Returns binary mask of changed pixels
    """
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary

def get_changed_pixels(frame1_memo, frame2_memo, threshold=30):
    """
    Get pixels that changed between frames
    Used for progressive animation drawing
    """
    diff_mask = detect_frame_difference(frame1_memo, frame2_memo, threshold)
    changed_pixels = cv2.findNonZero(diff_mask)
    return changed_pixels if changed_pixels is not None else []

def create_animated_memo_frames(image_or_frames, output_dir, num_colors=8, pixel_size=4):
    """
    Create animated memo-style frames from image or video frames
    Uses color reduction and pixelation like the classic DS memo app

    Args:
        image_or_frames: Path to image or list of video frames
        output_dir: Directory to save output frames
        num_colors: Number of colors to reduce to (default: 8)
        pixel_size: Pixel size for dotification (default: 4)

    Returns:
        List of animated frame paths
    """
    if isinstance(image_or_frames, str):
        # It's an image path
        img = cv2.imread(image_or_frames)
        img = cv2.resize(img, (800, 600))
        frames = [img]
    else:
        frames = image_or_frames

    # Convert all frames to memo style first
    memo_frames = []
    for frame in frames:
        memo_frame = convert_to_memo_style(frame, num_colors, pixel_size)
        memo_frames.append(memo_frame)

    animated_frames = []
    num_animation_steps = 15
    prev_memo_frame = np.ones_like(frames[0], dtype=np.uint8) * 255

    for frame_idx, memo_frame in enumerate(memo_frames):
        # Get changed pixels between this frame and previous
        changed_pixels = get_changed_pixels(prev_memo_frame, memo_frame, threshold=15)
        num_changes = len(changed_pixels)

        # Create animated sequence - draw changed pixels gradually
        for step in range(num_animation_steps):
            progress = step / num_animation_steps

            # Start with previous frame
            canvas = prev_memo_frame.copy()

            # Draw changed pixels progressively
            if num_changes > 0:
                num_to_draw = int(num_changes * progress)

                for i in range(num_to_draw):
                    pt = tuple(changed_pixels[i][0])
                    # Get color from target frame
                    color = tuple(memo_frame[pt[1], pt[0]])
                    cv2.circle(canvas, pt, 2, color, -1)

            # At final step, blend with full target frame
            if step == num_animation_steps - 1:
                canvas = memo_frame.copy()

            # Save frame
            frame_path = os.path.join(output_dir, f'frame_{frame_idx:04d}_{step:02d}.png')
            cv2.imwrite(frame_path, canvas)
            animated_frames.append(frame_path)

        prev_memo_frame = memo_frame.copy()

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
