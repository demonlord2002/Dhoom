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
    # Fetch file details from MongoDB
    file_data = collection.find_one({"token": token})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    # ✅ Get Telegram file message ID (from forwarded message)
    # Stored file_id is not the numeric Telegram message ID, so we’ll store message_id instead in the bot.
    file_id = file_data.get("file_id")
    message_id = file_data.get("message_id")

    # Ensure valid message ID
    if not message_id:
        raise HTTPException(status_code=400, detail="Invalid or missing message ID.")

    # ✅ Build working Telegram redirect link
    # /c/ + channel_id (without -100) + / + message_id
    tg_link = f"https://t.me/c/{str(BIN_CHANNEL)[4:]}/{message_id}"
    return RedirectResponse(url=tg_link)
