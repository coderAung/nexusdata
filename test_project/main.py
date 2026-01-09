import uvicorn
from fastapi import FastAPI

from test_project.apis import post_api, sign_in_api
from test_project.configs.database import init_db

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello Nexus Test Project"}

app.add_event_handler("startup", init_db)

app.include_router(post_api.router)
app.include_router(sign_in_api.router)


if __name__ == "__main__":
    uvicorn.run(app)