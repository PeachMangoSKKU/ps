from fastapi import FastAPI
from fastapi import Query, Path
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from typing import Annotated

import os
import aiofiles

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...)
):
    if not os.path.exists("uploaded_files"):
        os.mkdir("uploaded_files")
    file_location = f"uploaded_files/{file.filename}"
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/downloadfile/{file_name}")
async def download_file(
    file_name: str,
    q: Annotated[
        str,
        Query(
            alias="q",
            title="q",
            description="q",
            min_length=1,
            max_length=50,
            pattern="^[\w\-. ]+$",
        ),
    ] = ...
):
    if not os.path.exists("uploaded_files"):
        os.mkdir("uploaded_files")
    file_path = f"uploaded_files/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name)
    return {"error": "File not found."}

@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
