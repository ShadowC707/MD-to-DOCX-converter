import streamlit as st
import subprocess
import tempfile
import os
import zipfile
import glob

st.set_page_config(page_title="MD → DOCX", page_icon="📄")

st.title("MD → DOCX")
st.caption("Upload a Markdown file and get a Word document back. Formulas and images included.")

st.info("""
**Two ways to upload:**
- **Single `.md` file** — no images
- **`.zip` file** — your `.md` + any images in the same folder
""")

uploaded_file = st.file_uploader("Choose a .md or .zip file", type=["md", "zip"])

if uploaded_file is not None:
    if st.button("Convert", type="primary"):
        with st.spinner("Converting..."):
            with tempfile.TemporaryDirectory() as tmpdir:

                if uploaded_file.name.endswith(".zip"):
                    # Extract zip and find the .md file inside
                    zip_path = os.path.join(tmpdir, "upload.zip")
                    with open(zip_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    with zipfile.ZipFile(zip_path, "r") as z:
                        z.extractall(tmpdir)

                    # Find the first .md file in the extracted contents
                    md_files = glob.glob(os.path.join(tmpdir, "**", "*.md"), recursive=True)

                    if not md_files:
                        st.error("No .md file found inside the zip.")
                        st.stop()

                    input_path = md_files[0]
                    output_name = os.path.basename(input_path).replace(".md", ".docx")

                else:
                    # Plain .md upload
                    input_path = os.path.join(tmpdir, uploaded_file.name)
                    with open(input_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    output_name = uploaded_file.name.replace(".md", ".docx")

                output_path = os.path.join(tmpdir, output_name)

                # Run Pandoc from the directory where the .md lives
                # so relative image paths like ![img](images/x.png) resolve correctly
                result = subprocess.run(
                    ["pandoc", input_path, "-o", output_path, "--mathml"],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(input_path)
                )

                if result.returncode != 0:
                    st.error(f"Pandoc error: {result.stderr}")
                elif not os.path.exists(output_path):
                    st.error("Conversion failed — no output file produced.")
                else:
                    with open(output_path, "rb") as f:
                        docx_bytes = f.read()

                    st.success("Done!")
                    st.download_button(
                        label="⬇ Download .docx",
                        data=docx_bytes,
                        file_name=output_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
