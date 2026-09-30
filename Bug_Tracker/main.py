from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import models, schemas, utils, auth
from database import SessionLocal

app = FastAPI()

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ RATE LIMITING SETUP
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Try again later."}
    )

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bug Tracker API"}

# ✅ Register endpoint with validation
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = utils.hash_password(user.password)
    
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = models.User(username=user.username, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ Login endpoint with RATE LIMITING
@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token(
        {"sub": db_user.username},
        expires_delta=timedelta(minutes=15)
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 900
    }

# ✅ Get current user with error handling
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth.verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    
    user = db.query(models.User).filter(models.User.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# ✅ Create bug with RATE LIMITING
@app.post("/bugs")
@limiter.limit("10/minute")
def add_bug(
    request: Request,
    bug: schemas.BugCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_bug = models.Bug(
        title=bug.title,
        description=bug.description,
        category=bug.category,
        user_id=current_user.id
    )
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return {"message": "Bug inserted successfully", "id": new_bug.id}

# ✅ Get all bugs with pagination and user filter
@app.get("/bugs")
@limiter.limit("30/minute")
def get_all_bugs(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if limit > 100:
        limit = 100
    
    bugs = db.query(models.Bug).filter(
        models.Bug.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return {"bugs": bugs, "count": len(bugs)}

# ✅ Get bugs by category with pagination and user filter
@app.get("/bugs/{category}")
@limiter.limit("30/minute")
def get_bugs_by_category(
    request: Request,
    category: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if limit > 100:
        limit = 100
    
    bugs = db.query(models.Bug).filter(
        models.Bug.user_id == current_user.id,
        models.Bug.category == category
    ).offset(skip).limit(limit).all()
    
    return {"bugs": bugs, "count": len(bugs)}