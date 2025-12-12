import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MASTER_DB = os.getenv("MASTER_DB", "master_db")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
