from fastapi import FastAPI

app = FastAPI(title="YouTube Audio Extractor", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "YouTube Audio Extractor Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)    video_id: str

@app.get("/")
async def root():
    return {"message": "YouTube Audio Extractor Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/extract-audio", response_model=VideoResponse)
async def extract_audio(request: VideoRequest):
    try:
        logger.info(f"Processing video: {request.url}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'extract_flat': False,
        }
        
        # Extract video info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.url, download=False)
                
                response = VideoResponse(
                    status="success",
                    title=info.get('title', 'Unknown'),
                    duration=info.get('duration', 0),
                    audio_url=info.get('url', ''),
                    video_id=info.get('id', '')
                )
                
                logger.info(f"Successfully processed: {response.title}")
                return response
                
            except Exception as e:
                logger.error(f"yt-dlp error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to process video: {str(e)}")
                
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/get-video-info")
async def get_video_info(request: VideoRequest):
    """Get video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            
            return {
                "title": info.get('title'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "upload_date": info.get('upload_date'),
                "view_count": info.get('view_count'),
                "video_id": info.get('id'),
                "thumbnail": info.get('thumbnail')
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get video info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
