from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dao.conf.model_settings import get_settings
from routers.dispatcher import get_controller
from routers import user_router
from utils.profiler import CProfileMiddleware
from utils.exception_middleware import ExceptionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Depends
import uvicorn
app = FastAPI()

# order fields with tags in SwaggerUI
tags_metadata = [
    {"name": "User Account"}
]

app = FastAPI(
    title="UserAPI",
    description="UserAPI is an application that handles user account registration and activation",
    version="1.0.0",
    openapi_tags=tags_metadata
)

settings = get_settings()

## setup profiler if its development
if settings.env == "development":
    app.add_middleware(CProfileMiddleware)

# Add CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Add exception middleware
# app.add_middleware(ExceptionMiddleware)

# manage route for order field
app.include_router(user_router.router, dependencies=[Depends(get_controller)])

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=settings.app.port,
        reload=settings.app.reloading,
        workers=settings.app.nb_workers,
    )
