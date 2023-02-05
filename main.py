from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

import uvicorn

import crud
# import models
import schemas
from database import SessionLocal, engine, Base

# This is used to create initial table without Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# class User(BaseModel):
#   id: int
#   username: str

# all_users = [{"id":1, "username":"anique"}, {"id":2, "username":"jim"}]

# def find_user(id):
#   for u in all_users:
#     if u['id'] == id:
#       return u

@app.get("/")
async def main():
  return {"hello": "aaq"}

# @app.get("/users")
# async def get_users():
#   return {"data": all_users}

# @app.post("/users", status_code = status.HTTP_201_CREATED)
# async def create_user(user:User):
#   all_users.append(user.dict())
#   return {"data": user}

# @app.get("/users/{id}")
# def get_user(id: int):
#   user = find_user(id)
#   if not user:
#     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with ID: {id} was not found.")
#   return {"data": user}

# @app.delete("/users/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_user(id: int):
#   all_users.pop(0)
#   return {Response(status_code = status.HTTP_204_NO_CONTENT)}

# @app.put("/users/{id}", status_code = status.HTTP_200_OK)
# def update_user(id: int, user: User):
#   all_users[id-1] = user.dict()
#   return {"data": f"updated {all_users[id-1]}" }

if __name__ == '__main__':
  uvicorn.run("main:app", port = 8000, host = "127.0.0.1", reload=True)