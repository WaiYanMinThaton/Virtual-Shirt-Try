from fastapi import FastAPI, UploadFile, File ,Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import subprocess
import sqlite3


# Connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("database.db")

# Create a cursor object
cursor = conn.cursor()

app = FastAPI()
app.mount("/static", StaticFiles(directory="Resource"), name="static")

@app.get("/")
async def home():
    return FileResponse("templates/home.html")

@app.get('/api/simple-shirt')
async def simple_shirt():
    
    cursor.execute("""
    SELECT * FROM shirts
    WHERE id IN (
        SELECT MIN(id) FROM shirts GROUP BY brand
    )
    """)

    data = cursor.fetchall()
    shirts = []

    for shirt in data:
        shirt = transform_shirt(shirt)
        shirts.append(shirt)

    return JSONResponse(content={"data": shirts})


@app.post("/api/try")
async def try_upload(request: Request):
    request = await request.json()

    subprocess.Popen(["python", "main.py", request.get("shirt_type")])
    return JSONResponse(content={"shirt_type": request.get("shirt_type")})




def transform_shirt(shirt):
    keys = ["id", "path", "brand", "color", "size", "price", "stock", "suggestion"]
    dic = dict({})
    for i in range(len(keys)):
        dic[keys[i]] = shirt[i]

    return dic