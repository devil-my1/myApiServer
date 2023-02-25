from fastapi import FastAPI, Response, status,Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}/description")
async def read_item_description(item_id: int):
    item_description = "This is a sample item."
    headers = {"X-Custom-Header": "some-value"}
    return JSONResponse(content={"description": item_description}, status_code=status.HTTP_200_OK, headers=headers)


@app.post("/items/")
async def create_item(request: Request):
    data = await request.json()
    # Do some processing with the received data
    item_id = 123  # This could be a generated ID or any other value
    item = {"id": item_id, "name": data["name"], "description": data["description"]}
    return JSONResponse(content=item)