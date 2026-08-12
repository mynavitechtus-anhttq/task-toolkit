# Checklist bảo mật — bản hợp nhất

> **Một file, ba phần.** Phần 1 là checklist kỹ thuật dùng hằng ngày; Phần 2 là bộ yêu cầu khách gửi, giữ
> nguyên `Requirement ID` để nộp lại được; Phần 3 nối hai bên để tra chéo.
>
> Nguồn: `[Techtus] Security Checklist.xlsx` · `Web application security checksheet_ver 2.2.xlsx`.

## Cách dùng

- **Triage một task** → dùng **Phần 1**, chỉ lấy tầng liên quan.
- **Nộp cho khách** → dùng **Phần 2**, trả lời từng `Requirement ID`, **không đổi ID, không gộp dòng**.
- **Không chắc một mục thuộc đâu** → **Phần 3**.

**Ai chịu trách nhiệm** (Phần 1 có sẵn cột): `Devops/Techlead` = hạ tầng & cấu hình · `Engineer` = code ứng dụng.
**Bắt buộc ✓** = mọi dự án phải đạt; trống = tuỳ dự án, **không đạt thì phải ghi lý do**.

---

# Phần 1 — Checklist kỹ thuật theo tầng (74 mục)

## I. Network layer

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 1 | Use secure protocols such as HTTPS/SFTP/SSH to communicate with server | Devops/Techlead | ✓ |
| 2 | Check for inbound/outbound ports of server and only enable necessary ports | Devops/Techlead | ✓ |
| 3 | Restrict IP access for important service such as SSH connection | Devops/Techlead | ✓ |
| 4 | Use Bastion server as a gateway to connect to SSH | Devops/Techlead |  |
| 5 | Does WAF setup for server? | Devops/Techlead |  |

## II. Server configuration

### Directory Traversal

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 6 | Directory browsing should be disabled when accessing a folder via URL | Devops/Techlead | ✓ |
| 7 | Root directory of a web application must contains only entry file (index.php, app.js, etc) or asset files (such as .css, .js, font, images) | Devops/Techlead | ✓ |
| 8 | Config file such as .env, config.php, config.py, config.js, etc MUST NOT be placed at vhost root, and MUST NOT be accessible via URL | Devops/Techlead | ✓ |

### CORS

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 9 | "Access Control Allow Origin" MUST use specific domain name instead of '*' wildcard | Devops/Techlead | ✓ |

### Common

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 10 | Alway enable Basic Authentication for developing environments such as dev/qa/staging | Devops/Techlead | ✓ |
| 11 | With AWS credentials, there need to set only necessary permissions and MUST avoid allow full access | Devops/Techlead | ✓ |
| 12 | Application SHOULD be run with minimal privileges | Devops/Techlead | ✓ |
| 14 | DON'T use mode 0777 for folders | Devops/Techlead | ✓ |
| 15 | DON'T grant root access for deployed source. There need a user with limited permission for deployment | Devops/Techlead |  |
| 16 | OS packages should have latest update (try to use yum update, apt update) | Devops/Techlead |  |
| 17 | Web server & DB Server should be in different physical servers | Devops/Techlead |  |
| 18 | Production application and other application environment MUST be located on different physical servers | Devops/Techlead | ✓ |
| 19 | Is there any antivirus software have been installed on your server? | Devops/Techlead |  |
| 20 | Login/Logout session to server, network devices, firewall should be logged | Devops/Techlead |  |
| 21 | Password MUST be different between servers. With production server, it should be greater than 10 characters and contains upper case, lowercase, underscore and some special characters | Devops/Techlead | ✓ |
| 22 | Server time need to be synced with NTP | Devops/Techlead | ✓ |
| 23 | Version of server software need to be hidden in HTTP Header | Devops/Techlead | ✓ |

## III. Deployment

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 24 | Password for production environment should be kept only by limited in-charge people and MUST be kept secretly with vault | Devops/Techlead | ✓ |
| 25 | Maintenance mode available for new deployment | Devops/Techlead |  |
| 26 | Turn of DEBUG mode | Devops/Techlead | ✓ |

## IV. Programming layer

### Common

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 27 | Web pages that contain sensitive information (payment, transaction history, etc) should be set expire with No Cache | Engineer | ✓ |
| 28 | Form should have CSRF validation to prevent attack | Engineer | ✓ |
| 29 | All errors must have error and exception handling and error stack trace MUST NOT be threw to end user | Engineer | ✓ |
| 30 | Third party packages MUST be checked for vulnerabilities and must be latest update for security patch | Engineer | ✓ |

### Authentication/Authorization

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 31 | Validation check for user own data | Engineer | ✓ |
| 32 | Should have force logout mechanism when user's information or permission has changed (eg: change password, change role, change permission, etc) | Engineer |  |
| 33 | Password policy should be set: Password need at least 8 characters or need to check for password strength | Engineer |  |
| 34 | User's password should be encrypted with salt | Engineer | ✓ |
| 35 | Login credential MUST BE different on each environment (production/staging/qa/dev) | Engineer | ✓ |
| 36 | Use 2FA for system that store very important/sensitive information | Engineer |  |
| 37 | For registration function, does it contain email verification process? | Engineer | ✓ |
| 38 | When login fail, error message should only show "Your login credential is invalid", to prevent bot scanning for password and existence of ID | Engineer | ✓ |

### Privacy

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 39 | With system that contains credit card information, should not show all the numbers but use (*) as mask instead | Engineer | ✓ |
| 40 | Autocomplete MUST BE turn off on the form that contain sensitive information (such as payment form, password input, etc) | Engineer | ✓ |

### Encryption

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 41 | MUST use HTTPS for all incoming requests | Engineer | ✓ |
| 42 | Customer's sensitive information MUST BE encrypted or MUST NOT BE stored if not quite unnecessary (Sensitive information need to be defined by client) | Engineer | ✓ |

### Handling sensitive information

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 43 | Important/sensitive information (password, card info, etc) MUST BE sent via POST request | Engineer | ✓ |
| 44 | MUST NOT commit sensitive information to Git repository (AWS credential, password, secret key, etc) | Engineer | ✓ |
| 45 | JWT SHOULDN'T BE stored in LocalStorage but use Cookie instead | Engineer | ✓ |
| 46 | MUST NOT store sensitive information in JWT payload | — | ✓ |

### Log

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 47 | Success/failed login should be logged | Engineer |  |
| 48 | Lock account after failed login <n> times | Engineer |  |

### Session

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 49 | Session ID MUST BE generated at server side using random UUID (hex string with 32/40 characters length) | Engineer | ✓ |
| 50 | Session SHOULD have reasonable expiry date | Engineer | ✓ |
| 51 | SessionID exchange SHOULD BE done via cookie and MUST NOT pass via URL parameter | Engineer | ✓ |

### Cookie

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 52 | Cookie creation SHOULD have Secure flag | Engineer | ✓ |
| 53 | Cookie should store minimum information | Engineer | ✓ |
| 54 | Cookie MUST have domain, path | Engineer | ✓ |

### SQL Injection

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 55 | Request input MUST be sanitized and slash stripped for special characters such as single quote, double quote | Engineer | ✓ |
| 56 | Use parameter bind mechanism for raw SQL query | Engineer | ✓ |
| 57 | Does your in-use Framework has sanitize input or bind parameter as default mechanism for data model query? | Engineer | ✓ |

### Cross Site Scripting (XSS)

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 58 | Input from user MUST be validated. String input NEED to be stripped HTML tag and do escape special characters | Engineer | ✓ |
| 59 | Does your in-use Framework has middleware to prevent XSS attack? | Engineer |  |

### OS Command Injection

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 60 | User's upload file MUST NOT be executable at server side | Engineer | ✓ |
| 61 | If your application allow server command execution, need to make sure those commands MUST NOT be affected by user's input | Engineer | ✓ |

### Directory Traversal

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 62 | Path to file/folder if available on URL, there need a mechanism for authorization check to make sure it won't be discovered or accessible by other user | Engineer | ✓ |
| 63 | Path to file/folder SHOULD be hashed by random UUID | Engineer |  |

### CSRF

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 64 | Does your in-use Framework has middleware to prevent CSRF attack? | Engineer |  |

### User files

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 65 | User uploaded files MUST BE stored in isolated location and far from files that generated by system (such as cache, backup, import, export, etc) | Engineer | ✓ |
| 66 | User's uploaded files MUST be limit in size and allowed extensions | Engineer | ✓ |
| 67 | User MUST NOT be able to specify the location of uploaded files | Engineer | ✓ |

## V. Database Layer

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 68 | Only allow access from internal IP | Devops/Techlead | ✓ |
| 69 | Root password MUST BE different between environments, greater than 10 characters length and not easy to guess (Including digits uppercase, lowercase, and special characters) | Devops/Techlead | ✓ |
| 70 | Does your server and data has scheduling for backup (How often?) | Devops/Techlead |  |
| 71 | Does your system has recovery plan? | Devops/Techlead |  |

## VI. Client browser/UI Display

| # | Mục | Ai | Bắt buộc |
|---|---|---|---|
| 72 | NEVER show password in UI, user's entered password must be masking using '*' | Engineer | ✓ |
| 73 | When system got error, MUST not show error in detail | Engineer | ✓ |
| 74 | Does your form use Captcha to prevent bot for public forms? | Engineer |  |
| 75 | When rendering content, have you strip or escape HTML tag for content that show raw text? | Engineer | ✓ |

---

# Phần 2 — Yêu cầu từ checksheet khách (153 requirement)

> Bản gửi khách. Mỗi dòng có `Requirement ID` cố định — trả lời từng dòng, giữ nguyên ID.
> Cột **SL** = service level (`1` = áp dụng cho mọi hệ thống).

## 2.1. Database security

### Đối sách SQL injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_db_001` | Việc chọn data, query database (ví dụ: SQL, HQL, ORM, NoSQL) được bảo vệ bằng cách parameter hoá các query, ORM, Entity Framework hoặc các phương pháp tương đương, không bị ảnh hưởng bởi tấn công database Injection. | 1 |  |

### Đối sách LDAP injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_db_002` | Ứng dụng không bị ảnh hưởng bởi LDAP Injection, hoặc có biện pháp kiểm soát bảo mật ngăn chặn LDAP Injection. | 1 |  |

### Đối sách XPath injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_db_003` | Ứng dụng được bảo vệ khỏi tấn công XPath injection và XML injection. | 1 |  |

## 2.2. Đối sách liên quan hiển thị màn hình

### Cross-Site Scripting

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_display_001` | Tất cả các biến string có trong HTML hoặc web client code khác được en-code thủ công phù hợp theo ngữ cảnh, hoặc sử dụng template thực hiện en-code tự động theo ngữ cảnh, giúp ứng dụng không bị ảnh hưởng bởi tấn công phản xạ, lưu trữ và tấn công DOM base Cross-site Scripting (XSS) | 1 |  |

### Biện pháp phòng ngừa rò rỉ thông tin do comment trong các loại file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_display_002` | Xóa những comment không cần thiết. | 1 |  |

### Đối sách liên quan màn hình nhập thông tin quan trọng

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_display_003` | Những thông tin quan trọng mà chỉ cá nhân mới biết, chẳng hạn như mã PIN, số hộ chiếu, số thẻ bảo hiểm y tế và số bằng lái xe, sẽ được masking (bằng các ký tự mờ như *) rồi mới hiển thị. Implement option để khi cần hiển thị thông tin đăng ký, bật setting để tạm thời hiển thị trên màn hình | 1 |  |
| `webapp_v2.2_display_004` | Các form nhập thông tin đặc biệt nhạy cảm và quan trọng, chẳng hạn như mã PIN và số nhận dạng cá nhân, nên được setting thuộc tính mật khẩu và masking. Implement option để khi cần hiển thị thì bật setting để tạm thời hiển thị ra forrm. | 1 |  |
| `ứng dụng web_v2.2_display_005` | Các thông tin quan trọng không được lưu giữ trên màn hình (bao gồm cả trong hidden field) khi chuyển màn hình normal hoặc trong quá trình kiểm tra lỗi. Trường ợp cần giữ lại, phải ghi rõ lý do chưa xử lý trong mục “Lý do chưa đối ứng" trong checksheet. | 1 |  |

### Đối sách khi sử dụng JSONP

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_display_006` | Không sử dụng JSONP nếu trong response có chứa thông tin quan trọng. Nếu trong response có chứa thông tin quan trọng thì phải implement JSON sử dụng (vì JSONP không bị hạn chế bởi CORS và có thể được truy cập từ các nguồn khác, nên có nguy cơ thông tin nhạy cảm bị rò rỉ). | 1 |  |

### Đối sách khi sử dụng 3.3.4.JSONP

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_display_007` | Phía server phải xác nhận rằng tên hàm callback chỉ bao gồm ký tự chữ và số. Nếu chứa ký tự ngoài bảng chữ số, phải trả về lỗi ngay lập tức. | 1 |  |

### Đối sách khi sử dụng Cross-Origin communication

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_hiển thị_008` | Khi sử dụng giao tiếp cross-origin, chỉ cho phép access origin tối thiểu cần thiết bằng cách cấu hình CORS (Access-Control-Allow-Origin) | 1 |  |
| `webapp_v2.2_display_009` | Tại XMLHttpRequest, setting request header "X-Requested-With: XMLHttpRequest", thực hiện check bên phía server | 1 |  |

## 2.4. Đối sách khi sử dụng HTML5

### Đối sách khi sử dụng Web Storage

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_html5_001` | Không đưa thông tin nhạy cảm vào Web Storage. | 1 |  |
| `ứng dụng web_v2.2_html5_002` | Không đưa vào nội dung có thể gây ra vấn đề nếu bị giả mạo. | 1 |  |

### Đối sách khi sử dụng Cross Document Messaging

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_html5_003` | Để ngăn chặn việc gửi hoặc nhận tin nhắn đến những địa chỉ không mong muốn, khi nhận gửi, sẽ check origin đích connect có đúng hay không | 1 |  |

## 2.5. Đối sách khi liên kết external

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_linkage_001` | Không đưa thông tin quan trọng vào URL hoặc query string. Nếu cần tạo external link có chứa thông tin quan trọng, thì phải kiểm tra xem domain đó có được cho phép hay không. Trường hợp không thể kiểm tra domain do service spec, thì tạm thời di chuyển sang page dùng cho link (cushion page) rồi mới hiển thị lại link | 1 |  |
| `webapp_v2.2_linkage_002` | Trước khi gửi thông tin quan trọng external service web, phải được phê duyệt qua quy trình nội bộ công ty, bao gồm cả đơn xin ngoại lệ (nếu có), và tuân thủ các biện pháp được chỉ định. | 1 |  |
| `webapp_v2.2_linkage_003` | Khi sử dụng các external web service (bao gồm cả dịch vụ đám mây) như dịch vụ phân phối email, servey form, WAF,... vui lòng sử dụng các service common của công ty Mynavi. Chi tiết về service common thì vui lòng tham khảo trang web nội bộ (http://inet-cms.int.mynavi.jp/sysintra/). | 99 |  |

## 2.6. Đối sách liên quan đến các xử lý quan trọng

### Đối sách Cross-Site Request Forgery

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_csrf_001` | Trong các hệ thống sử dụng cookie, tại các màn hình thực hiện các xử lý quan trọng (như thay đổi mật khẩu, cập nhật thông tin cá nhân, mua sản phẩm, thực hiện thanh toán, đăng bài trên bảng tin, gửi email, hủy tư cách thành viên/đăng ký, chấp thuận đơn đăng ký và thêm chữ ký), cần triển khai các biện pháp chống Cross-Site Request Forgery (CSRF) bằng các cách như Anti-CSRF token trong request header, Anti-CSRF token qua hidden parameter, nhập lại mật khẩu, check Origin header trong request (trình tự ưu tiên theo trình tự đã viết ra ở đây). | 1 |  |

## 2.7. Đối sách khi sử dụng OS command

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_osci_001` | Phải được bảo vệ khỏi OS Command Injection, và Operationg system sử dụng OS query đã được tham số hóa, hoặc sử dụng context command line output encoding | 1 |  |

## 2.8. Đối sách khi access fi;e

### Đối sách Directory Traversal

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileaccess_001` | Không tạo cơ chế chỉ định trực tiếp file-name. Khi chỉ định file. directory vào đối số, thì bên server hãy sử dụng file-name cố định, hoặc hạn chế các ký tự và chuỗi có thể sử dụng. Ngoài ra, hãy từ chối các đường dẫn không mong muốn sử dụng dấu ".", "/", "\", v.v. | 1 |  |

### Forced browsing

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileaccess_002` | Những file được lưu trong directory công khai là các CGI program và file HTML thôi. | 1 |  |

## 2.9. Các biện pháp liên quan đến chức năng email

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_mail_001` | Bảo vệ khỏi tấn công SMTP hoặc IMAP bằng cách khử trùng thông tin đầu vào của người dùng trước khi ứng dụng truyền sang mail service. | 1 |  |
| `webapp_v2.2_mail_002` | Mật khẩu sẽ không được gửi qua email do nguy cơ bị nghe lén mạng. Tuy nhiên, điều này không áp dụng cho mật khẩu tạm thời, vì bắt buộc phải thay đổi khi đăng nhập lần đầu. | 1 |  |
| `webapp_v2.2_mail_003` | Khi gửi cùng một nội dung cho nhiều người dùng, chẳng hạn như bản tin email, hãy đảm bảo rằng trong TO hoặc Cc không có địa chỉ email của người dùng (không liên quan đến nhau) | 1 |  |
| `webapp_v2.2_mail_004` | Chúng tôi sử dụng các biện pháp để ngăn chặn email giả mạo, chẳng hạn như SPF, DKIM (Domainkeys Identified Mail,) DMARC, nhằm tăng độ tin cậy của email. | 2 |  |

## 2.10. Đối sách xử lý redirectory

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_redirect_001` | Các đích chuyển hướng và URL trong frame không được tạo từ các request parameter, và đang có thực hiện các biện pháp ngăn chặn các chuyển hướng không mong muốn. | 1 |  |

## 2.11. Đối sách liên quan check input

### Check input

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_input_001` | Đối với các đối số và cookie nhận được trên server thì thực hiện check tính hợp lệ của các giá trị cố định, giá trị mong đợi (kiểu ký tự, định dạng giá trị, độ dài chuỗi) và ký tự control (ký tự NULL và mã xuống dòng). Việc check giá trị input được thực hiện trên server application chứ không phải trên frontend. | 1 |  |

## 3.9. Đối sách check input

### Đối sách HTTP Header Injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_input_002` | Khi sử dụng giá trị input làm giá trị HTTP header, thì không xuất trực tiếp header, mà hãy sử dụng API output header đã được chuẩn bị theo ngôn ngữ/ môi trường thực hiện. Nếu cần output trực tiếp, thì trước khi output, hãy mã hóa URL hoặc vô hiệu hoá mã xuống dòng. | 1 |  |

## 2.12. Đối sách liên quan quản lý session

### Phương pháp quản lý session

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_001` | Session p được phát hành và hủy bỏ vào timing hợp lý, và đang được quản lý thích hợp. | 1 |  |
| `webapp_v2.2_session_002` | Thời gian valid session khuyến nghị là 30 phút. Ngay cả khi vượt quá 30 phút, thời gian valid của session cũng chỉ nên tối đa là một tuần, và phải ghi thời gian cụ thể và lý do cần được mô tả trong cột "Lý do không đối ứng" của checksheet | 2 |  |

### Đối sách liên quan Cookie

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_003` | Về cơ bản, chỉ nên lưu thông tin session ID trong cookie (sử dụng chức năng quản lý session của ngôn ngữ phát triển để lưu session ID vào cookie). Nếu cần sử dụng thông tin khác ngoài Session ID, chỉ sử dụng cho các tính năng không gây rủi ro nếu bị giả mạo (ví dụ: tính năng cá nhân hóa người dùng), hoặc phải được mã hóa. Về thời gian hiệu lực của thông tin sử dụng lúc đó, cần cần setting thời gian ngắn nhất có thể. *Khi hiển thị giá trị cookie trên màn hình, phải thực hiện các biện pháp chống XSS (Cross-site Scripting) (tham khảo mục "2.2.1. Biện pháp chống XSS phía server"). | 2 |  |
| `webapp_v2.2_session_004` | Các cookie quan trọng như cookie session, cookie nhận dạng user... thì phải được thêm thuộc tính Secure | 2 |  |
| `webapp_v2.2_session_005` | Các cookie quan trọng như cookie session, cookie nhận dạng user... thì phải được thêm thuộc tính HttpOnly. | 2 |  |
| `webapp_v2.2_session_006` | Các cookie quan trọng như cookie session, cookie nhận dạng user... thì phải thêm thuộc tính SameSite, và chỉ định Strict hoặc Lax tùy theo yêu cầu của trang web. | 2 |  |

## 3.10. Đối sách quản lý session

### Đối sách liên quan query string

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_007` | Thông tin có tính bảo mật cao (ID đăng nhập, mật khẩu, v.v.) và thông tin cần duy trì tính toàn vẹn của dữ liệu (thông tin giá cả, quyền của người dùng, v.v.) thì không nên được đưa vào query string (GET method), mà phải sử dụng method POST. | 1 |  |

### 3.10.3. Đối sách URL paramater

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_008` | Khi truyền nhận data với các page có tác dụng phụ (như đăng ký, cập nhật hoặc xóa cơ sở dữ liệu hoặc gửi email), thì không sử dụng query string (GET method), mà phải sử dụng method POST. | 1 |  |

### Đối sách liên quan field hidden

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_009` | Không lưu các thông tin không được phép ghi đè (ví dụ nhưu thông tin giá cả) trong các field hidden. Chỉ lưu trữ các giá trị key (chẳng hạn như mã sản phẩm), còn các thông tin khác ví dụ như giá cả thì luôn tham chiếu thông tin mới nhất từ DB. | 1 |  |

### 3.10.4. Đối sách field hidden

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_010` | Trường hợp truyền nhận parameter giữa nhiều page trong field hidden cũng phải thực hiện check input trên server application. Ví dụ: Trường hợp di chuyển từ "màn hình input" => "màn hình xác nhận" => "màn hình xử lý đăng ký", thì việc check input không chỉ nên được thực hiện trên "màn hình xử lý đăng ký" mà còn phải thực hiện trên cả "màn hình input" và "màn hình xác nhận". | 1 |  |

### Đối sách liên quan biến số session

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_session_011` | Việc truyền nhận ID đăng nhập và quyền của user thì không sử dụng field hidden, query string, mà phải sử dụng biến session. | 2 |  |

## 2.13. Error message

### Đối sách khi lỗi check input

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_errormsg_001` | Trên các màn hình sau, khi bị lỗi input, không hiển thị thông báo cho biết tính chính xác của từng trường, chẳng hạn như "ID đăng nhập không tồn tại" hoặc "Mật khẩu không đúng", mà phải hiển thị message không đoán được nguyên nhân lỗi, ví dụ như "ID đăng nhập hoặc mật khẩu không đúng". - Màn hình đăng nhập - Màn hình thay đổi mật khẩu - Màn hình đặt lại mật khẩu - Màn hình thanh toán (chẳng hạn như nhập số thẻ tín dụng) | 2 |  |

## 3.11. Đối sách error message

### Đối sách khi lỗi nội bộ

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_errormsg_002` | Implement xử lý lỗi thích hợp, để khi xảy ra lỗi, sẽ không hiển thị thông tin chi tiết lỗi bên phía client, không gây ra hoạt động không đúng. | 1 |  |

## 2.14. Đối sách liên quan I/O của file

### Đối sách khi download file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileio_001` | Quản lý quyền truy cập file một cách phù hợp, ngoại trừ những file được phép rò rỉ. | 1 |  |

## 3.12. Đối sách liên quan I/O của file

### 3.12.1. Đối sách khi download file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileio_002` | Các file tạo tạm thời thì không được tạo trong directory công khai, và phải được xóa sau khi một khoảng thời gian nhất định. | 1 |  |

### Đối sách khi upload file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileio_003` | Check định dạng file (đuôi mở rộng) và kích thước của file upload. Chỉ trường hợp được phép mới thực hiện upload. | 1 |  |

### 3.12.2. Đối sách khi upload file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileio_004` | Apply phần mềm diệt virus, và implement chức năng tự động kiểm tra virus khi upload. | 2 |  |
| `webapp_v2.2_fileio_005` | Đối với file đã upload, set quyền access thích hợp, không quá mức cần thiết, nếu không cần thì xoá đi | 1 |  |
| `webapp_v2.2_fileio_006` | Khi upload file tương ứng với thông tin quan trọng thì sử dụng chức năng mã hoá đích lưu sau khi upload để mã hoá rồi lưu (để giảm risk trong trường hợp file sau khi upload bị rò rỉ) | 2 |  |

## 2.15. Đối sách khi include file

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_fileinclude_001` | Ứng dụng của bạn không bị ảnh hưởng bởi Remote File Inclusion (RFI) và Local File Inclusion (LFI). | 1 |  |

## 2.16. Đối sách kiên quan character code

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_charcode_001` | Chỉ định mã hóa ký tự khi kết nối với cơ sở dữ liệu. | 1 |  |

## 2.17. Sử dụng Serialized Object

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_serialize_001` | Không deserialize các giá trị nhận được từ input mà có thể bị thay đổi từ bên ngoài như query string, tham số POST, cookie... | 1 |  |

## 3.15. Đối sách evel injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_serialize_002` | Nếu bắt buộc phải deserialize giá trị input external (theo spec), thì phải áp dụng mã hóa, chữ ký điện tử, hoặc HMAC để ngăn việc bị sửa đổi. | 1 |  |
| `webapp_v2.2_serialize_003` | Nếu phát hiện bất kỳ sửa đổi nào, thông tin chi tiết sẽ được ghi lại trong application log | 1 |  |

## 2.18. Đối sách liên quan multi-thread

### Đối sách liên quan multi-thread programing

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_multithread_001` | Khi cập nhật cơ sở dữ liệu, một loạt các quy trình như kiểm tra điều kiện cập nhật, get data trước khi cập nhật, cập nhật ...được nhóm lại với nhau dưới dạng giao dịch và khóa hàng được áp dụng. | 1 |  |

## 3.16. Đối sách multi-thread

### 3.16.1. Đối sách multi-thread programing

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_multithread_002` | Khi cập nhật một file được sharing từ nhiều proccess/thread, thì thực hiện access loại trừ theo lock | 1 |  |
| `webapp_v2.2_multithread_003` | Khi cập nhật sharing memory, thì việc này được thực hiện ở trạng tháicbị khóa bằng semaphore chẳng hạn | 1 |  |

### Đối sách khi sử dụng Java Servlets

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_multithread_004` | Trong Java Servlet, không sử dụng biến instance servlet class. Nếu bạn phải sử dụng chúng, thì hãy implement Exclusive Control | 1 |  |

### 3.16.2. Đối sách khi sử dụng Java Servlet

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_multithread_005` | Trong Java Servlet, không sử dụng biến tĩnh (biến static) khi xử lý thông tin cụ thể của người dùng. | 1 |  |

## 2.19. Đối sách liên quan XML

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_xml_001` | Application hạn chế server XML đúng đắn, chỉ sử dụng cấu hình hạn chế nhất có thể , và ngăn chặn XXE bằng cách vô hiệu hóa các tính năng nguy hiểm như giải quyết external entity... | 1 |  |

## 2.20. Đối sách liên quan Server-Side Template Injection

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_templatei_001` | Ứng dụng được bảo vệ chống lại các cuộc tấn công chèn mẫu bằng cách khử trùng hoặc cách ly dữ liệu đầu vào của người dùng. | 1 |  |

## 2.21. Đối sách liên quan Server‑Side Request Forgery

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_ssrf_001` | Các ứng dụng được bảo vệ khỏi các cuộc tấn công làm giả yêu cầu từ phía máy chủ bằng cách xác thực hoặc khử trùng dữ liệu không đáng tin cậy và siêu dữ liệu tệp HTTP như tên tệp và trường nhập URL, cũng như bằng cách sử dụng danh sách trắng cho các giao thức, tên miền, đường dẫn và cổng. | 1 |  |

## Xác thực

### Đăng nhập

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_authentication_001` | Application đang được bảo vệ khỏi Template Injection bằng cách khử độc input của user hoặc sandbox hóa | 2 |  |
| `webapp_v2.2_authentication_002` | Tại login form, ngoài xác thực ID đăng nhập và mật khẩu, sẽ hỗ trợ một trong các tùy chọn sau: - Giới hạn địa chỉ IP - Basic auth/Digest auth - Xác thực đa yếu tố - Triển khai CAPTCHA | 2 |  |
| `webapp_v2.2_authentication_003` | Khi thất bại liên tiếp với cùng login ID, thì lock. Về số lần thất bại liên tiếp, thời gian lock thì quyết định theo từng service. Nếu không có yêu cầu đặc biệt thì setting tiêu chuẩn PCI DSS (Payment Card Industry Data Security Standard) (5 lần thất bại liên tiếp, thời gian lock tối thiểu 30 phút) | 2 |  |

### Đăng xuất

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_authentication_004` | Cung cấp chức năng logout rõ ràng và hủy session bên phía server (xem ở mục "2.12 Đối sách liên quan quản lý sesion") | 2 |  |
| `webapp_v2.2_authentication_005` | Cung cấp chức năng logout tự động do session timeout. Thời gian session timeout thì xác định theo từng service. Nếu không có thời gian cụ thể, hãy setting là 30 phút (về cách setting thời gian session timeout thì xem tại mục "2.12 Đối sách về quản lý session") | 2 |  |

## Quản lý account

### Cấp ID đăng nhập

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_account_001` | Đối với ID login thì không sử dụng các số ID cố hữu thường được sử dụng chung cho nhiều mục đích khác nhau, chẳng hạn như Mynumber hoặc số tài khoản. | 2 |  |

### 4.2.1. Cấp ID đăng nhập

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_account_002` | Trường hợp cấp ID login tự động thì không thực hiện gán ID login là các số liên tiếp, chỉ khác nhau một chữ số là thành user khác. | 2 |  |
| `webapp_v2.2_account_003` | Không thể sử dụng ID login trùng lặp. | 2 |  |
| `webapp_v2.2_account_004` | Không thể sử dụng ID login giống với ID login đã hủy đăng ký trước đó. Tuy nhiên, nếu ID login là thông tin khó thay đổi như địa chỉ email của người dùng và có khả năng tái đăng ký, thì có thể ngoại lệ. Trong trường hợp đó, về nguyên tắc, tài khoản sẽ được xử lý như một người dùng mới. Nếu cần kế thừa trạng thái ngay trước khi huỷ đăng ký, thì cần thiết lập quy trình confirm chính chủ. | 2 |  |

### Cấp mật khẩu

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_account_005` | Không hiển thị mật khẩu trên màn hình. Hiển thị form nhập mật khẩu với thuộc tính password. | 2 |  |
| `webapp_v2.2_account_006` | Nếu người dùng muốn, mật khẩu có thể được hiển thị tạm thời trên màn hình. Nếu frame-work không hỗ trợ implement tính năng này thì cho hiển thị ký tự cuối cùng của mật khẩu đã nhập. | 2 |  |
| `webapp_v2.2_account_007` | Chức năng thay đổi mật khẩu sẽ được cung cấp để người dùng có thể thay đổi mật khẩu bất cứ lúc nào. | 2 | O |
| `webapp_v2.2_account_008` | Số ký tự tối thiểu có thể đặt làm mật khẩu là 8 ký tự trở lên và số ký tự tối đa là 64 ký tự trở lên. | 1 | O |
| `webapp_v2.2_account_009` | Nếu mật khẩu có độ dài dưới 12 ký tự, mật khẩu phải chứa ít nhất hai trong các loại ký tự sau: chữ cái tiếng Anh viết hoa, chữ cái tiếng Anh viết thường, chữ số Ả Rập và các ký tự không phải chữ và số (ký hiệu đặc biệt, dấu câu và ký hiệu). | 1 | O |
| `webapp_v2.2_account_010` | Trường hợp cấp mật khẩu default trong hệ thống, hãy sử dụng các số ngẫu nhiên để loại bỏ bất kỳ quy luật nào và là một chuỗi gồm 8 chữ số trở lên khó đoán. Các ký tự có thể được sử dụng trong chuỗi phải tuân thủ Requirement ID "webap-v2.0-account-009". Ngoài ra, phải force user thay đổi mật khẩu. | 2 | O |
| `webapp_v2.2_account_011` | Mật khẩu tạm thời do hệ thống cấp khi cấp ID đăng nhập phải được thay đổi trước lần đăng nhập đầu tiên. Mật khẩu tạm thời phải được cài thời gian valid (tối đa 24 giờ), và nếu mật khẩu thực tế không được đăng ký trước khi hết hạn, mật khẩu sẽ bị vô hiệu hóa. | 2 | O |
| `webapp_v2.2_account_012` | Không thiết kế tài khoản có mục đích chia sẻ cho nhiều người. | 2 |  |
| `webapp_v2.2_account_013` | Khi đăng ký mật khẩu vào DB, lưu giá trị đã được hash sử dụng salt. Hàm hash sử dụng thì có các hàm được cho phép trong "3.4 TLS", còn chi phép cả PBKDF2 và bcrypt. | 2 |  |
| `webapp_v2.2_account_014` | Nếu sử dụng PBKDF2 để hash, thì iteration phải được setting từ 100.000 lần trở lên. | 2 |  |
| `webapp_v2.2_account_015` | Nếu sử dụng bcrypt để hash, thì worker phải được setting từ 13 trở lên. | 2 |  |
| `webapp_v2.2_account_016` | Mật khẩu tạm thời và mật khẩu do quản trị viên cấp được thiết kế để người dùng tự thay đổi khi sử dụng dịch vụ lần đầu tiên. | 2 | O |

### Đặt lại mật khẩu

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_account_017` | Không có gợi ý mật khẩu hoặc xác thực dựa trên kiến ​​thức (còn gọi là "câu hỏi bí mật"). | 2 | O |

## 3.3. Authorization

### Xử lý Authorization

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_authorization_001` | Quyền truy cập và quyền thực thi của người dùng được kiểm soát ở phía server bằng cách sử dụng session ID mỗi khi có yêu cầu truy cập. | 2 |  |

## 4.3. Authorization

### Xử lý Authorization

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_authorization_002` | Thông tin quyền không được lưu trong các parameter phía client ví dụ: admin=true). Thông tin quyền được quản lý ở phía server bằng session ID | 2 |  |
| `webapp_v2.2_authorization_003` | Cấm truy cập vào các chức năng quản trị từ Internet mà không hạn chế quyền truy cập. Nếu cần truy cập các chức năng quản trị từ internet segment khác với internet segment nơi server cài đặt, thì ngoài việc xác thực thông thường bằng ID đăng nhập và mật khẩu, hãy sử dụng các biện pháp bảo mật nâng cao hơn như hạn chế địa chỉ IP có thể truy cập, xác thực lẫn nhau bằng chứng chỉ client, xác thực hai yếu tố, giao tiếp mã hóa giữa các thiết bị và cơ sở bằng VPN, v.v. | 2 |  |
| `webapp_v2.2_authorization_004` | Không đăng nhập người quản trị và người dùng chung trên một màn hình chung (cùng URI). | 2 |  |

## 3.4. TLS

### Mã hóa dữ liệu trên đường truyền: ※Nếu hệ thống sử dụng nền tảng của Mynavi Cloud, thì việc quản lý các yếu tố như giao 

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_authorization_005` | Biến toàn bộ trang web thành trang TLS. | 1 |  |
| `webapp_v2.2_authorization_006` | Chỉ HTTPS mới được phép sử dụng cho các trang TLS và giao tiếp HTTP sẽ bị từ chối hoặc chuyển hướng đến URL HTTPS để không thể truy cập qua HTTP. | 1 |  |
| `ứng dụng web_v2.2_tls_001` | Cấm sử dụng SSL 2.0, SSL 3.0, TLS 1.0 và TLS1.1. | 1 | O |
| `ứng dụng web_v2.2_tls_002` | Không sử dụng các thuật toán mã hóa có độ mạnh mã hóa yếu. Hãy sử dụng các thuật toán mã hóa được liệt kê trong Danh sách Mã hóa CRYPTREC làm tiêu chuẩn cho các thuật toán khả dụng và sử dụng các thuật toán mã hóa có độ mạnh hơn các thuật toán được liệt kê. Ngay cả trong các trường hợp sau, mong muống áp dụng một tiêu chuẩn có độ mạnh mã hóa cao hơn, nhưng nếu không thể implement được thì chấp nhận sử dụng tiêu chuẩn tương ứng. - Nếu tiêu chuẩn khác với luật pháp của mỗi quốc gia, tiêu chuẩn do luật pháp của quốc gia đó thiết lập sẽ được sử dụng. - Nếu tiêu chuẩn khác với tiêu chuẩn ngành, tiêu chuẩn do ngành đó thiết lập sẽ được sử dụng. Tham khảo: http://www.cryptrec.go.jp/list.html | 1 | O |
| `ứng dụng web_v2.2_tls_003` | Cấm mua mới hoặc gia hạn chứng chỉ có khóa công khai có độ dài nhỏ hơn 2048 bit. | 1 |  |
| `ứng dụng web_v2.2_tls_004` | Cấm mua mới hoặc gia hạn chứng chỉ có hàm hash là MD5, SHA-1. | 1 |  |
| `ứng dụng web_v2.2_tls_005` | Chứng chỉ sử dụng trên site PROD dành cho ngoài công ty thì sử dụng chứng chỉ EV. Tuy nhiên, ngoại trừ trong các trường hợp sau: "FQDN không dành cho người dùng truy cập trực tiếp, chẳng hạn như những FQDN được sử dụng để phân phối contents tĩnh", "việc gia hạn chứng chỉ được tự động hóa bằng Amazon Certification Manager hoặc chức năng tương tự để giảm gánh nặng vận hành". | 1 |  |

## 3.6. Service thanh toán

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_payment_001` | Không lưu bất kỳ thông tin thẻ tín dụng nào. Và trong web application cũng không gửi hoặc nhận thông tin thẻ tín dụng | 2 |  |
| `webapp_v2.2_payment_002` | Khi sử dụng chức năng thanh toán, thì sử dụng service đại lý thanh toán | 2 |  |
| `webapp_v2.2_payment_003` | Lưu lại lịch sử thao tác liên quan thanh toán, để người dùng có thể tự kiểm tra. | 2 |  |
| `webapp_v2.2_payment_004` | Đặt giới hạn số tiền thanh toán. | 2 |  |
| `webapp_v2.2_payment_005` | Trước khi thực hiện xử lý thanh toán, người dùng được yêu cầu nhập lại mật khẩu (xác thực lại). | 2 |  |
| `webapp_v2.2_payment_006` | Các trường nhập liệu của người dùng không bao gồm tên sản phẩm, giá cả, v.v. | 2 |  |

## 3.7. Quản lý khóa mã hoá

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_key_001` | Khi mã hóa dữ liệu, hãy xác định phương pháp quản lý khóa mã hóa và lập thành văn bản, để ngăn chặn việc rò rỉ. Khi xác định phương pháp quản lý, cấm tuyệt đối việc hard-coding và lưu khóa ở dạng văn bản thuần (plain text). | 1 |  |

## 4.1 Setting của Web server

### Directory Listing

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_001` | Setting web server để nghiêm cấm việc directory listing | 1 |  |
| `webapp_v2.2_webserver_002` | Vô hiệu hóa UserDir directive | 1 |  |
| `webapp_v2.2_webserver_003` | Đối với người dùng chạy web server thì chỉ gắn quyền truy cập tối thiểu cần thiết. | 1 |  |

### Không hiển thị thông tin Web server

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_004` | Xóa thông tin server header không cần thiết. | 1 |  |
| `webapp_v2.2_webserver_005` | Không hiển thị thông tin version web server, thông tin lỗi server internal trong response, bao gồm cả màn hình lỗi. | 1 |  |

### Cache Control

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_006` | Khi hiển thị thông tin cá nhân hoặc thông tin quan trọng, cần thực hiện điều khiển bộ nhớ đệm (cache control) để tránh việc thông tin đó bị lưu lại trong web browser hoặc proxy server. ※ Do cách kiểm soát bộ nhớ đệm khác nhau tùy theo CDN service hoặc cache server, nên cần kiểm tra kỹ spec của CDN service, cache server rồi mới thực hiện setting. | 1 |  |

### Sử dụng phần mềm an toàn

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_007` | Thiết lập các quy tắc vận hành để áp dụng các security patch mới nhất của OS/software. Đặc biệt, thiết lập một hệ thống có khả năng xác định và ứng phó ngay lập tức với các mối đe dọa rủi ro cao, chẳng hạn như các mối đe dọa liên quan đến bảo mật, bao gồm rò rỉ thông tin, mà lại dễ thực hiện. | 1 | O |
| `webapp_v2.2_webserver_008` | Định kỳ update OS, software version và ít nhất là không sử dụng các vesion ngoài đối tượng support, hoặc chỉ support một phần chẳng hạn như "chỉ áp dụng các security patch quan trọng". | 1 | O |
| `webapp_v2.2_webserver_009` | Không sử dụng frame-worin của riêng biệt của công ty phát triển. | 1 |  |
| `webapp_v2.2_webserver_010` | Ở trạng thái có thể liệt kê và kiểm tra danh sách mới nhất OS và software (bao gồm cả version) được mà system đang sử dụng, và apply cơ chế phát hiện các lỗ hổng trong hệ thống dựa trên danh sách này. | 1 | O |

### Xác định phương thức HTTP nào sẽ được hỗ trợ

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_011` | Chỉ chấp nhận các phương thức HTTP đang được sử dụng trong application, API, bao gồm cả pre-flight OPTIONS | 1 |  |

### Thận trọng khi sử dụng WebDAV

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_webserver_012` | Trường hợp sử dụng WebDAV, thì không công khai lên Internet. | 1 |  |
| `webapp_v2.2_webserver_013` | Trường hợp cần phải công khai lên Internet, thì phải giới hạn IP address đích kết nối, hoặc setting để chỉ có thể truy cập thông qua kết nối VPN. | 1 |  |
| `webapp_v2.2_webserver_014` | Setting quyền phù hợp theo người dùng, chẳng hạn như ghi, thay đổi và xóa. | 1 |  |

## 4.4. Những lưu ý trên môi trường phát triển

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_dev_001` | Một môi trường chuyên dụng cho phát triển và test sẽ được chuẩn bị, tách biệt với môi trường vận hành. | 1 |  |
| `ứng dụng web_v2.2_dev_002` | Đối với môi trường không phải môi trường PROD, hãy hạn chế nguồn kết nối hoặc thiết lập xác thực. | 1 |  |
| `ứng dụng web_v2.2_dev_003` | Trên môi trường không phải môi trường PROD, không sử dụng data của môi trường PROD, data chứa thông tin cá nhân, mà phải tạo dummy data để sử dụng. Tuy nhiên, nếu bắt buộc phải sử dụng data PROD thì cố gắng masking thông tin cá nhân càng nhiều càng tốt, và sử dụng TLS cho tất cả các giao tiếp liên quan đến các chức năng xử lý thông tin cá nhân (quy định về TLS tuân thủ "3.4.TLS"). | 1 |  |

## 4.5. Những lưu ý trên môi trường PROD

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_prod_001` | Xóa mọi tính năng debug được sử dụng trong quá trình phát triển. | 1 |  |
| `webapp_v2.2_prod_002` | Việc tạo file backup trong directory công khai là bị cấm. | 1 |  |
| `webapp_v2.2_prod_003` | Các file trên Web server mà không còn sử dụng nữa thì không đặt trong directory công khai | 1 |  |

## 4.6. Bảo vệ thông tin cá nhân

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_pii_001` | Tạo và công khai page phương châm bảo vệ thông tin cá nhân. Đồng thời, hãy tạo chức năng xin phép khi thu thập thông tin cá nhân. | 2 |  |

## HTTP securiry header

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_header_001` | Mã ký tự cần thiết lập trong Content-Type của HTTP response header phải là UTF-8 và cần thiết lập như sau: Content-Type: text/html; charset=UTF-8 | 1 |  |
| `webapp_v2.2_header_002` | Setting X-Content-Type-Options: nosniff trong tất cả các HTTP response header. | 1 |  |
| `webapp_v2.2_header_003` | Để giảm thiểu các cuộc tấn công cross-site scripting và clickjacking, hãy setting header liên quan Contenst Security Policy sau vào HTTP response header. Content-Security-Policy: default-src 'self' X-Content-Security-Policy: default-src 'self' | 99 |  |
| `webapp_v2.2_header_004` | Đối với màn hình có button thực hiện "xử lý quan trọng", hãy setting X-FRAME-OPTIONS trong HTTP response header. Chọn DENY hoặc SAMEORIGIN làm giá trị. | 1 |  |
| `webapp_v2.2_header_005` | Đối với các dịch vụ chỉ được cung cấp qua HTTPS, hãy setting Strict-Transport-Security trong HTTP response header. Giá trị max-age thì xem xét tương ứng với spec của site | 1 |  |
| `webapp_v2.2_header_006` | Khi thực hiện download file, thì setting Content-Disposition: attachment trong HTTP response header, để không mở được file trực tiếp từ trình duyệt (cho hiển thị dowload dialog). | 1 |  |

## Monitoring log

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_logging_001` | Ít nhất, các log bắt buộc lưu theo checksheet thì phải lưu tối thiểu 5 năm được lưu giữ trong tối thiểu năm năm, trong đó các log của của 1 năm gần nhất ở trạng thái có thể truy xuất ngay lập tức. | 1 | O |
| `webapp_v2.2_logging_002` | Để tránh mất log do tấn công hoặc kết thúc auto-scaling, cần chuyển log từ server nơi sinh log sang storage bên ngoài ngay lập tức hoặc định kỳ. | 2 |  |
| `webapp_v2.2_logging_003` | Timezone của log cần được thống nhất trong toàn bộ hệ thống và đồng bộ với cùng một nhóm NTP server trong hệ thống. | 2 |  |
| `webapp_v2.2_logging_004` | Lưu access log. IP address nguồn gửi được ghi log phải là của node nguồn gửi thực tế (không phải của node trung gian như proxy...) | 2 |  |
| `webapp_v2.2_logging_005` | Lưu log monitoring database | 99 |  |
| `webapp_v2.2_logging_006` | Lưu log system liên quan security. ・/var/log/messages ・/var/log/secure ・/var/log/audit/*.log (trường hợp liên quan RHEL) | 2 |  |
| `webapp_v2.2_logging_007` | Lưu network flow log | 99 |  |
| `webapp_v2.2_logging_008` | Lưu DNS query log | 99 |  |
| `webapp_v2.2_logging_009` | Lưu log liên quan đến mail (chẳng hạn như /var/log/maillog cho postfix và sendmail trên CentOS). | 2 |  |
| `webapp_v2.2_logging_010` | Ghi lại các access vào thông tin xác thực và thông tin mật dưới dạng log ứng dụng. Log phải cho biết rõ thời điểm truy cập, người dùng nào thực hiện, và truy cập vào thông tin mật nào. | 2 |  |
| `webapp_v2.2_logging_011` | Để có thể truy vết lịch sử các thao tác đặc quyền như thao tác hệ thống, thay đổi phá hủy, truy cập thông tin mật bởi quản trị viên hệ thống (bao gồm cả nhà phát triển và người vận hành), cần lưu trữ log thao tác của system và flatform | 2 |  |
| `webapp_v2.2_logging_012` | Khi lưu log vào external storage, cần thực hiện mã hóa. Đặc biệt, đối với log chứa thông tin cá nhân, cần đảm bảo khả năng truy vết người đã giải mã và thời điểm giải mã. | 2 |  |

## Tổng quan system architecture

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_architecture_001` | Thiết lập cấu hình mạng, cơ chế xác thực và hạn chế sao cho chỉ cho phép lưu lượng inbound và outbound ở mức tối thiểu cần thiết đối với tất cả các máy chủ. | 1 |  |
| `webapp_v2.2_architecture_002` | Các server cấu thành hệ thống cần được triển khai trên các thiết bị phần cứng hoặc instance riêng biệt theo từng vai trò như Web, cơ sở dữ liệu, v.v. Không tạo server mang nhiều vai trò. | 2 |  |
| `webapp_v2.2_architecture_003` | Người dùng chạy ứng dụng, proccess thì chỉ được cấp quyền hạn ở mức tối thiểu cần thiết. | 1 |  |
| `webapp_v2.2_architecture_004` | Dừng hoặc un-instal các service (và port) không cần thiết, ngoài các service công khai và các service cần thiết cho hoạt động và quản lý. | 1 |  |
| `webapp_v2.2_architecture_005` | Sử dụng tường lửa mạng hoặc chức năng tường lửa máy chủ để từ chối giao tiếp với các dịch vụ không cần thiết ngoài các dịch vụ công cộng và dịch vụ cần thiết cho quản lý vận hành. | 1 | O |
| `webapp_v2.2_architecture_006` | Triển khai WAF và duy trì trạng thái có thể phòng ngừa các cuộc tấn công phổ biến vào ứng dụng web cũng như phòng ngừa các cuộc tấn công tương lai dựa trên chữ ký (signature). | 1 | O |
| `webapp_v2.2_architecture_007` | Triển khai IDS/IPS để ngăn chặn các cuộc tấn công phổ biến vào flatform và ngăn chặn các cuộc tấn công sử dụng chữ ký trong tương lai. Nếu IDS được triển khai, hãy hành động dựa trên nội dung được phát hiện. | 1 | O |

## Thể chế phát triển

### Quản lý nhà phát triển và nhà điều hành

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_ops_001` | Quyền hạn được cấp cho người dùng (như thao tác hệ thống hoặc thay đổi source code) phải được giới hạn ở mức tối thiểu cần thiết. | 1 |  |
| `ứng dụng web_v2.2_ops_002` | Việc cấp và thu hồi quyền thao tác hệ thống cho người dùng phải được thực hiện nhanh chóng ngay khi cần, đồng thời ghi lại lịch sử này trong BTS hoặc sổ nhật ký. | 1 |  |

### Quản lý sourcode và setting

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `ứng dụng web_v2.2_ops_003` | Những thay đổi đối với source code và system đang được quản lý bằng system quản lý source code hoặc BTS, dựa theo thủ tục thay đổi được xác định trước. | 2 |  |

## Monitoring

| Requirement ID | Yêu cầu | SL | Mục quan trọng |
|---|---|---|---|
| `webapp_v2.2_monitoring_001` | Định nghĩa trạng thái hệ thống ngưng hoạt động (không thể cung cấp dịch vụ) và giám sát để có thể phát hiện được trạng thái này. | 1 |  |
| `webapp_v2.2_monitoring_002` | Theo dõi để phát hiện sự gia tăng đột ngột về số lượng truy cập. | 2 |  |
| `webapp_v2.2_monitoring_003` | Giám sát để phát hiện hoạt động đặc quyền và phá hoại trong hệ thống (thêm, thay đổi hoặc xóa file hoặc setting) | 99 |  |

---

# Phần 3 — Ánh xạ giữa hai phần

| Tầng kỹ thuật (Phần 1) | Nhóm tương ứng trong checksheet khách (Phần 2) |
|---|---|
| **I · Network** | `3.4 TLS` |
| **II · Server configuration** | `4.1 Setting của Web server` · `HTTP security header` |
| **III · Deployment** | `4.4 môi trường phát triển` · `4.5 môi trường PROD` |
| **IV · Programming** — injection | `2.1 Database security` · `2.7 OS command` · `2.11`/`3.9 check input` · `2.15 include file` · `2.16 character code` · `2.17 Serialized Object` · `2.19 XML` · `2.20 SSTI` · `3.15 eval injection` |
| **IV · Programming** — hiển thị & client | `2.2 hiển thị màn hình (XSS, JSONP, CORS)` · `2.4 HTML5` · `2.10 redirect` |
| **IV · Programming** — xác thực & phiên | `Xác thực` · `Quản lý account` · `3.3`/`4.3 Authorization` · `2.12`/`3.10 session` · `2.6 CSRF` |
| **IV · Programming** — file | `2.8 access file` · `2.14`/`3.12 I/O file` |
| **IV · Programming** — khác | `2.5 liên kết external` · `2.9 email` · `2.13`/`3.11 error message` · `2.18`/`3.16 multi-thread` · `2.21 SSRF` · `3.6 thanh toán` · `3.7 quản lý khoá` · `4.6 bảo vệ thông tin cá nhân` |
| **V · Database** | `2.1 Database security` |
| **VI · Client browser/UI** | `2.2 hiển thị màn hình` · `2.13 error message` |
| *(không có trong Phần 1)* | `Monitoring log` (12) · `Monitoring` (3) · `Tổng quan system architecture` (7) · `Thể chế phát triển` (3) |

> **Bốn nhóm cuối bảng không có trong Phần 1** — giám sát log, giám sát hệ thống, tổng quan kiến trúc,
> và thể chế phát triển. Đây là vùng checklist kỹ thuật **chưa phủ**; task chạm tới thì lấy thẳng yêu cầu
> ở Phần 2 làm căn cứ.
