from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS
from utils import (
    is_allowed_file, is_video_file, extract_video_frames,
    create_animated_memo_frames, create_gif_from_frames, create_video_from_frames
)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@app.route('/api/transform', methods=['POST'])
def transform_media():
    """Transform image or video to animated memo style"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check file extension
        if not is_allowed_file(file.filename):
            return jsonify({
                'error': 'File type not allowed. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS)
            }), 400

        # Get output format
        output_format = request.form.get('format', 'gif')  # 'gif' or 'video'
        if output_format not in ['gif', 'video']:
            output_format = 'gif'

        # Create unique job ID
        job_id = str(uuid.uuid4())
        job_folder = os.path.join(OUTPUT_FOLDER, job_id)
        os.makedirs(job_folder, exist_ok=True)

        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, f'{job_id}_{filename}')
        file.save(upload_path)

        # Process file
        if is_video_file(filename):
            # Extract frames from video
            frames = extract_video_frames(upload_path)
        else:
            # Load image
            frames = upload_path

        # Create animated frames
        animated_frames = create_animated_memo_frames(frames, job_folder)

        # Create output file
        if output_format == 'gif':
            output_filename = f'animated_{job_id}.gif'
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            create_gif_from_frames(animated_frames, output_path)
        else:
            output_filename = f'animated_{job_id}.mp4'
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            create_video_from_frames(animated_frames, output_path)

        # Clean up temporary frames
        for frame_path in animated_frames:
            try:
                os.remove(frame_path)
            except:
                pass

        # Clean up uploaded file
        try:
            os.remove(upload_path)
        except:
            pass

        return jsonify({
            'success': True,
            'job_id': job_id,
            'filename': output_filename,
            'download_url': f'/api/download/{output_filename}',
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated file"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, secure_filename(filename))

        # Security check
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Check if file is in output folder (prevent directory traversal)
        if not os.path.abspath(file_path).startswith(os.path.abspath(OUTPUT_FOLDER)):
            return jsonify({'error': 'Invalid file path'}), 403

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<job_id>', methods=['GET'])
def check_status(job_id):
    """Check processing status"""
    try:
        job_folder = os.path.join(OUTPUT_FOLDER, job_id)

        if not os.path.exists(job_folder):
            return jsonify({'status': 'not_found'}), 404

        # Check if output files exist
        gif_file = os.path.join(OUTPUT_FOLDER, f'animated_{job_id}.gif')
        mp4_file = os.path.join(OUTPUT_FOLDER, f'animated_{job_id}.mp4')

        if os.path.exists(gif_file):
            return jsonify({
                'status': 'completed',
                'format': 'gif',
                'download_url': f'/api/download/animated_{job_id}.gif'
            }), 200
        elif os.path.exists(mp4_file):
            return jsonify({
                'status': 'completed',
                'format': 'video',
                'download_url': f'/api/download/animated_{job_id}.mp4'
            }), 200
        else:
            return jsonify({'status': 'processing'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve index page"""
    return jsonify({'message': 'UgokuMemoTransformer API Server', 'version': '1.0.0'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
