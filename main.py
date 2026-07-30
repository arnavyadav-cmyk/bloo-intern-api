from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return{"message": "welcome to my app"}

@app.get("/hello")
def hello():
    return{"message": "hello World"}

@app.get("/health")
def health():
    return{"status": "healthy"}
