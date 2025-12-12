from fastapi import APIRouter, HTTPException
from app.services.mongo_manager import db
from app.utils.hashing import verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login")
async def login(email: str, password: str):
    admin = await db["admins"].find_one({"email": email})
    if not admin:
        raise HTTPException(400, "Invalid credentials")
    if not verify_password(password, admin["password"]):
        raise HTTPException(400, "Invalid credentials")
    token = create_access_token({"sub": str(admin["_id"]), "email": admin["email"], "role": admin.get("role")})
    return {"access_token": token, "token_type":"bearer"}
