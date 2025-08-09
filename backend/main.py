from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read file
    input_bytes = await file.read()

    # Open as image
    input_image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

    # Remove background
    output_image = remove(input_image)

    # Save result to BytesIO without resizing
    img_bytes = io.BytesIO()
    output_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")
