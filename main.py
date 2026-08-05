from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class User(BaseModel):
    name: str
    role: str

app = FastAPI()

inventory = {
    1: {
        "name": "arnav",
        "role": "intern"
    },
    2: {
        "name": "ashish",
        "role": "mentor"
    }
}

@app.get("/")
def home():
    logging.info("Home endpoint accessed")
    return {"message": "welcome to my app"}

@app.get("/hello")
def hello():
    return {"message": "hello World"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.get("/user/{user_id}")
def user(
    user_id: int = Path(
        ...,
        description="The ID of the user",
        ge=1
    )
):
    return inventory[user_id]

@app.get("/users")
def get_users(name: Optional[str] = None):
    for user_id in inventory:
        if inventory[user_id]["name"] == name:
            return inventory[user_id]
    return {"message": "user not found"}

@app.post("/users")
def create_user(user: User):
    user_id = max(inventory) + 1

    inventory[user_id] = {
        "name": user.name,
        "role": user.role
    }
    return user