import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/remove-background/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    const imageBlob = new Blob([new Uint8Array(res.data.image_bytes)], { type: "image/png" });
    setOutput(URL.createObjectURL(imageBlob));
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Background Remover</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Remove Background</button>
      {output && <img src={output} alt="result" style={{ marginTop: 20, maxWidth: "100%" }} />}
    </div>
  );
}

export default App;