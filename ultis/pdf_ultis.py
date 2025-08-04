import fitz  # PyMuPDF

def read_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Ví dụ:
pdf_path = r"C:\Users\minhs\OneDrive\Videos\SGK KHTN 8 KNTT.pdf"

