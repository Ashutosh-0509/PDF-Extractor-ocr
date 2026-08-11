import streamlit as st
import subprocess
import os
import shutil

st.set_page_config(page_title="PDF to Markdown Extractor", page_icon="📄")
st.title("📄 PDF → Markdown Extractor")
st.caption("Text + Equations (Nougat) + Figures/Diagrams (PyMuPDF) — sab ek saath")

uploaded_file = st.file_uploader("Apna PDF upload karo", type="pdf")

if uploaded_file:
    st.info(f"File: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

    if st.button("🚀 Process PDF", type="primary"):
        temp_pdf_path = "temp_upload.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        base_name = "temp_upload"
        output_root = f"pipeline_output_{base_name}"

        # Purana output agar hai toh clean karo
        if os.path.exists(output_root):
            shutil.rmtree(output_root)

        progress_placeholder = st.empty()
        log_placeholder = st.empty()

        with st.spinner("Processing ho raha hai... CPU pe 15-30+ minutes lag sakte hain, patience rakho."):
            process = subprocess.Popen(
                ["python", "master_pipeline.py", temp_pdf_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            log_lines = []
            for line in process.stdout:
                log_lines.append(line.strip())
                log_placeholder.text("\n".join(log_lines[-15:]))  # last 15 lines dikhao

            process.wait()

        final_md_path = os.path.join(output_root, "FINAL_OUTPUT.md")

        if process.returncode == 0 and os.path.exists(final_md_path):
            st.success("✅ Processing complete!")

            with open(final_md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            st.download_button(
                label="⬇️ Download FINAL_OUTPUT.md",
                data=md_content,
                file_name=f"{uploaded_file.name.replace('.pdf', '')}_output.md",
                mime="text/markdown"
            )

            with st.expander("📖 Preview (text only, images alag download honge)"):
                st.markdown(md_content)

            # Images folder ko bhi zip karke download option do
            images_dir = os.path.join(output_root, "images")
            if os.path.exists(images_dir) and os.listdir(images_dir):
                zip_path = f"{output_root}_full"
                shutil.make_archive(zip_path, "zip", output_root)
                with open(f"{zip_path}.zip", "rb") as f:
                    st.download_button(
                        label="⬇️ Download Full Package (.md + images as .zip)",
                        data=f,
                        file_name=f"{uploaded_file.name.replace('.pdf', '')}_full.zip",
                        mime="application/zip"
                    )
        else:
            st.error("❌ Processing fail hua. Neeche logs check karo.")
            st.code("\n".join(log_lines))