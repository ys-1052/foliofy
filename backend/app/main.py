from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, dashboard, holdings

app = FastAPI(title="Foliofy API", description="保有株管理ツール API", version="0.1.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(holdings.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Foliofy API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
