import os

API_ID = int(os.environ.get("API_ID", "YOUR_API_ID"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
BIN_CHANNEL = os.environ.get("BIN_CHANNEL", "-1003293810900") # new working channel

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "telegram_files"
COLLECTION_NAME = "files"

DOMAIN = os.environ.get("DOMAIN", "vignesh-v2.netlify.app")
