from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, BIN_CHANNEL

app = FastAPI()

# MongoDB setup
mongo = MongoClient(MONGO_URI)
db = mongo[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/")
async def home():
    return {"status": "online", "message": "File to Link bot API is working!"}

@app.get("/file/{token}")
async def get_file(token: str):
    file_data = collection.find_one({"token": token})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    # Telegram file redirect
    tg_link = f"https://t.me/c/{str(BIN_CHANNEL)[4:]}/{file_data['file_id']}"
    return RedirectResponse(url=tg_link)
    
