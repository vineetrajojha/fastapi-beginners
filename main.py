#This is the main FastAPI application where you define the API routes.

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/")
def read_items(db: Session = Depends(database.get_db)):
    items = db.query(models.Item).all()
    return items

@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(database.get_db)):
    item = models.Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
