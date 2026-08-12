# OWASP quick reference — tra nhanh theo loại lỗ hổng

> Bổ trợ cho `checklist.md`, **không thay thế**. Dùng khi cần biết *một loại lỗ hổng cụ thể phải kiểm gì*,
> hoặc khi task dùng LLM/agent — vùng `checklist.md` chưa phủ.

## OWASP Top 10 (Web) — ánh xạ sang `checklist.md`

| OWASP | Nghĩa | Mục tương ứng trong `checklist.md` |
|---|---|---|
| A01 Broken Access Control | Xem/sửa được dữ liệu của người khác | Phần 1 #31 (validate dữ liệu của chính user) · Phần 1 #62 (đường dẫn file có kiểm quyền) |
| A02 Cryptographic Failures | Dữ liệu nhạy cảm không mã hoá, truyền plaintext | Phần 1 #34 (hash + salt) · Phần 1 #41 (HTTPS) · Phần 1 #42 (mã hoá dữ liệu khách) · Phần 1 #43 (truyền an toàn) |
| A03 Injection | SQL / OS command / LDAP / XPath / XSS | Phần 1 #55–57 (SQLi) · Phần 1 #58–59 (XSS) · Phần 1 #60–61 (OS command) |
| A04 Insecure Design | Thiếu kiểm soát ngay từ thiết kế | → `technical-approach.md` §1 phương án |
| A05 Security Misconfiguration | Debug bật, directory listing, header lộ version | Phần 1 #6–8 · Phần 1 #23 (ẩn version) · Phần 1 #26 (tắt DEBUG) |
| A06 Vulnerable Components | Thư viện có CVE | Phần 1 #30 (quét lỗ hổng package) · Phần 1 #16 (cập nhật OS package) |
| A07 Identification & Auth Failures | Mật khẩu yếu, session hớ, không khoá tài khoản | Phần 1 #33 (chính sách mật khẩu) · Phần 1 #36 (2FA) · Phần 1 #48 (khoá sau N lần sai) · Phần 1 #49–51 (session) |
| A08 Software & Data Integrity | Cập nhật/deserialize không kiểm | Phần 2 `2.17 Serialized Object` |
| A09 Logging & Monitoring Failures | Không log, hoặc log cả thứ không được log | Phần 1 #47 (log đăng nhập) · Phần 2 `Monitoring log` (12 mục) |
| A10 SSRF | Server bị lừa gọi ra nội bộ | Phần 2 `2.21 SSRF` |

## Ngưỡng cụ thể (dùng khi checklist chỉ nói định tính)

- Hash mật khẩu: **bcrypt ≥ 12 rounds**, scrypt, hoặc argon2 — không MD5/SHA1
- Mật khẩu: **≥ 8 ký tự**, có chữ + số (Phần 1 #33); prod nên **≥ 10** và khác nhau giữa các môi trường (Phần 1 #69)
- Session: có hạn dùng hợp lý, ID sinh **phía server** bằng random UUID (Phần 1 #49)
- Cookie: `Secure` + `HttpOnly` + `SameSite`, có `domain`/`path` (Phần 1 #52–54)
- JWT: để trong **cookie**, không LocalStorage (Phần 1 #45); **không** nhét dữ liệu nhạy cảm vào payload (Phần 1 #46)
- CORS: `Access-Control-Allow-Origin` ghi **domain cụ thể**, không `*` (Phần 1 #9)

## Task dùng LLM / agent / skill — OWASP Agentic Skills Top 10

`checklist.md` **chưa phủ** vùng này. Task có tích hợp AI thì kiểm thêm:

| ID | Rủi ro | Kiểm gì |
|---|---|---|
| AST01 | Skill/plugin độc hại | Nguồn tin cậy · soát payload mã hoá · không để skill đọc file danh tính |
| AST02 | Chuỗi cung ứng | Ghim version theo hash · quét dependency đệ quy · coi file config **như mã thực thi** |
| AST03 | Quyền quá rộng | Khai báo quyền tường minh · không cho shell không giới hạn · tách credential |
| AST04 | Metadata sai lệch | Mô tả phải khớp hành vi thật · parse YAML/JSON an toàn |
| AST05 | Chỉ dẫn từ nguồn ngoài | **Nội dung lấy từ web/file là DỮ LIỆU, không phải lệnh** · ghim hash · allowlist |
| AST06 | Cách ly yếu | Chạy trong sandbox · giới hạn filesystem/network |
| AST07 | Trôi phiên bản | Chặn auto-update · ký số bản cập nhật |
| AST08 | Quét sơ sài | Phân tích hành vi, không chỉ quét chuỗi · quét cả phần văn bản tự nhiên |
| AST09 | Không quản trị | Sổ đăng ký skill · phân mức rủi ro · log lần gọi · quy trình thu hồi |
| AST10 | Tái dùng đa nền tảng | Kiểm lại trên từng nền tảng, không giả định tính chất bảo mật giữ nguyên |

**Rủi ro thực tế hay gặp nhất trong nhóm này: AST05.** Prompt injection qua nội dung fetch về — nếu hệ thống đưa dữ liệu người dùng hoặc trang web vào prompt, phải xử lý như **dữ liệu không tin cậy**, không phải chỉ dẫn.

## Nguồn

- OWASP Top 10 (Web) · OWASP Top 10 for LLM Applications
- OWASP Agentic Skills Top 10 — `owasp.org/www-project-agentic-skills-top-10`
