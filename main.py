from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database.database import SessionLocal, engine
from model.models import User
from schema.schemas import UserCreate, UserUpdate
from typing import List
from services.service import create_database

app = FastAPI()
create_database()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": exc.errors()},
    )

@app.on_event("startup")
def startup():
    engine.connect()

@app.on_event("shutdown")
def shutdown():
    engine.dispose()

# @app.get("/users")
# def list_user():
#     return {"Hello","world"}    

@app.get("/users")
def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    return users


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(title=user.title, content=user.content, amount=user.amount, check=user.check)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}
