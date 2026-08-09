from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel
import logging
import time
from pythonjsonlogger import jsonlogger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class User(BaseModel):
    name: str
    role: str

logger = logging.getLogger()

handler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s %(method)s %(path)s %(status_code)s %(duration_ms)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.setLevel(logging.INFO)


app = FastAPI()


@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    response = None
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code

    except Exception as e:
        logger.exception("request failed")
        raise
    finally:
        duration = (time.time() - start_time) * 1000

        logger.info(
            "HTTP request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": round(duration, 2)
            }
        )

    return response

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
    return {"message": "welcome to my app"}

@app.get("/hello")
def hello():
    return {"message": "hello from Docker v2"}

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
    logger.info(f"User created: {user.name}")
    return user