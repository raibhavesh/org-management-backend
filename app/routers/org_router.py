from fastapi import APIRouter, HTTPException, Body, Depends, Header
from app.models.master_models import OrgCreate, OrgOut
from app.services.mongo_manager import db, create_org_collection, drop_org_collection, copy_collection
from app.utils.hashing import hash_password, verify_password
from bson.objectid import ObjectId
from app.auth.jwt_handler import create_access_token, decode_token
import re

router = APIRouter(prefix="/org", tags=["org"])

def slugify(name: str):
    s = name.strip().lower()
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'[^a-z0-9_]', '', s)
    return s

@router.post("/create", response_model=OrgOut)
async def create_org(payload: OrgCreate):
    org_slug = slugify(payload.organization_name)
    existing = await db["organizations"].find_one({"organization_name": org_slug})
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")
    admin_doc = {"email": payload.email, "password": hash_password(payload.password), "role": "admin"}
    admin_res = await db["admins"].insert_one(admin_doc)
    collection_name = await create_org_collection(org_slug)
    org_doc = {"organization_name": org_slug, "collection_name": collection_name, "admin_id": str(admin_res.inserted_id)}
    await db["organizations"].insert_one(org_doc)
    return OrgOut(**org_doc)

@router.get("/get")
async def get_org(organization_name: str):
    org_slug = slugify(organization_name)
    org = await db["organizations"].find_one({"organization_name": org_slug})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    org["_id"] = str(org["_id"])
    return org

@router.put("/update")
async def update_org(old_name: str = Body(...), new_name: str = Body(...), authorization: str | None = Header(None)):
    # Simple auth check: require Bearer token of admin that belongs to this org (for demo)
    if not authorization:
        raise HTTPException(401, "Missing authorization")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    old_slug = slugify(old_name)
    new_slug = slugify(new_name)
    org = await db["organizations"].find_one({"organization_name": old_slug})
    if not org:
        raise HTTPException(404, "old org not found")
    # check admin
    if str(payload.get("sub")) != org.get("admin_id"):
        raise HTTPException(403, "Not allowed")
    new_collection = f"org_{new_slug}"
    await create_org_collection(new_slug)
    await copy_collection(org["collection_name"], new_collection)
    # update master
    await db["organizations"].update_one({"_id": org["_id"]}, {"$set": {"organization_name": new_slug, "collection_name": new_collection}})
    return {"status":"success","new_name": new_slug}

@router.delete("/delete")
async def delete_org(organization_name: str = Body(...), authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing authorization")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    org_slug = slugify(organization_name)
    org = await db["organizations"].find_one({"organization_name": org_slug})
    if not org:
        raise HTTPException(404, "Organization not found")
    if str(payload.get("sub")) != org.get("admin_id"):
        raise HTTPException(403, "Not allowed")
    await drop_org_collection(org["collection_name"])
    await db["organizations"].delete_one({"_id": org["_id"]})
    await db["admins"].delete_one({"_id": ObjectId(org["admin_id"])})
    return {"status":"deleted"}
