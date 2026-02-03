# UgokuMemoTransformer (うごくメモ帳 変換ツール)

Transform images and videos into animated memo-style animations.

## Project Structure

```
├── backend/          # Python/Flask API server
├── frontend/         # React application
├── public/          # Static files
└── README.md        # This file
```

## Features

- Upload images or videos
- Convert to animated memo-style display
- Smooth animation transitions
- Export as video or GIF

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- FFmpeg (for video processing)

### Installation

1. Install backend dependencies:
```bash
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
npm install
cd frontend && npm install
```

### Running the Application

1. Start the backend:
```bash
python backend/app.py
```

2. In another terminal, start the frontend:
```bash
npm run frontend
```

3. Open your browser and navigate to `http://localhost:3000`

## Development

- Backend API runs on `http://localhost:5000`
- Frontend runs on `http://localhost:3000`

## License

MIT
