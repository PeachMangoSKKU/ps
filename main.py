from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

import os
import shutil

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not os.path.exists("uploaded_files"):
        os.mkdir("uploaded_files")
    file_location = f"uploaded_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/downloadfile/{file_name}")
async def download_file(file_name: str):
    # 파일 위치 지정
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
