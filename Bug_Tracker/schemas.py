from pydantic import BaseModel, Field, validator

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    
    @validator('password')
    def validate_password(cls, v):
        """Enforce password complexity."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserOut(BaseModel):
    id: int
    username: str
    
    class Config:
        orm_mode = True

class BugCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=5000)
    category: str = Field(..., min_length=1, max_length=50)

class BugOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    user_id: int
    
    class Config:
        orm_mode = True