from fastapi import FastAPI
from managers import pusher

from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Pusher v1.3"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class PushForm(BaseModel):
    token: str
    title: str
    message: str
    pass


@app.post("/api/v1/pusher/push")
async def push(pushForm: PushForm):
    print("[ push to android device ]", pushForm)
    pusher.send(
        pushForm.token,
        pushForm.title,
        pushForm.message,
    )
    return {"status": "done"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9030)
