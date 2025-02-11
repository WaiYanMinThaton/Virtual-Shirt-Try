from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse


app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("templates/home.html")

@app.post("/try")
async def try_upload():
    return "hi"