import io
from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image

app = Flask(__name__)

# Optional: Limit upload size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        # Open image as a PIL Image without forcing resize
        input_image = Image.open(file.stream).convert("RGBA")

        # Remove background, keeping full resolution
        output = remove(input_image)

        # Save to a BytesIO stream
        output_bytes = io.BytesIO()
        output.save(output_bytes, format="PNG")
        output_bytes.seek(0)

        return send_file(
            output_bytes,
            mimetype="image/png",
            as_attachment=True,
            download_name="no-bg.png"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "AI Background Remover API — POST to /remove-bg"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
