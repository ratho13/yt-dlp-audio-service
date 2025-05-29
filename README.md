# YouTube Audio Extractor Service

A FastAPI service that extracts audio information from YouTube videos using yt-dlp.

## Features

- Extract audio URLs from YouTube videos
- Get video metadata (title, duration, etc.)
- Health check endpoints
- Docker ready

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /extract-audio` - Extract audio from video URL
- `POST /get-video-info` - Get video information

## Usage

```bash
curl -X POST "http://localhost:8001/extract-audio" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
