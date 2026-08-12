---
name: security-check
description: >-
  Security gate and audit for ANY project, driven by the company's own checklists — a 74-item
  engineering checklist (network · server config · deployment · programming · database · client UI) and
  the 153-requirement customer web-application checksheet — plus an OWASP quick reference. Two
  modes: TASK mode triages what one change actually touches and writes 01-discovery/security.md (cheap,
  runs on every task that touches auth, data, secrets, uploads, infra or external calls); AUDIT mode
  answers the full checklists for a release or customer submission and writes
  05-delivery/security-checklist-<date>.md. Trigger on "check bảo mật", "security review/checklist",
  "rà an ninh", "điền checksheet bảo mật", "task này có rủi ro bảo mật gì", or as the security gate of
  analyze-spec. Locale vn (default) / en / ja.
---

# Security Check — cổng bảo mật theo checklist

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

> Ngôn ngữ giao tiếp: tiếng Việt. Output theo `locale` (mặc định vn). Gõ `security-check help` → in Help cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — AI dò checklist, đối chiếu code và soạn nháp; **kết luận "mục này đạt / không áp dụng" là của người phụ trách**. Một dòng "N/A" sai trong checksheet gửi khách đắt hơn nhiều so với một dòng "chưa kiểm".

## Hai tầng — đừng lẫn

| | **TASK mode** | **AUDIT mode** |
|---|---|---|
| Câu hỏi | *thay đổi này đụng vào đâu về mặt bảo mật?* | *cả hệ thống có đạt checklist không?* |
| Phạm vi | 1 task / 1 PR | 1 release / 1 hệ thống |
| Chi phí | 10–20 phút | nửa buổi → 1 ngày |
| Output | `01-discovery/security.md` | `05-delivery/security-checklist-<yyyymmdd>.md` |
| Khi nào | **mỗi task** chạm 6 tín hiệu bên dưới | trước release lớn · khách yêu cầu · định kỳ |
| Gọi từ | `analyze-spec` (tự động) | người gọi tay |

**Vì sao tách:** chạy 153 requirement cho một task sửa CSS là lãng phí và sẽ bị bỏ qua sau vài lần. Ngược lại, chỉ làm audit định kỳ thì mọi thay đổi giữa hai kỳ audit không ai soi. Cần cả hai, ở hai nhịp khác nhau.

## TASK mode

### Bước 1 — Có cần chạy không (6 tín hiệu)

Chạy nếu task chạm **ít nhất một**:

1. **Xác thực / phân quyền** — đăng nhập, session, token, vai trò, ai xem được gì
2. **Dữ liệu nhạy cảm** — thông tin cá nhân, thanh toán, mật khẩu, secret, khoá
3. **Input từ ngoài** — form, query param, API nhận request, import file
4. **File** — upload, download, đường dẫn file trên URL
5. **Hạ tầng / cấu hình** — port, IAM, biến môi trường, header, CORS, deploy
6. **Phụ thuộc ngoài** — thư viện mới/nâng version, API bên thứ ba, webhook

Không chạm mục nào → ghi vào `technical-approach.md` §3: **"không đụng bảo mật"** kèm lý do, **không** tạo `security.md` rỗng.

### Bước 2 — Triage: lọc checklist xuống phần liên quan

Từ tín hiệu ở Bước 1 → mở đúng mục trong [`reference/checklist.md`](reference/checklist.md):

| Tín hiệu | Phần 1 — tầng kỹ thuật | Phần 2 — nhóm yêu cầu khách |
|---|---|---|
| Xác thực / phân quyền | IV · Authentication/Authorization, Session, Cookie | `Xác thực`, `3.3/4.3 Authorization`, `2.12/3.10 session` |
| Dữ liệu nhạy cảm | IV · Privacy, Encryption, Handling sensitive information | `3.4 TLS`, `3.7 Quản lý khoá`, `4.6 Bảo vệ thông tin cá nhân` |
| Input từ ngoài | IV · SQL Injection, XSS, OS Command Injection | `2.1 db`, `2.2 display`, `2.7 OS command`, `2.11/3.9 check input` |
| File | IV · Directory Traversal, User files | `2.8 access file`, `2.14/3.12 I/O file` |
| Hạ tầng / cấu hình | I · Network · II · Server config · III · Deployment | `4.1 Web server`, `HTTP security header`, `4.4/4.5 môi trường` |
| Phụ thuộc ngoài | IV · Common (mục 30) | `2.5 liên kết external`, `2.21 SSRF` |

Chỉ lấy **các mục thực sự liên quan**. Mục không liên quan **không** cần trả lời — nhưng phải nói rõ đã loại nhóm nào và vì sao.

### Bước 3 — Trả lời từng mục, có evidence

````markdown
# Security — {task}

> Tín hiệu kích hoạt: {liệt kê} · Nguồn: `01-discovery/current-state.md` · `impact.md`
> Checklist đối chiếu: `checklist.md` Phần 1 §{tầng} · Phần 2 §{nhóm}

## Kết luận
{1–3 câu: task này có rủi ro bảo mật nào, đã xử lý thế nào, còn gì phải quyết}

## Bảng đối chiếu
| Mục | Nguồn | Trạng thái | Evidence / Lý do |
|---|---|---|---|
| Input validate ở đâu | P1 #55, #58 | ✅ Đạt | `FormRequest::rules()` `app/Http/Requests/X.php:24` |
| Quyền xem dữ liệu người khác | P1 #31 | ⚠ Cần làm | chưa kiểm `user_id` — thêm vào ticket 3 |
| Upload file | P1 #65–67 | ➖ Không áp dụng | task không có upload |

## Rủi ro còn lại
| Rủi ro | Mức | Xử lý ở đâu |
|---|---|---|

## Việc phải làm — đưa vào ticket
- [ ] {việc} → ticket {NN}
````

**Bốn trạng thái, không có trạng thái thứ năm:** `✅ Đạt` (có evidence) · `⚠ Cần làm` (→ phải thành checkbox trong ticket) · `➖ Không áp dụng` (kèm lý do) · `❓ Chưa kiểm được` (kèm cách kiểm). **Bỏ trống không phải câu trả lời.**

### Bước 4 — Đẩy ngược vào ticket

Mọi dòng `⚠ Cần làm` phải xuất hiện ở **`Implementation content`** của ticket tương ứng và **`Completion condition`** dạng kiểm được. Nằm mãi trong `security.md` thì không ai làm.

## AUDIT mode

Trả lời **toàn bộ** checklist cho một release/hệ thống.

1. **Chọn phần**: rà nội bộ → [`checklist.md`](reference/checklist.md) **Phần 1** (74 mục theo tầng). Nộp cho khách → **Phần 2** (153 requirement, **giữ nguyên `Requirement ID`, không gộp dòng**).
2. **Chia theo người chịu trách nhiệm** — Phần 1 có sẵn cột: `Devops/Techlead` (hạ tầng) vs `Engineer` (code). Không gộp: hai người trả lời hai phần khác nhau.
3. **Mục bắt buộc ✓ không đạt = blocker**, phải có kế hoạch xử lý kèm ngày, không được ghi "sẽ làm sau".
4. **Mọi câu trả lời cần evidence**: đường dẫn file · cấu hình · ảnh chụp · lệnh verify. Trả lời "Có" không kèm gì là **chưa trả lời**.
5. Ghi `tasks/{ID}/05-delivery/security-checklist-<yyyymmdd>.md`; bản gửi khách export sang xlsx theo template gốc (**copy file mẫu rồi ghi theo dòng**, đừng dựng lại layout).

## Nguồn tham chiếu

| File | Dùng khi |
|---|---|
| [`reference/checklist.md`](reference/checklist.md) | **nguồn rule chính** — Phần 1: 74 mục kỹ thuật theo tầng · Phần 2: 153 requirement khách (ID cố định) · Phần 3: ánh xạ hai bên |
| [`reference/owasp.md`](reference/owasp.md) | tra nhanh theo loại lỗ hổng; task dùng LLM/agent → mục AST |

## Guardrails

- **[HARD] Không đánh dấu ✅ nếu chưa mở code/cấu hình xác nhận.** Suy từ "framework chắc có middleware" là đoán, không phải evidence — mục #57, #59, #64 hỏi đúng câu đó và câu trả lời phải là *đã kiểm thấy nó bật*.
- **[HARD] Không đưa secret thật vào file.** Trích dẫn tên biến/đường dẫn, không dán giá trị. `security.md` nằm trong repo.
- **[HARD] Không tự ý sửa cấu hình bảo mật đang chạy** trong lúc rà — ghi phát hiện, để người có thẩm quyền quyết.
- Không copy checklist vào `security.md` rồi tick hết — chỉ đưa mục **liên quan**, mỗi mục một câu trả lời riêng.
- Không dùng skill này thay cho pentest. Nó là **lưới của người làm**, không phải kiểm định độc lập.

## Help

```
security-check [task|audit] <TICKET-ID> [locale=vn|en|ja]
  task  (mặc định) — triage 1 thay đổi → 01-discovery/security.md. Chạy khi task chạm 1 trong 6 tín hiệu:
                     xác thực/phân quyền · dữ liệu nhạy cảm · input ngoài · file · hạ tầng · phụ thuộc ngoài.
  audit           — trả lời toàn bộ checklist cho release/hệ thống → 05-delivery/security-checklist-<date>.md.
  Nguồn rule: reference/checklist.md (74 mục kỹ thuật + 153 requirement khách + ánh xạ) · reference/owasp.md.
  Mọi ⚠ Cần làm phải đẩy ngược thành checkbox trong ticket — không để nằm lại trong file.
```
