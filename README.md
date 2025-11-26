# BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
## Chủ đề: Chữ ký số trong file PDF
## Giảng viên: Đỗ Duy Cốp
## Nông Hồ Nhật _K225480106094
### I. MÔ TẢ CHUNG

#### Sinh viên thực hiện báo cáo và thực hành: phân tích và hiện thực việc nhúng, xác thực chữ ký số trong file PDF.

#### Phải nêu rõ chuẩn tham chiếu (PDF 1.7 / PDF 2.0, PAdES/ETSI) và sử dụng công cụ thực thi (ví dụ iText7, OpenSSL, PyPDF, pdf-lib). II. CÁC YÊU CẦU CỤ THỂ

### 1) Cấu trúc PDF liên quan chữ ký (Nghiên cứu)
- Mô tả ngắn gọn: Catalog, Pages tree, Page object, Resources, Content streams, XObject, AcroForm, Signature field (widget), Signature dictionary (/Sig), /ByteRange, /Contents, incremental updates, và DSS (theo PAdES).

- Liệt kê object refs quan trọng và giải thích vai trò của từng object trong lưu/truy xuất chữ ký.

- Đầu ra: 1 trang tóm tắt + sơ đồ object (ví dụ: Catalog → Pages → Page → /Contents ; Catalog → /AcroForm → SigField → SigDict).

### 2) Thời gian ký được lưu ở đâu?
- Nêu tất cả vị trí có thể lưu thông tin thời gian:
- /M trong Signature dictionary (dạng text, không có giá trị pháp lý).
- Timestamp token (RFC 3161) trong PKCS#7 (attribute timeStampToken).
- Document timestamp object (PAdES).
- DSS (Document Security Store) nếu có lưu timestamp và dữ liệu xác minh.
- Giải thích khác biệt giữa thông tin thời gian /M và timestamp RFC3161.
### 3) Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)
- Viết script/code thực hiện tuần tự:
- Chuẩn bị file PDF gốc.
- Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes).
- Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).
- Tính hash (SHA-256/512) trên vùng ByteRange.
- Tạo PKCS#7/CMS detached hoặc CAdES:
+  Include messageDigest, signingTime, contentType.
+ Include certificate chain.
+ (Tùy chọn) thêm RFC3161 timestamp token.
_ Chèn blob DER PKCS#7 vào /Contents (hex/binary) đúng offset.
_ Ghi incremental update.
_ (LTV) Cập nhật DSS với Certs, OCSPs, CRLs, VRI.
- Phải nêu rõ: hash alg, RSA padding, key size, vị trí lưu trong PKCS#7.
- Đầu ra: mã nguồn, file PDF gốc, file PDF đã ký.4) Các bước xác thực chữ ký trên PDF đã ký
### 4) Các bước xác thực chữ ký trên PDF đã ký
#### Các bước kiểm tra:
- Đọc Signature dictionary: /Contents, /ByteRange.
- Tách PKCS#7, kiểm tra định dạng.
- Tính hash và so sánh messageDigest.
- Verify signature bằng public key trong cert.
- Kiểm tra chain → root trusted CA.
- Kiểm tra OCSP/CRL.
- Kiểm tra timestamp token.
- Kiểm tra incremental update (phát hiện sửa đổi).
- Nộp kèm script verify + log kiểm thử. III. QUY TRÌNH THỰC HIỆN
- Sinh khóa RSA và chứng thư số
  
## 2.1  Cấu trúc PDF liên quan chữ ký (Nghiên cứu)
•	Mô tả ngắn gọn: Catalog, Pages tree, Page object, Resources, Content streams, XObject, AcroForm, Signature field (widget), Signature dictionary (/Sig), /ByteRange, /Contents, incremental updates, và DSS (theo PAdES).

•	Liệt kê object refs quan trọng và giải thích vai trò của từng object trong lưu/truy xuất chữ ký.

•	Đầu ra: 1 trang tóm tắt + sơ đồ object (ví dụ: Catalog → Pages → Page → /Contents ; Catalog → /AcroForm → SigField → SigDict).

 <img width="940" height="647" alt="image" src="https://github.com/user-attachments/assets/24a3de5e-c153-468c-ae1e-ee68b9d19870" />

## 2.2 Thời gian ký được lưu ở đâu?
	Trong tài liệu PDF, thông tin thời gian ký có thể được lưu ở nhiều vị trí khác nhau: 
1.	Trường /M trong Signature Dictionary:

-	Lưu thời gian ký dưới dạng chuỗi văn bản (text string).
  
-	Không có giá trị pháp lý vì không được xác thực bởi bên thứ ba.
  
2.	Timestamp Token (RFC 3161) trong PKCS#7:
   
-	Là một thuộc tính (attribute) của cấu trúc chữ ký CMS (timeStampToken).
  
-	Được cung cấp bởi Time Stamping Authority (TSA), có giá trị pháp lý.
  
3.	Document Timestamp Object (PAdES):
   
-	Là một dạng chữ ký đặc biệt áp dụng cho toàn bộ tài liệu (không gắn người ký).
  
-	Được dùng để đóng dấu thời gian cho tài liệu điện tử.
  
4.	DSS (Document Security Store):
   
-	Có thể chứa thông tin timestamp, OCSP, CRL và dữ liệu xác minh khác.
  
	Khác biệt giữa /M và timestamp RFC3161: 

-	/M chỉ là thông tin thời gian do phần mềm ký chèn vào, không được bảo vệ bởi cơ chế xác thực.
  
-	Timestamp RFC3161 được tạo bởi bên thứ ba (TSA) và được ký số, đảm bảo giá trị pháp lý và xác thực thời gian.
  
# 2.3 Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)

Viết script/code thực hiện tuần tự:

	Chuẩn bị file PDF gốc : btvn2_baomat.pdf

	Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes). 

• Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).
Tính hash (SHA-256/512) trên vùng ByteRange.

 • Tạo PKCS#7/CMS detached hoặc CAdES:
 
 • Include messageDigest, signingTime, contentType. 
 
• Include certificate chain

. • (Tùy chọn) thêm RFC3161 timestamp token. _ Chèn blob DER PKCS#7 vào /Contents (hex/binary) đúng offset. _ Ghi incremental update. _ (LTV) Cập nhật DSS với Certs, OCSPs, CRLs, VRI. 

• Phải nêu rõ: hash alg, RSA padding, key size, vị trí lưu trong PKCS#7
Đầu ra: mã nguồn, file PDF gốc, file PDF đã ký.4) Các bước xác thực chữ ký trên PDF đã ký

# 2.4 Các bước xác thực chữ ký trên PDF đã ký
Các bước kiểm tra:

•	Đọc Signature dictionary: /Contents, /ByteRange.

•	Tách PKCS#7, kiểm tra định dạng.

•	Tính hash và so sánh messageDigest.

•	Verify signature bằng public key trong cert.

•	Kiểm tra chain → root trusted CA.

•	Kiểm tra OCSP/CRL.

•	Kiểm tra timestamp token.

•	Kiểm tra incremental update (phát hiện sửa đổi).

•	Nộp kèm script verify + log kiểm thử

•	Sinh khóa RSA và chứng thư số

 <img width="713" height="1009" alt="image" src="https://github.com/user-attachments/assets/e502a0ca-d9db-41e3-b698-8b854b8bcf5c" />

2.5. Rủi ro chính và biện pháp giảm thiểu.

<img width="575" height="706" alt="image" src="https://github.com/user-attachments/assets/66441f9c-d6b6-4634-bc48-065f0b22e535" />

<img width="938" height="494" alt="image" src="https://github.com/user-attachments/assets/af86b2b6-fc96-409b-ae6d-d59d4a135992" />

2.6. Khuyến nghị kỹ thuật 
- Dùng SHA-256 hoặc mạnh hơn cho message digest.
- Dùng RSA 2048+ hoặc RSA-PSS(khuyến nghị) cho chữ ký và server TSA đáng tin cậy cho timestamp RFC -3161.
- Thực hiện LTV (PAdES-LTV) bằng cách nhúng chứng thư, OCSP/CRL và timestamp token và DSS.
- Kiểm tra modification level và đảm bảo trình verify báo rõ ràng khi có incremental updates.


2.7. Minh họa File đính kèm 
Trong bài nộp kèm các file mẫu 
- btvn2_baomat.pdf -file gốc.
-btvn2_baomat_ signed.pdf- file sau khi đã ký ( chứa/Contents PKCS#7 và ByteRange hợp lệ).

 <img width="939" height="528" alt="image" src="https://github.com/user-attachments/assets/0f459f22-309d-4388-83cc-807619ce1a59" />

 <img width="754" height="860" alt="image" src="https://github.com/user-attachments/assets/6b820d6f-b299-4fad-a788-32077580a5fd" />

2.8.Kết luận

      Bài tập này giúp hiểu rõ cơ chế lưu và xác minh chữ ký trong PDF thông qua các thành phần /ByteRange ,/Contents và incremental update. Trường /M chỉ lưu thời gian hiện thị không, không 
      
      có giá trị pháp lý, trong khi timestamp RFC-3161 trong PKCS#7 mới chứng minh được thời điểm ký thực tế. Để đảm bảo tính pháp lý và xác minh lâu dài (LTV), cần kết hợp PKCS#7 + timestamp 
      
      từ TSA và nhúng dữ liệu OCSP/CRL vào DSS theo chuẩn PAdES.

