# Danh sách Quan điểm viết Unit Test

## Mục lục

- [Vị trí trong quy trình kiểm thử](#vị-trí-trong-quy-trình-kiểm-thử)
- [Cơ sở phương pháp](#cơ-sở-phương-pháp)
- [Cách đọc tài liệu](#cách-đọc-tài-liệu)
- [Checklist quan điểm](#checklist-quan-điểm)
  - [A. Phân vùng tương đương (Equivalence Partitioning)](#a-phân-vùng-tương-đương-equivalence-partitioning)
  - [B. Giá trị biên (Boundary Value Analysis)](#b-giá-trị-biên-boundary-value-analysis)
  - [C. Độ phủ theo cấu trúc code (Branch + Condition Coverage)](#c-độ-phủ-theo-cấu-trúc-code-branch--condition-coverage)
  - [D. Ngoại lệ, phụ thuộc & tác dụng phụ (Exception & Interaction)](#d-ngoại-lệ-phụ-thuộc--tác-dụng-phụ-exception--interaction)
  - [E. Chuyển trạng thái & yếu tố không tất định](#e-chuyển-trạng-thái--yếu-tố-không-tất-định)
  - [F. Logic đặc thù theo domain (locale Nhật & nghiệp vụ)](#f-logic-đặc-thù-theo-domain-locale-nhật--nghiệp-vụ-dự-án)
- [Phụ lục A — Chuẩn chất lượng test code](#phụ-lục-a--chuẩn-chất-lượng-test-code)
- [Phụ lục B — Quan điểm từ bug lịch sử](#phụ-lục-b--quan-điểm-từ-bug-lịch-sử-cần-bổ-sung-theo-hiện-trạng)
- [Cách sử dụng & vận hành](#cách-sử-dụng--vận-hành)

---

## Vị trí trong quy trình kiểm thử

Quy trình Unit Test gồm 4 bước: **(1)** Kế hoạch test → **(2) Thiết kế UT – Quan điểm kiểm thử** → **(3)** Thiết kế UT – Mã test → **(4)** Thực thi UT.

- **Tài liệu này phục vụ bước (2)** — sản phẩm bàn giao là *danh sách quan điểm kiểm thử*: tổ chức quan điểm cho case bình thường / bất thường / giá trị biên, điều kiện rẽ nhánh, xử lý ngoại lệ, biến thể đầu vào; rà mục thiếu–trùng; quản lý dạng danh sách.
- **Bước (3) – Mã test**: chuyển mỗi quan điểm thành test chạy được → **Phụ lục A** của file này là chuẩn chất lượng cho bước đó.
- **Yêu cầu review** mỗi bước (bắt buộc / tùy chọn) do **Ma trận Yêu cầu Review** quyết định theo loại dự án.

## Cơ sở phương pháp

| Nguồn | Dùng cho phần nào |
| --- | --- |
| ISO/IEC/IEEE 29119-4, ISTQB Foundation | Tên gọi & định nghĩa kỹ thuật thiết kế test (EP, BVA, Decision Table, State Transition, Error Guessing) — nhóm A, B, D, E |
| Tiêu chí độ phủ cấu trúc code (branch + condition coverage) | Quan điểm độ phủ theo cấu trúc code — nhóm C |
| Nguyên tắc FIRST (Clean Code), mẫu AAA, xUnit Test Patterns (Meszaros) | Chuẩn chất lượng test code — Phụ lục A |
| Bug lịch sử của dự án | Error Guessing — nhóm E và Phụ lục B (cần bổ sung, xem Phụ lục B) |
| Spec dự án + điểm nóng locale Nhật *(chắt lọc từ dòng U của checklist Tester)* | Logic đặc thù domain — nhóm F |

---

## Cách đọc tài liệu

- Mỗi quan điểm là **một dòng ☐** để tự kiểm khi thiết kế test.
- Kèm theo mỗi quan điểm là **một kịch bản mẫu** viết theo dạng **Given – When – Then** (bằng lời) để hiểu ý, **không phải code**:
  - **Given** — bối cảnh / dữ liệu đầu vào đã cho.
  - **When** — hành động (gọi hàm đang test).
  - **Then** — kết quả kỳ vọng cần khẳng định (assert).
- Các ví dụ dùng vài hàm giả định xuyên suốt cho dễ theo dõi:
  - `validateAge(age)` — tuổi hợp lệ trong khoảng **18–120**.
  - `calcShippingFee(order)` — tính phí giao hàng theo quy tắc nghiệp vụ.
  - `parseDate(text)` — phân tích chuỗi ngày.
  - `orderState` — máy trạng thái đơn hàng: `DRAFT → CONFIRMED → SHIPPED → DELIVERED`.

---

## Checklist quan điểm

> **A→E** áp dụng cho **mọi** hàm/module viết UT. **F** chỉ áp dụng khi hàm chạm đúng loại logic đặc thù tương ứng.

### A. Phân vùng tương đương (Equivalence Partitioning)

Chia miền đầu vào thành các **vùng cho cùng một hành vi**; mỗi vùng chỉ cần **1 đại diện**.

**☐ A1 — Luồng chính (happy path) có ít nhất 1 test.** Case đại diện cho hành vi đúng.
> **Ví dụ** — `validateAge`
> - **Given** tuổi = 25 (nằm trong vùng hợp lệ 18–120)
> - **When** gọi `validateAge(25)`
> - **Then** trả về `hợp lệ`, không phát sinh lỗi

**☐ A2 — Mỗi vùng input *hợp lệ* có ít nhất 1 case.** Không cần test mọi giá trị trong cùng một vùng.
> **Ví dụ** — `calcShippingFee` có 2 bậc giá: đơn < 500k tính phí, đơn ≥ 500k miễn phí
> - **Given** đơn hàng 300.000đ (vùng "có phí") và một đơn 600.000đ (vùng "miễn phí")
> - **When** gọi `calcShippingFee` cho từng đơn
> - **Then** đơn 300k trả phí > 0; đơn 600k trả phí = 0 (mỗi vùng 1 đại diện là đủ)

**☐ A3 — Mỗi vùng input *không hợp lệ* có ít nhất 1 case.** Sai kiểu, sai định dạng, ngoài miền giá trị.
> **Ví dụ** — `validateAge`
> - **Given** tuổi = -5 (số âm) và tuổi = "abc" (sai kiểu)
> - **When** gọi `validateAge` cho từng giá trị
> - **Then** cả hai đều trả về `không hợp lệ` (mỗi loại lỗi 1 đại diện)

### B. Giá trị biên (Boundary Value Analysis)

Lỗi hay nằm ở **rìa vùng**. Với mỗi biên, kiểm cả giá trị **ngay trong** và **ngay ngoài**.

**☐ B1 — Biên min / max và min−1 / max+1.** Áp cho số, độ dài chuỗi, kích thước danh sách.
> **Ví dụ** — `validateAge` (hợp lệ 18–120)
> - **Given** lần lượt các tuổi 17, 18, 120, 121
> - **When** gọi `validateAge` cho từng giá trị
> - **Then** 17 → không hợp lệ; 18 → hợp lệ; 120 → hợp lệ; 121 → không hợp lệ

**☐ B2 — Giá trị 0, rỗng, `null` / `undefined`.** Phân biệt rỗng và null nếu ngôn ngữ có.
> **Ví dụ** — `calcShippingFee`
> - **Given** đơn hàng có tổng tiền = 0 và một tham số đơn hàng = `null`
> - **When** gọi `calcShippingFee`
> - **Then** đơn 0đ xử lý theo spec (ví dụ vẫn tính phí); đơn `null` ném lỗi rõ ràng, không crash

**☐ B3 — Chuỗi: rỗng, chỉ khoảng trắng, độ dài tối đa, ký tự đặc biệt / đa byte** (Kanji 4-byte, emoji).
> **Ví dụ** — trường tên (tối đa 50 ký tự)
> - **Given** chuỗi rỗng "", chuỗi 3 dấu cách "   ", chuỗi đúng 50 ký tự, chuỗi 51 ký tự, và tên chứa emoji "😀"
> - **When** validate trường tên
> - **Then** rỗng & toàn dấu cách → lỗi bắt buộc; 50 ký tự → hợp lệ; 51 → lỗi độ dài; emoji đếm đúng độ dài (không vỡ ở surrogate pair)

**☐ B4 — Collection: rỗng, 1 phần tử, nhiều phần tử, có phần tử trùng lặp.**
> **Ví dụ** — `calcShippingFee` cộng phí theo danh sách mặt hàng
> - **Given** giỏ hàng rỗng, giỏ 1 món, giỏ nhiều món, và giỏ có 2 món trùng mã
> - **When** gọi `calcShippingFee`
> - **Then** giỏ rỗng → phí 0 (hoặc lỗi theo spec); các trường hợp còn lại tính đúng tổng, không nhân đôi nhầm món trùng

### C. Độ phủ theo cấu trúc code (Branch + Condition Coverage)

Bảo đảm **mọi nhánh** trong code đều được đi qua với cả hai kết quả.

> **Coverage là sàn, không phải mục tiêu:** đạt 100% branch **không** chứng minh code đúng. Độ phủ chỉ đảm bảo *đã đi qua* nhánh, không đảm bảo *đã kiểm đúng kết quả* — tránh viết test chỉ để "xanh" mà assertion rỗng/yếu.

**☐ C1 — Branch coverage.** Mỗi nhánh `if/else`, `switch`, early return, ternary, vòng lặp (đi vào / bỏ qua) đều lấy cả `true` và `false`. *Statement coverage không đủ.*
> **Ví dụ** — `calcShippingFee` có `if (order.isVip) fee = 0;`
> - **Given** một đơn của khách VIP và một đơn của khách thường
> - **When** gọi `calcShippingFee` cho từng đơn
> - **Then** VIP → phí 0 (nhánh true); thường → phí theo bậc (nhánh false) — cả 2 nhánh đều được chạy

**☐ C2 — Condition coverage.** Với điều kiện phức hợp (`&&`, `||`), mỗi điều kiện con nguyên tử phải nhận cả `true` lẫn `false` ít nhất 1 lần.
> **Ví dụ** — `if (isVip && orderTotal >= 500000)` miễn phí
> - **Given** 4 tổ hợp: (VIP, đủ tiền) / (VIP, thiếu tiền) / (thường, đủ tiền) / (thường, thiếu tiền)
> - **When** gọi hàm cho các tổ hợp
> - **Then** mỗi biến `isVip` và `orderTotal >= 500000` đều đã từng nhận cả true lẫn false

**☐ C3 — Đạt đồng thời C1 + C2 (tức Branch + Condition = C/DC).** ⚠️ Condition coverage **không** tự bao hàm Branch coverage — đây là lý do phải yêu cầu **cả hai**, không dùng cái này thay cái kia.
> **Ví dụ cảnh báo** — `if (A || B)`
> - **Given** chỉ 2 case: (A=true, B=false) và (A=false, B=true)
> - **Then** đã thỏa condition coverage (mỗi biến từng true/false) **nhưng** nhánh **luôn = true** → bỏ sót nhánh `false`. Phải thêm case (A=false, B=false) để phủ nhánh false (đạt Branch coverage).

**☐ C4 — Điều kiện kết hợp: lập bảng quyết định (decision table) và phủ các tổ hợp có ý nghĩa.** Không cần phủ tổ hợp bất khả thi — ghi rõ lý do loại.
> **Ví dụ** — phí = f(hạng khách × phương thức giao)
>
> | Hạng khách | Giao nhanh? | Phí kỳ vọng |
> | --- | --- | --- |
> | VIP | Có | 0 |
> | VIP | Không | 0 |
> | Thường | Có | 50.000 |
> | Thường | Không | 30.000 |
>
> - **Given** từng dòng trong bảng
> - **When** gọi `calcShippingFee`
> - **Then** kết quả khớp cột "Phí kỳ vọng" của dòng tương ứng

> **Lưu ý short-circuit:** với `&&` / `||`, khi vế trái đã quyết định kết quả thì vế phải **không được đánh giá** (ví dụ `A=false` thì `A && B` bỏ qua B). Cần thiết kế dữ liệu để mỗi điều kiện con **thực sự được đánh giá tới**, nếu không condition coverage chỉ đạt trên giấy.

### D. Ngoại lệ, phụ thuộc & tác dụng phụ (Exception & Interaction)

Kiểm hành vi khi có lỗi và cách hàm **tương tác với phụ thuộc** — không chỉ khi mọi thứ suôn sẻ.

**☐ D1 — Throw đúng *loại* exception, đúng message / error code.**
> **Ví dụ** — `parseDate`
> - **Given** chuỗi "2026-13-40" (tháng/ngày không tồn tại)
> - **When** gọi `parseDate`
> - **Then** ném `InvalidDateException` với message chỉ rõ trường sai — không trả về ngày rác, không ném lỗi chung chung

**☐ D2 — Cleanup / rollback chạy đúng sau khi lỗi xảy ra.** Resource được giải phóng, trạng thái không bị bỏ dở nửa chừng.
> **Ví dụ** — hàm ghi đơn hàng có mở transaction
> - **Given** thao tác ghi bước 2 ném lỗi (đã mock)
> - **When** gọi hàm lưu đơn
> - **Then** transaction được rollback, không còn bản ghi dở; kết nối/khóa được đóng

**☐ D3 — Lỗi từ dependency (I/O, API, DB đã mock) được xử lý đúng.** Mock trả lỗi / timeout và xác nhận hành vi của hàm đang test.
> **Ví dụ** — `calcShippingFee` gọi service tra cứu vùng giao hàng
> - **Given** service (đã mock) trả timeout
> - **When** gọi `calcShippingFee`
> - **Then** hàm trả lỗi có kiểm soát hoặc dùng giá trị mặc định theo spec — không treo, không nuốt lỗi im lặng

**☐ D4 — Kiểm chứng tương tác (interaction).** Không chỉ kiểm giá trị trả về — xác nhận collaborator (đã mock) được gọi **đúng hàm, đúng tham số, đúng số lần**. Quan trọng nhất với hàm `void` / side-effect (gọi API, emit event, ghi DB) vì không có return value để assert.
> **Ví dụ** — `checkout(order)` gọi `paymentGateway.charge(amount)`
> - **Given** đơn 500.000đ, `paymentGateway` đã mock
> - **When** gọi `checkout(order)`
> - **Then** `charge` được gọi **đúng 1 lần** với tham số 500000 — không 0 lần, không 2 lần

**☐ D5 — Idempotency / retry.** Gọi lại hàm hoặc retry sau timeout **không** nhân đôi tác dụng phụ.
> **Ví dụ** — `submitOrder(id)` bị retry sau timeout mạng
> - **Given** đơn `id` đã tạo thành công ở lần gọi đầu (nhưng client timeout, không nhận được response)
> - **When** client retry `submitOrder(id)`
> - **Then** không tạo đơn thứ 2 (nhận diện qua idempotency key) — chỉ 1 đơn tồn tại

### E. Chuyển trạng thái & yếu tố không tất định

**☐ E1 — State machine: phủ các chuyển trạng thái hợp lệ và ít nhất 1 chuyển không hợp lệ** (State Transition Testing).
> **Ví dụ** — `orderState`: `DRAFT → CONFIRMED → SHIPPED → DELIVERED`
> - **Given** đơn ở trạng thái `SHIPPED`
> - **When** gọi hành động `cancel()` (chỉ cho phép ở `DRAFT`/`CONFIRMED`)
> - **Then** bị từ chối với lỗi "không thể hủy đơn đã giao vận"; đơn giữ nguyên `SHIPPED` (đồng thời vẫn có các case chuyển hợp lệ DRAFT→CONFIRMED… được test)

**☐ E2 — Test không phụ thuộc thời gian thực, random, thứ tự chạy.** Cố định clock/seed qua injection — xem Phụ lục A. Nếu logic phụ thuộc ngày-giờ, test thêm **múi giờ / DST / mốc nửa đêm** (vd JST ↔ UTC làm lệch "hôm nay").
> **Ví dụ** — hàm gắn hạn thanh toán = ngày hiện tại + 7
> - **Given** clock được inject cố định ở "2026-07-01"
> - **When** gọi hàm tạo hạn thanh toán
> - **Then** luôn trả "2026-07-08" ở mọi máy, mọi thời điểm chạy (không dùng `DateTime.now()` trực tiếp)

**☐ E3 — Đối chiếu danh mục bug lịch sử (Error Guessing).** Có quan điểm nào ở Phụ lục B áp cho hàm này không?
> **Ví dụ** — nếu Phụ lục B ghi "từng lỗi làm tròn .5 sai chiều"
> - **Given** số tiền 100,5 với quy tắc làm tròn nửa lên
> - **When** gọi hàm định dạng tiền
> - **Then** ra 101 (thêm đúng case biên .5 mà bug cũ từng bỏ sót)

**☐ E4 — Bất định do đồng thời (async / concurrency).** Với hàm async (Future/Stream) hoặc có shared state: test các thứ tự hoàn thành khác nhau, gọi đồng thời nhiều lần, và race trên trạng thái dùng chung.
> **Ví dụ** — `loadProfile()` ghi kết quả vào cache dùng chung
> - **Given** 2 lời gọi `loadProfile()` chạy đồng thời, response B trả về trước response A
> - **When** cả hai cùng ghi vào cache
> - **Then** cache giữ kết quả nhất quán (không ghi đè sai thứ tự, không mất cập nhật)

### F. Logic đặc thù theo domain (locale Nhật & nghiệp vụ dự án)

> **Khác A→E:** A→E áp dụng cho **mọi** hàm. **F là danh mục "trigger"** — chỉ áp dụng **khi** hàm chạm đúng loại logic tương ứng: thấy hàm làm việc X thì nhớ các bẫy Y (rồi áp dụng lại kỹ thuật A→E lên chúng). Nguồn: **spec dự án + điểm nóng locale/nghiệp vụ hay lặp lại**, thay cho việc dev phải tự nhớ.

**☐ F1 — Chuẩn hóa / trim chuỗi.** Khoảng trắng **full-width（　）lẫn half-width** ở đầu/cuối; có / không convert **full ↔ half** theo spec từng trường.
> **Ví dụ** — `normalizeInput`
> - **Given** tên "　山田　" (khoảng trắng full-width 2 đầu) và "ＡＢＣ" (chữ full-width)
> - **When** gọi `normalizeInput`
> - **Then** trim cả full-width lẫn half-width → "山田"; nếu spec yêu cầu convert thì "ＡＢＣ" → "ABC", nếu không thì giữ nguyên

**☐ F2 — So khớp / chuyển đổi kana.** Chuẩn hóa **Hiragana ↔ Katakana**; sinh / tách **furigana** nếu có.
> **Ví dụ** — `matchKana`
> - **Given** người dùng search "やまだ" (Hiragana), dữ liệu lưu "ヤマダ" (Katakana)
> - **When** chuẩn hóa kana rồi so khớp
> - **Then** hai chuỗi được coi là khớp (không phân biệt Hiragana/Katakana)

**☐ F3 — Sort / compare chuỗi Nhật.** Thứ tự **gojūon**, **dakuten / handakuten**, trộn full/half trong cùng danh sách; ổn định khi giá trị bằng nhau.
> **Ví dụ** — `sortByKana`
> - **Given** danh sách ["さ", "ざ", "か", "が"]
> - **When** sort theo gojūon
> - **Then** thứ tự đúng "か" → "が" → "さ" → "ざ" (dakuten xếp ngay sau ký tự gốc)

**☐ F4 — Ngày (parse / format / tính).** **Niên hiệu (era) ↔ dương lịch** & thời điểm giao era; biên 29/2, cuối tháng, cuối năm, năm nhuận *(áp dụng B)*.
> **Ví dụ** — `formatEraDate`
> - **Given** ngày 2019-05-01 (đúng ngày đổi Heisei → Reiwa)
> - **When** gọi `formatEraDate("2019-05-01")`
> - **Then** trả "令和元年5月1日", **không** phải "平成31年…" (đúng thời điểm giao era)

**☐ F5 — Tiền yên / số học tiền.** **Làm tròn .5** đúng chiều, dấu phân cách nghìn, số thập phân, số âm *(áp dụng B)*.
> **Ví dụ** — `formatYen`
> - **Given** 100,5 yên với quy tắc làm tròn nửa lên
> - **When** gọi `formatYen(100.5)`
> - **Then** ra "¥101" (case biên .5 mà bug cũ hay sai chiều)

**☐ F6 — Đếm độ dài chuỗi.** **dakuten / handakuten**, **surrogate pair** (Kanji 4-byte, emoji) *(đã nêu ở B3)*.
> **Ví dụ** — `countChars`
> - **Given** "が" (kana + dakuten), "𩸽" (Kanji 4-byte) và "😀" (emoji)
> - **When** gọi `countChars`
> - **Then** đếm đúng số ký tự hiển thị theo spec — không tính surrogate pair thành 2, không tách dakuten

**☐ F7 — Validate định dạng theo rule dự án.** SĐT & email theo **rule TechTus** (vd chỉ `@mynavitechtus.com`); **thứ tự ưu tiên thông báo** khi vi phạm nhiều rule cùng lúc.
> **Ví dụ** — `validateEmail`
> - **Given** "a@mynavitechtus.com", "a@gmail.com" (sai domain), "abc" (thiếu @ — vi phạm cả định dạng lẫn domain)
> - **When** gọi `validateEmail`
> - **Then** case 1 hợp lệ; case 2 lỗi domain; case 3 báo **đúng rule ưu tiên trước** (định dạng trước domain)

**☐ F8 — Auto-fill từ mã bưu chính.** Case **tìm thấy / không tìm thấy / lỗi API** (mock master data).
> **Ví dụ** — `lookupAddress`
> - **Given** "100-0001" (tồn tại), "999-9999" (không tồn tại), và service master (mock) trả lỗi
> - **When** gọi `lookupAddress`
> - **Then** tồn tại → điền đúng tỉnh/thành; không tồn tại → thông báo không tìm thấy; lỗi API → xử lý có kiểm soát, không crash

**☐ F9 — Trường bắt buộc có điều kiện.** "Field A bắt buộc **nếu** B được chọn" → test đủ tổ hợp phụ thuộc chéo.
> **Ví dụ** — `validateForm` (lý do bắt buộc **nếu** trạng thái = Từ chối)
> - **Given** form (trạng thái = Từ chối, lý do rỗng) và form (trạng thái = Duyệt, lý do rỗng)
> - **When** gọi `validateForm`
> - **Then** form 1 → lỗi "bắt buộc nhập lý do"; form 2 → hợp lệ (không bắt buộc)

**☐ F10 — Quy tắc trigger / thông báo nghiệp vụ.** Điều kiện kích hoạt đúng / không; **hủy giữa chừng**; **nhiều trigger cùng thỏa**.
> **Ví dụ** — `evaluateTriggers(event)`
> - **Given** event thỏa điều kiện kích hoạt; một event bị hủy giữa chừng; một event thỏa **2 trigger** cùng lúc
> - **When** gọi `evaluateTriggers`
> - **Then** kích hoạt khi thỏa, **không** kích hoạt khi hủy; khi nhiều trigger cùng thỏa → xử lý đúng spec (vd chỉ bắn 1 lần / theo ưu tiên)

---

## Phụ lục A — Chuẩn chất lượng test code

Quan điểm ở đây trả lời *"test viết ra có đạt chất lượng không"*, áp dụng khi review mã test.

**Nguyên tắc FIRST**

- **Fast** — đủ nhanh để chạy mỗi lần commit; không gọi I/O thật.
- **Isolated** — không phụ thuộc test khác, không phụ thuộc thứ tự chạy; tự chuẩn bị và dọn dữ liệu.
- **Repeatable** — kết quả như nhau ở mọi máy / mọi thời điểm; cố định clock, seed random qua injection.
- **Self-validating** — pass/fail tự động bằng assertion, không cần người đọc log.
- **Timely** — viết cùng lúc (hoặc trước) code production, không dồn về cuối sprint.

**Cấu trúc & đặt tên**

- Mỗi test theo mẫu **AAA** (Arrange – Act – Assert), một test xác minh **một hành vi**. Mẫu này chính là Given–When–Then ở dạng code (Arrange = Given, Act = When, Assert = Then).
- **Tên test thống nhất bằng tiếng Anh** theo cấu trúc `methodName_stateUnderTest_expectedBehavior` (đơn vị đang test _ điều kiện _ kết quả kỳ vọng). Ví dụ: `calcShippingFee_whenVipCustomer_returnsZero`, `validateAge_whenBelowMin_returnsInvalid`. **Không** đặt tên tiếng Việt/Nhật, cũng không đặt `test1`, `testOK`.
- Assertion cụ thể (giá trị kỳ vọng rõ ràng), tránh chỉ assert "không throw".

**Chính sách mock**

- Mock tại **ranh giới I/O** (API, DB, file, thời gian, random); **không** mock logic nội bộ của module đang test.
- Mock cần định nghĩa cả case trả lỗi / timeout, không chỉ case thành công (liên kết với D3).
- Tránh over-mocking: phải mock quá nhiều để test được → xem lại thiết kế của code production.

**Test smells cần tránh** (theo xUnit Test Patterns)

- Test phụ thuộc dữ liệu dùng chung, có thể bị sửa (Shared Fixture mutable).
- Assertion Roulette: nhiều assert không có message, fail không biết vì đâu.
- Conditional logic (`if/for`) bên trong test.
- Snapshot test thay thế cho assertion hành vi (snapshot chỉ bổ trợ).

---

## Phụ lục B — Quan điểm từ bug lịch sử (cần bổ sung theo hiện trạng)

> ⚠️ **Phần này để trống có chủ đích.** Đây là phần làm cho danh sách "sát thực tế của dự án" — cần làm 2 việc trước khi chốt phiên bản 1.0:
>
> 1. **Audit test code hiện có** — thống kê pattern đang thiếu (thường: abnormal case, boundary, exception path) và pattern thừa (happy path trùng lặp).
> 2. **Phân loại bug 6–12 tháng gần nhất** — mỗi bug lẽ ra UT bắt được → viết thành 1 quan điểm cụ thể tại đây (kèm kịch bản Given–When–Then), ghi mã bug tham chiếu.

| # | Quan điểm (từ bug thực tế) | Bug tham chiếu | Kịch bản Given–When–Then |
| --- | --- | --- | --- |
| B-01 | *(chưa có — bổ sung sau audit)* | | |

---

## Cách sử dụng & vận hành

1. **Khi thiết kế UT:** developer đi qua **A→E cho mọi hàm** (và **F nếu hàm chạm loại logic đặc thù**); với mỗi quan điểm áp dụng, viết một kịch bản Given–When–Then cụ thể cho hàm của mình. Kết quả là danh sách quan điểm cho tính năng — đầu vào review theo **Ma trận Yêu cầu Review**.
2. **Khi viết mã test:** reviewer đối chiếu Phụ lục A; mỗi Given–When–Then trở thành một test theo mẫu AAA.
3. **Khi đóng bug:** nếu bug lẽ ra UT bắt được, thêm 1 dòng vào Phụ lục B; nếu lặp lại ≥ 2 lần, nâng thành quan điểm chính thức trong nhóm A→E phù hợp.
4. **Chu kỳ review tài liệu:** mỗi quý hoặc sau mỗi release lớn.

