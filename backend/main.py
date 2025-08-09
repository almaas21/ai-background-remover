from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uuid
from rembg import remove
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Save the uploaded file
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.png")
    output_path = os.path.join(RESULT_FOLDER, f"{file_id}.png")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Remove background
    with open(input_path, "rb") as inp:
        result = remove(inp.read())
        with open(output_path, "wb") as out:
            out.write(result)

    return FileResponse(output_path, media_type="image/png")
