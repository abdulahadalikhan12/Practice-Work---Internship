from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Message" : "My first API is working"}