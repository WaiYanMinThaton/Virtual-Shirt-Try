from fastapi import FastAPI, UploadFile, File ,Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import subprocess


app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("templates/home.html")


@app.post("/api/try")
async def try_upload(request: Request):
    request = await request.json()

    subprocess.Popen(["python", "main.py", request.get("shirt_type")])
    return JSONResponse(content={"shirt_type": request.get("shirt_type")})