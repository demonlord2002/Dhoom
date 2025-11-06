from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pymongo import MongoClient
from pyrogram import Client
from web.config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, DB_NAME, COLLECTION_NAME

app = FastAPI()

# MongoDB
mongo = MongoClient(MONGO_URI)
db = mongo[DB_NAME]
collection = db[COLLECTION_NAME]

# Pyrogram Client
client = Client("direct_link_web", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.get("/file/{token}")
async def get_file(token: str):
    file_record = collection.find_one({"token": token})
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    file_id = file_record["file_id"]

    # Download file as stream
    async with client:
        stream = await client.download_media(file_id, in_memory=True)
        return StreamingResponse(
            stream,
            media_type=file_record.get("mime_type", "application/octet-stream"),
            headers={"Content-Disposition": f'attachment; filename="{file_record["file_name"]}"'}
        )
