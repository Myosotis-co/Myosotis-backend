from fastapi import FastAPI

app = FastAPI(title="FastAPI, Docker")


@app.get("/app")
def read_root():
    return {"hello": "world"}