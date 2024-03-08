# general framework imports
from pydantic import BaseModel, Field, EmailStr, validator

class UserAccountRegistrationRequest(BaseModel):
    email: EmailStr = Field(title="user email", example="souheil.toumi@test-domain.com")
    password: str = Field(title="user password", example="strongPassword123", hideen=True)

class UserAccountRegistrationResponse(BaseModel):
    message: str = Field(title="regustration response message", example="activation token sent to email 'souheil.toumi@test-domain.com'")
