from fastapi import FastAPI
from routers import all_routers
from database import engine, Base
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start as start_scheduler
from contextlib import asynccontextmanager

from fastapi.security import HTTPBearer

# Create tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    start_scheduler()
    
    yield  # Let the app run

    # SHUTDOWN (if needed)
    # Stop scheduler here if needed

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "https://activity-tracker-frontend-two.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # allow all headers
)

bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Todo api routes",
        version="1.0.0",
        description="API using HTTPBearer Token",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"msg": "Todo API running"}
for r in all_routers:
    app.include_router(r)
