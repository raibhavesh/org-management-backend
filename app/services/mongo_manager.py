from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, MASTER_DB

client = AsyncIOMotorClient(MONGO_URI)
db = client[MASTER_DB]

async def create_org_collection(org_slug: str):
    collection_name = f"org_{org_slug}"
    # create collection if not exists by inserting then deleting a dummy doc (Mongo creates on first insert),
    # but Motor has create_collection:
    try:
        await db.create_collection(collection_name)
    except Exception:
        # already exists
        pass
    return collection_name

async def drop_org_collection(collection_name: str):
    try:
        await db.drop_collection(collection_name)
        return True
    except Exception:
        return False

async def copy_collection(old_name: str, new_name: str):
    cursor = db[old_name].find({})
    docs = []
    async for d in cursor:
        d.pop("_id", None)
        docs.append(d)
    if docs:
        await db[new_name].insert_many(docs)
    return True
