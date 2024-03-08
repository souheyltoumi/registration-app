# general framework imports
from pydantic import BaseModel, Field, EmailStr, validator

class UserAccountActivationRequest(BaseModel):
    email: EmailStr = Field(title="user email", example="souheil.toumi@test-domain.com")
    password: str = Field(title="user password", example="strongPassword123", hideen=True)
    token: str = Field(title="account activation token", example="XeDKN92XC")

class UserAccountActivationResponse(BaseModel):
    message: str = Field(title="activation response message", example="Account souheil.toumi@test-domain.com activated")
