from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
load_dotenv()


from app.interfaces.api.routes import image, auth
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.session import engine

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hexagonal API",
        version="1.0.0",
        description="API with JWT auth and image upload",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

origins = [
    "http://localhost:5173",
    "https://like-it-pre-prod.coak.fr",
    "https://like-it.coak.fr",
    "http://like-it-api-pre-prod.coak.fr"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(image.router)
