import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(page_title="MD → DOCX", page_icon="📄")

st.title("MD → DOCX")
st.caption("Upload a Markdown file and get a Word document back. Formulas included.")

uploaded_file = st.file_uploader("Choose a .md file", type=["md"])

if uploaded_file is not None:
    if st.button("Convert", type="primary"):
        with st.spinner("Converting..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "input.md")
                output_path = os.path.join(tmpdir, "output.docx")

                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                result = subprocess.run(
                    ["pandoc", input_path, "-o", output_path, "--mathml"],
                    capture_output=True,
                    text=True
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
                        file_name=uploaded_file.name.replace(".md", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
