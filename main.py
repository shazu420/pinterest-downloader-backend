from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()
TMP = "/tmp"

@app.post("/fetch")
async def fetch(req: Request):
    data = await req.json()
    url = data.get("url", "")

    if "pinterest" not in url and "pin.it" not in url:
        return {"error": "Invalid URL"}

    filename = f"{uuid.uuid4()}.mp4"
    path = os.path.join(TMP, filename)

    try:
        subprocess.run(
            ["yt-dlp", "-f", "mp4", "-o", path, url],
            timeout=40
        )
    except:
        return {"error": "Download failed"}

    return {"file": filename}

@app.get("/download/{file}")
def download(file: str):
    path = os.path.join(TMP, file)
    if not os.path.exists(path):
        return {"error": "Expired"}
    return FileResponse(path, filename="pinterest.mp4")
