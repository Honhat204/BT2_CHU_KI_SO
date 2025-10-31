# BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
## Chủ đề: Chữ ký số trong file PDF
## Giảng viên: Đỗ Duy Cốp
## Nông Hồ Nhật _K225480106094
### I. MÔ TẢ CHUNG

Sinh viên thực hiện báo cáo và thực hành: phân tích và hiện thực việc nhúng, xác thực chữ ký số trong file PDF.
Phải nêu rõ chuẩn tham chiếu (PDF 1.7 / PDF 2.0, PAdES/ETSI) và sử dụng công cụ thực thi (ví dụ iText7, OpenSSL, PyPDF, pdf-lib). II. CÁC YÊU CẦU CỤ THỂ
1) Cấu trúc PDF liên quan chữ ký (Nghiên cứu)
Mô tả ngắn gọn: Catalog, Pages tree, Page object, Resources, Content streams, XObject, AcroForm, Signature field (widget), Signature dictionary (/Sig), /ByteRange, /Contents, incremental updates, và DSS (theo PAdES).

Liệt kê object refs quan trọng và giải thích vai trò của từng object trong lưu/truy xuất chữ ký.

Đầu ra: 1 trang tóm tắt + sơ đồ object (ví dụ: Catalog → Pages → Page → /Contents ; Catalog → /AcroForm → SigField → SigDict).

2) Thời gian ký được lưu ở đâu?
Nêu tất cả vị trí có thể lưu thông tin thời gian:
/M trong Signature dictionary (dạng text, không có giá trị pháp lý).
Timestamp token (RFC 3161) trong PKCS#7 (attribute timeStampToken).
Document timestamp object (PAdES).
DSS (Document Security Store) nếu có lưu timestamp và dữ liệu xác minh.
Giải thích khác biệt giữa thông tin thời gian /M và timestamp RFC3161.
3) Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)
Viết script/code thực hiện tuần tự:
Chuẩn bị file PDF gốc.
Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes).
Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).
Tính hash (SHA-256/512) trên vùng ByteRange.
Tạo PKCS#7/CMS detached hoặc CAdES:
Include messageDigest, signingTime, contentType.
Include certificate chain.
(Tùy chọn) thêm RFC3161 timestamp token.
Chèn blob DER PKCS#7 vào /Contents (hex/binary) đúng offset.
Ghi incremental update.
(LTV) Cập nhật DSS với Certs, OCSPs, CRLs, VRI.
Phải nêu rõ: hash alg, RSA padding, key size, vị trí lưu trong PKCS#7.
Đầu ra: mã nguồn, file PDF gốc, file PDF đã ký.4) Các bước xác thực chữ ký trên PDF đã ký
4) Các bước xác thực chữ ký trên PDF đã ký
Các bước kiểm tra:
Đọc Signature dictionary: /Contents, /ByteRange.
Tách PKCS#7, kiểm tra định dạng.
Tính hash và so sánh messageDigest.
Verify signature bằng public key trong cert.
Kiểm tra chain → root trusted CA.
Kiểm tra OCSP/CRL.
Kiểm tra timestamp token.
Kiểm tra incremental update (phát hiện sửa đổi).
Nộp kèm script verify + log kiểm thử. III. QUY TRÌNH THỰC HIỆN
Sinh khóa RSA và chứng thư số
