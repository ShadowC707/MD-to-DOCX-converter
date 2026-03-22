import subprocess
import tempfile
import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This allows your GitHub Pages frontend to talk to this backend
# Without this, browsers block cross-origin requests (CORS policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this later once you know your GitHub Pages URL
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert(file: UploadFile):
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are accepted")

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.md")
        output_path = os.path.join(tmpdir, "output.docx")

        # Save uploaded file to disk
        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)

        # Run Pandoc
        result = subprocess.run(
            ["pandoc", input_path, "-o", output_path, "--mathml"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Pandoc error: {result.stderr}")

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="converted.docx"
        )