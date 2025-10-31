from pyhanko.sign import signers
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.pdf_utils.writer import PdfFileWriter
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from pyhanko.sign.signers import PdfSignatureMetadata, SimpleSigner, PdfSignatureAppearance

PDF_IN = r'D:\chu_ky_so\btvn2_baomat.pdf'
PDF_OUT = r'D:\chu_ky_so\btvn2_baomat_signed_output.pdf'
KEY_FILE = r'D:\chu_ky_so\signer_key.pem'
CERT_FILE = r'D:\chu_ky_so\signer_cert.pem'

# Tạo signer từ PEM
signer = SimpleSigner.load(
    key=KEY_FILE,
    cert=CERT_FILE,
    passphrase=None  # nếu private key không có mật khẩu
)

# Đọc PDF gốc
with open(PDF_IN, 'rb') as f:
    pdf_reader = PdfFileReader(f)
    pdf_writer = PdfFileWriter()
    for page in pdf_reader.pages:
        pdf_writer.addpage(page)

# Tạo signature field (vị trí optional)
sig_field_spec = SigFieldSpec(sig_field_name='Signature1', on_page=0, box=(50, 50, 200, 100))
append_signature_field(pdf_writer, sig_field_spec)

# Metadata và appearance
sig_meta = PdfSignatureMetadata(field_name='Signature1', md_algorithm='sha256')
appearance = PdfSignatureAppearance()

# Ký PDF incremental update
with open(PDF_OUT, 'wb') as out_f:
    signers.sign_pdf(
        pdf_writer,
        signature_meta=sig_meta,
        signer=signer,
        appearance=appearance,
        output=out_f
    )

print(f"✅ PDF đã ký: {PDF_OUT}")
