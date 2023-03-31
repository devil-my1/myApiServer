from fastapi import FastAPI, Response, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from Controler import inst_api_manager as iam
from common.logger import logger

BASE_URL = "http://185.51.246.205:8000/"
app = FastAPI()


inst_user: iam.User = None


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
    inst_user = iam.User(user_name)
    return inst_user.user_info()


@app.get("/inst/get_user_stories")
def get_user_stories():
    if inst_user:
        return inst_user.user_stories()
    else:
        return {"Info": "First check user info to get user stories!"}


@app.get("/inst/download_story/")
async def download_story(url: str = "", story_id: str = ""):
    """Download instagram story api

    Args:
        url (str): Story's url
    """
    if url:
        id = url.split("/")[-2]
        story_id = id if id.isdigit() else story_id

    result = iam.User.download_story(url, story_id)
    logger.info("Downloaded stories result [%s]", result)
    status_code = status.HTTP_200_OK
    if "Error" in result.keys():
        status_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=result, status_code=status_code)
