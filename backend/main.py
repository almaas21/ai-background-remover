from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
from io import BytesIO

# Initialize FastAPI app
app = FastAPI()

# Use lightweight model to save RAM
session = new_session("u2netp")

@app.get("/")
def home():
    return {"message": "AI Background Remover API running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Read file into memory
        contents = await file.read()

        # Open image
        image = Image.open(BytesIO(contents)).convert("RGB")

        # Resize large images to max 1024px (keeps aspect ratio)
        max_size = 1024
        image.thumbnail((max_size, max_size))

        # Remove background
        result = remove(image, session=session)

        # Save to BytesIO for response
        buf = BytesIO()
        result.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
