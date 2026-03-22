import subprocess
import tempfile
import os
import logging
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)

        # Log what pandoc version we're running
        version = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        logger.info(f"Pandoc version: {version.stdout.splitlines()[0]}")

        result = subprocess.run(
            ["pandoc", input_path, "-o", output_path],
            capture_output=True,
            text=True
        )

        logger.info(f"Pandoc stdout: {result.stdout}")
        logger.info(f"Pandoc stderr: {result.stderr}")
        logger.info(f"Pandoc returncode: {result.returncode}")

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Pandoc error: {result.stderr}")

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail=f"Pandoc produced no output. stderr: {result.stderr}")

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="converted.docx"
        )