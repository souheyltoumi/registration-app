from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str
    error: str = "Internal Server Error"
    status_code: Optional[int] = 500

class ExceptionMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            error_status_code = getattr(e, "status_code", 500)
            error_response = ErrorResponse(detail=str(e), status_code=error_status_code)
            response =  JSONResponse(status_code=error_response.status_code, content=error_response.dict())
            await response(scope, receive, send)