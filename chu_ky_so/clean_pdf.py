from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("btvn2_baomat.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open("btvn2_baomat_fixed.pdf", "wb") as f:
    writer.write(f)

print("✅ Đã tạo file btvn2_baomat_fixed.pdf (PDF sạch, không hybrid xref).")
