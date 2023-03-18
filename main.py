from fastapi import FastAPI, Response, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from random import randint
from Controler import inst_api_manager as iap
import os
import openai


app = FastAPI()

MY_API_KEY = "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"
BASE_URL = "http://185.51.246.205:8000/"


openai.api_key = MY_API_KEY
openai.Model.list()
inst_user: iap.User = None


@app.get("/")
async def root():
    return RedirectResponse(BASE_URL + "docs")


@app.get("/items/{item_id}/description")
async def read_item_description(item_id: int):
    item_description = "This is a sample item."
    headers = {"X-Custom-Header": "some-value"}
    return JSONResponse(
        content={"description": item_description},
        status_code=status.HTTP_200_OK,
        headers=headers,
    )


@app.post("/items/")
async def create_item(request: Request):
    data = await request.json()
    # Do some processing with the received data
    item_id = 123  # This could be a generated ID or any other value
    item = {"id": item_id, "name": data["name"], "description": data["description"]}
    return JSONResponse(content=item)


@app.get("/inst/get_user/{user_name}")
async def get_inst_user_info(user_name: str):
    global inst_user
    inst_user = iap.User(user_name)
    return inst_user.user_info()


@app.get("/inst/get_user_stories")
def get_user_stories():
    if inst_user:
        return inst_user.user_stories()
    else:
        return {"Info": "First check user info to get user stories!"}
