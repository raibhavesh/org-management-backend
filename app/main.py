from fastapi import FastAPI
from app.routers import org_router, admin_router

app = FastAPI(title="Organization Management Service")
app.include_router(org_router.router)
app.include_router(admin_router.router)

@app.get("/")
def root():
    return {"message":"API running. Open /docs for Swagger UI"}
