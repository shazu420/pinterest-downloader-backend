from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess, uuid, os

app = FastAPI()
TMP = "/tmp"

# ✅ Request body schema
class FetchRequest(BaseModel):
    url: str

@app.post("/fetch")
async def fetch(data: FetchRequest):
    url = data.url

    if "pinterest" not in url and "pin.it" not in url:
        return {"error": "Invalid Pinterest URL"}

    filename = f"{uuid.uuid4()}.mp4"
    path = os.path.join(TMP, filename)

    try:
        subprocess.run(
            [
                "yt-dlp",
                "-f", "bv*+ba/best",
                "--merge-output-format", "mp4",
                "--user-agent", "Mozilla/5.0",
                "-o", path,
                url
            ],
            timeout=60,
            check=True
        )
    except Exception as e:
        return {"error": str(e)}

    return {"file": filename}

@app.get("/download/{file}")
def download(file: str):
    path = os.path.join(TMP, file)
    if not os.path.exists(path):
        return {"error": "Expired"}
    return FileResponse(path, filename="pinterest.mp4")
