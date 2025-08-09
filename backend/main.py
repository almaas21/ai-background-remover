from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import rembg
import io

app = FastAPI()

# 1️⃣ Home page with file upload form
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>AI Background Remover</title></head>
        <body>
            <h2>Upload an image to remove background</h2>
            <form action="/remove-bg" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Remove Background">
            </form>
        </body>
    </html>
    """

# 2️⃣ API endpoint to remove background
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    output_image = rembg.remove(input_image)
    return FileResponse(io.BytesIO(output_image), media_type="image/png", filename="no-bg.png")
