# Ví dụ output — `spec-analysis.md`

> File này là **few-shot** cho agent và mẫu đối chiếu cho người. Nội dung dưới đây là hư cấu, dùng một task nhỏ có thật về hình dạng: thêm một trường vào form ứng tuyển và sửa quy tắc validate số điện thoại.
>
> Chú ý ba chỗ hay bị làm sai, đã đánh dấu 👀 trong file.

---

# Spec Analysis — TICKET-4821

## 1 · Analysis Status

| | |
|---|---|
| **Status** | 🔴 **BLOCKED** |
| Loại | feature (change) |
| Lý do | Còn 2 `[BLOCKER]` — QA-01 và QA-03. Không chốt được thì không suy ra `expected` cho REQ-02 và REQ-04 |
| Nguồn đã đọc | `spec-4821.md` (v1.2) · `screen-detail-応募フォーム.pdf` · `tasks/TICKET-4821/current-state.md` · `impact.md` |
| Mức tin cậy | Trung bình — spec không mô tả miền giá trị của trường mới |

👀 **Trạng thái mặc định của một task chưa hỏi khách là `BLOCKED`, không phải `READY`.** Ghi `READY` khi còn BLOCKER là bỏ qua toàn bộ mục đích của bước này.

## 2 · Task Summary

| | |
|---|---|
| **Mục tiêu** | Ứng viên chọn được nơi làm việc mong muốn khi nộp đơn; đồng thời nới quy tắc số điện thoại để nhận số cố định |
| **Actor** | Ứng viên (chưa đăng nhập) |
| **Trigger → End-state** | Mở form ứng tuyển → điền → gửi → đơn lưu kèm nơi làm việc mong muốn |
| **In-scope** | Form ứng tuyển · validate phía client và server · lưu DB |
| **Out-of-scope** | Màn quản trị xem đơn (ticket khác) · email xác nhận |
| **Impact chính** | 1 màn hình sửa · 1 bảng DB thêm cột · validate dùng chung với 2 form khác — xem `impact.md` |

## 3 · Related Screens / Touchpoints

| Định danh | Vai trò | Entry | Action | Dependency | Trạng thái | Source |
|---|---|---|---|---|---|---|
| `応募フォーム` | Form chính | `/apply` | submit | `ApplicationValidator` | ⚠ update | screen-detail p.3 |
| `お問い合わせフォーム` | Không đụng trực tiếp | `/contact` | — | **dùng chung** `ApplicationValidator` | ⚠ **rủi ro lan** | `impact.md` |
| `確認画面` | Xem lại trước gửi | `/apply/confirm` | — | render lại field | ⚠ update | screen-detail p.5 |

👀 **Dòng thứ hai là thứ dependency walk sinh ra.** Spec không nhắc form liên hệ — nhưng nó dùng chung validator, nên sửa validate SĐT là đụng cả nó. Không có `impact.md` thì dòng này không tồn tại.

## 4 · Requirements

| REQ-ID | Screen | Requirement | Type | Delta | Maps to | Source | Conf. |
|---|---|---|---|---|---|---|---|
| REQ-01 | 応募フォーム | Form PHẢI có trường chọn nơi làm việc mong muốn | UI | `ADDED` | 🆕 | spec §2.1 | Explicit |
| REQ-02 | 応募フォーム | Nơi làm việc mong muốn PHẢI bắt buộc nhập | Validation | `ADDED` | 🆕 | — | **Open** |
| REQ-03 | 応募フォーム · お問い合わせ | Số điện thoại PHẢI chấp nhận số cố định 10 chữ số | Validation | `MODIFIED` | ⚠ | spec §3.2 | Explicit |
| REQ-04 | 確認画面 | Màn xác nhận PHẢI hiển thị nơi làm việc đã chọn | UI | `ADDED` | 🆕 | screen-detail p.5 | Explicit |

### Scenarios

```
### REQ-03 — Số điện thoại chấp nhận số cố định
Hệ thống PHẢI chấp nhận số điện thoại cố định 10 chữ số, ngoài số di động 11 chữ số.

#### Scenario: Số di động, 11 chữ số
- WHEN nhập "09012345678"
- THEN hợp lệ, cho gửi

#### Scenario: Số cố định, 10 chữ số
- WHEN nhập "0312345678"
- THEN hợp lệ, cho gửi        ← hành vi MỚI, trước đây báo lỗi

#### Scenario: Độ dài không thuộc hai nhóm trên
- WHEN nhập "012345"
- THEN báo lỗi định dạng số điện thoại

#### Scenario: Nhập bằng chữ số full-width
- WHEN nhập "０９０１２３４５６７８"
- THEN ???                     ← [BLOCKER] QA-03, xem section 6
```

👀 **REQ-02 không có scenario nào** vì spec không nói bắt buộc hay không. Nó nằm trong bảng với `Source: —` và `Conf: Open` — **không được** viết đại một scenario để bảng trông đầy đủ.

`MODIFIED` ở REQ-03 phải ghi **đủ** hành vi mới, gồm cả phần không đổi (số di động 11 chữ số). Ghi mỗi phần thêm vào thì người đọc sau tưởng số di động bị bỏ.

## 5 · Input Contract 🆕

| Tham số / Field | Kiểu | Miền hợp lệ | Bắt buộc | Giá trị đặc biệt | Nguồn | Conf. |
|---|---|---|---|---|---|---|
| `preferredLocation` | string | 1 trong 47 都道府県 | **???** | rỗng: ??? | spec §2.1 *(chỉ liệt kê danh sách, không nói bắt buộc)* | **Open** |
| `phoneNumber` | string | 10 **hoặc** 11 chữ số | có | rỗng → lỗi bắt buộc | spec §3.2 | Explicit |
| `phoneNumber` | — | **≤ 20 ký tự** | — | — | `applications.phone varchar(20)` | Explicit |
| `applicantName` | string | **≤ 50 ký tự** | có | toàn khoảng trắng → lỗi | `applications.name varchar(50)` | Explicit |
| `email` | string | RFC 5322 + domain bất kỳ | có | — | API contract `POST /applications` `format: email` | Explicit |
| `attachments` | list | 0–3 file, mỗi file ≤ 5 MB | không | **danh sách rỗng hợp lệ** | spec §4.1 | Explicit |

**Ghi chú nguồn:**

- `phoneNumber` có **hai** dòng vì hai ràng buộc đến từ hai nguồn khác nhau — spec cho *định dạng*, schema DB cho *độ dài tối đa*. Cả hai đều phải test.
- `applicantName ≤ 50` **không có trong spec**, chỉ có trong schema. Đây là loại ràng buộc hay bị bỏ sót nhất, và là chỗ bug tràn dữ liệu hay xảy ra.

👀 **Chỗ dễ sai nhất:** trong code hiện có `ApplicationValidator::PHONE_MAX = 15`. Con số đó **không** được đưa vào bảng này như một ràng buộc — nó lệch với `varchar(20)` của DB, và lệch đó chính là **QA-02**. Lấy 15 làm miền hợp lệ là chép lại một quy tắc có thể đang sai.

## 6 · Open Questions / Conflicts

| QA-ID | Level | Issue | Source A | Source B / Code-reality | Impact | Câu hỏi cho khách |
|---|---|---|---|---|---|---|
| **QA-01** | 🔴 BLOCKER | Nơi làm việc mong muốn bắt buộc hay không | spec §2.1 chỉ liệt kê 47 tỉnh, không nói bắt buộc | screen-detail p.3 **có dấu 必須** | Đổi REQ-02, đổi cả validate client lẫn server | Trường này bắt buộc nhập hay được để trống? |
| **QA-02** | 🟡 CLARIFY | Độ dài tối đa SĐT lệch nhau | `applications.phone varchar(20)` | `ApplicationValidator::PHONE_MAX = 15` | Số 16–20 ký tự: DB nhận, code chặn | Giới hạn đúng là bao nhiêu — 15 hay 20? |
| **QA-03** | 🔴 BLOCKER | Chữ số full-width `０９０…` xử lý ra sao | Không tài liệu nào nói | Code hiện tại **không** convert → báo lỗi | Người dùng Nhật gõ IME hay ra full-width. Ảnh hưởng tỉ lệ gửi đơn thành công | Có tự chuyển full-width sang half-width trước khi validate không? |
| **QA-04** | 🟡 CLARIFY | Sửa validate SĐT lan sang form liên hệ | `impact.md` — dùng chung `ApplicationValidator` | — | Form liên hệ cũng nhận số cố định, không rõ có mong muốn không | Form liên hệ có nên đổi theo không, hay tách rule riêng? |

👀 **QA-02 và QA-03 là hai loại conflict khác nhau, xử lý khác nhau:**

- **QA-01 là doc ⟷ doc.** Hai tài liệu nói khác nhau. Screen detail ưu tiên hơn spec chung, **nhưng** vì ảnh hưởng hành vi nên vẫn để BLOCKER, không tự chọn bên.
- **QA-02 là doc ⟷ code.** Không phân xử bằng ưu tiên. Ghi cả hai phía kèm nguồn, để khách quyết. `varchar(20)` không "thắng" chỉ vì nó là DB.
- **QA-03 là gap thật** — không bên nào nói gì. Đây là loại câu hỏi mà không chạy analyze-spec thì sẽ phát hiện lúc đang code, hoặc tệ hơn: lúc user Nhật gửi đơn thất bại.

---

## Đối chiếu nhanh trước khi báo xong

- [ ] Mọi requirement có **≥1 scenario `WHEN…THEN`**, hoặc nằm ở `Open` với `Source: —`
- [ ] Mọi dòng Input Contract có **nguồn**, và nguồn đó **không phải rule validate trong code**
- [ ] `MODIFIED` ghi **đủ** hành vi mới, không chỉ phần thêm
- [ ] Conflict **doc ⟷ code** ghi cả hai phía, không tự phân xử
- [ ] Còn `[BLOCKER]` → Status là **BLOCKED**
- [ ] Task không đổi hành vi → ghi *"không đổi hành vi"*, **không** nặn requirement giả
