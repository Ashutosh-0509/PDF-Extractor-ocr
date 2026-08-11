# 📄 PDF Extractor OCR (Nougat + PyMuPDF)

A powerful end-to-end PDF to Markdown extraction pipeline that combines **Nougat OCR** (for mathematical equations and structured text) and **PyMuPDF / Pillow** (for figure extraction and vector-graphics fallback).

It includes an interactive **Streamlit Web Application** UI for uploading PDFs, processing them, previewing the output, and downloading full Markdown + image packages.

---

## ✨ Features

- 🧮 **Math & Equation Extraction**: Uses Meta AI's Nougat model (`0.1.0-base`) to accurately translate math formulas into LaTeX Markdown formatting.
- 🖼️ **Smart Figure Extraction**: Extracts embedded raster figures and stitches multi-part diagram images on each page.
- 🎨 **Vector Graphics Fallback**: Detects pages with vector graphics/diagrams and automatically renders high-resolution page fallbacks.
- 🌐 **Interactive Streamlit Web UI**: Simple, user-friendly interface (`app.py`) for PDF uploading and real-time log monitoring.
- 📦 **Downloadable Packages**: Export pure Markdown or full `.zip` packages containing Markdown and linked images.

---

## 🛠️ Project Structure

```text
PDF-Extractor-ocr/
├── app.py                 # Streamlit Web UI Application
├── master_pipeline.py     # Core OCR & extraction pipeline script
├── requirements.txt       # Project Python dependencies
├── .gitignore             # Ignored output folders and virtual environments
└── nougat-main/           # Nougat core engine & model source code
```

---

## 🚀 Quick Start

### 1. Environment Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/Ashutosh-0509/PDF-Extractor-ocr.git
cd PDF-Extractor-ocr

# Create and activate virtual environment
python -m venv nougat_env
# On Windows:
nougat_env\Scripts\activate
# On Linux/macOS:
source nougat_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e nougat-main
```

---

### 2. Running via Streamlit Web App

Start the web dashboard:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, upload any PDF, and click **Process PDF**.

---

### 3. Running via Command Line (CLI)

Run the master pipeline directly on any PDF file:

```bash
python master_pipeline.py "path/to/your/document.pdf"
```

The output will be saved under `pipeline_output_<filename>/` including `FINAL_OUTPUT.md` and all extracted images under `images/`.

---

## 📄 License

This project is licensed under the MIT License / Meta Nougat License. See individual directories for model weights licensing.
