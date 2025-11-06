from pyrogram import Client, filters
from bot.config import API_ID, API_HASH, BOT_TOKEN, BIN_CHANNEL, MONGO_URI, DB_NAME, COLLECTION_NAME, DOMAIN
from pymongo import MongoClient
import uuid

# MongoDB setup
mongo = MongoClient(MONGO_URI)
db = mongo[DB_NAME]
collection = db[COLLECTION_NAME]

bot = Client("direct_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def handle_upload(client, message):
    # Forward file to BIN_CHANNEL
    fwd = await message.forward(BIN_CHANNEL)
    
    # Generate unique token
    token = str(uuid.uuid4())
    
    # Determine file_id and file_name
    if message.document:
        file_id = fwd.document.file_id
        file_name = fwd.document.file_name
        mime_type = fwd.document.mime_type
    elif message.video:
        file_id = fwd.video.file_id
        file_name = fwd.video.file_name
        mime_type = fwd.video.mime_type
    elif message.audio:
        file_id = fwd.audio.file_id
        file_name = fwd.audio.file_name
        mime_type = fwd.audio.mime_type
    elif message.photo:
        file_id = fwd.photo.file_id
        file_name = "photo.jpg"
        mime_type = "image/jpeg"
    
    # Save metadata to MongoDB
    collection.insert_one({
        "token": token,
        "file_id": file_id,
        "file_name": file_name,
        "mime_type": mime_type
    })
    
    # Reply with direct link
    link = f"https://{DOMAIN}/file/{token}"
    await message.reply(f"✅ Your permanent link: {link}")

bot.run()
