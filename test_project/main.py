import uvicorn
from fastapi import FastAPI

from test_project.apis import comment_api, post_api, sign_in_api, sign_up_api
from test_project.configs import handlers
from test_project.configs.database import init_db
from test_project.utils.exception import AppBusinessException

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello Nexus Test Project"}

app.add_event_handler("startup", init_db)

app.include_router(post_api.router)
app.include_router(sign_in_api.router)
app.include_router(sign_up_api.router)
app.include_router(comment_api.router)

app.add_exception_handler(AppBusinessException, handler=handlers.handle)


if __name__ == "__main__":
    uvicorn.run(app)