from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse,FileResponse
import requests
import uvicorn
from urllib.parse import unquote
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_file_info(url: str) -> dict:
    # 获取请求头
    response = requests.head(url)
    
    # 检查响应是否成功
    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve file information from {url}")
    
    # 从响应头里面拿到文件信息和文件大小
    content_disposition = response.headers.get('Content-Disposition')
    content_length = response.headers.get('Content-Length')
    
    if not content_disposition:
        path_segments = url.split("/")
        filename_from_url = unquote(path_segments[-1]) if path_segments else None
        content_disposition = f'attachment; filename="{filename_from_url}"'
    
    size = None
    if content_length:
        try:
            size = int(content_length)
        except ValueError:
            pass
    
    return {
        "filename": content_disposition,
        "size": size
    }

@app.get("/")
def read_item():
    return FileResponse("templates/index.html")

# 中转流
@app.get("/download/")
def download_file(url: str):
    try:
        file_info = get_file_info(url)
    except HTTPException as e:
        return e
    
    response = requests.get(url, stream=True)
    
    def stream_content():
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk
            
    return StreamingResponse(stream_content(), 
                             media_type='application/octet-stream',
                             headers={"Content-Disposition": file_info['filename'],
                                      "Content-Length": str(file_info['size']) if file_info['size'] else None})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)