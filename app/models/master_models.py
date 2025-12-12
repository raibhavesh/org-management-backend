from pydantic import BaseModel, EmailStr

class OrgCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrgOut(BaseModel):
    organization_name: str
    collection_name: str
    admin_id: str
