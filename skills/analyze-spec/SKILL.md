---
name: analyze-spec
description: >-
  Analyze the task INPUT for a task on ANY project — a feature/change spec OR a bug report — and turn it
  into a clarified, code-grounded pack: what is being asked (feature: requirements Explicit/Inferred/Open;
  bug: expected vs actual + repro + scope), the related screens/touchpoints, an INPUT CONTRACT (valid
  range, boundaries and required-ness per parameter, each with the SOURCE that proves it was not derived
  from the implementation), and customer-facing open questions & conflicts. GROUNDED by the prior task-survey (reads current-state.md/impact.md) so conflict
  detection is against real code ("spec says X but the system does Y", "the route described doesn't
  exist"), not the document alone. Runs AFTER task-survey for every task type, then hands off: feature →
  planning; bug → RCA (feeds its Problem Statement). Not for test-case authoring (that is the QC
  analyze-spec / create-test-case) and not for writing tickets. Trigger on "phân tích spec/ticket",
  "review spec", "analyze input", "làm rõ yêu cầu", "rút requirement", "làm rõ bug/expected". Locale vn
  (default) / en / ja.
---

# Analyze Spec (bản toolkit — làm rõ input task, grounded by survey)

> Ngôn ngữ giao tiếp: tiếng Việt. Output theo `locale` (mặc định vn). Gõ `analyze-spec help` → in Help cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Làm rõ **input của task** — dù là spec feature hay bug report — thành gói **đã hiểu + đối chiếu code**: khách hỏi gì, đối chiếu hiện trạng (từ task-survey), và **open questions** cần khách chốt. Chạy **sau survey, cho MỌI loại task**; rồi rẽ: feature → planning, bug → RCA. Ambiguity bắt ở đây là **rẻ nhất** — trước khi code/RCA.

> Khác với `analyze-spec` bản QC (hướng testcase, rule-library, testable requirements): bản này hướng **dev/planning** — làm rõ để chia việc / để RCA, conflict để hỏi khách trước khi làm.

## Vị trí trong pipeline (universal — không còn "chỉ khi có spec")

```
task-survey (current-state.md + impact.md)  →  ANALYZE-SPEC  →  ┬─ feature → planning
                     baseline code             làm rõ input,      └─ bug → RCA → planning
                                                grounded vs code
```

- **Luôn chạy sau survey** cho cả feature lẫn bug. Chỉ khác **shape** của phân tích:
  - **Feature/change** → bóc **requirements** (Explicit/Inferred/Open) + màn hình mới/sửa.
  - **Bug** → làm rõ **expected vs actual** + repro + scope + open questions → **feed Problem Statement cho RCA** (RCA không dựng lại).
- **Escape valve**: task **quá nhỏ-rõ** (không mập mờ, 1 file) → được skip; nhưng default là chạy vì input mập mờ là chuyện thường.

## Bước 1 — Gom nguồn + đọc baseline (BẮT BUỘC)

- **Input sources**: ticket khách (dán content trực tiếp cũng được) / BRD / feature doc / screen detail / API docs / business rule / acceptance criteria; với bug: mô tả lỗi + expected + steps + screenshot/log.
- **Baseline code** (mấu chốt): đọc `tasks/{ID}/current-state.md` (gap ✅⚠🆕❌) + `impact.md` (dependency walk) mà **task-survey đã sinh**. Chưa có → chạy `task-survey` trước (không grounded thì conflict/expected yếu).
- Cần **tự đối chiếu thêm một điểm code** cho conflict doc⟷code (đọc phía consumer, đọc cả unit, sinh lệnh verify): áp [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md). Bản chất analyze-spec **tiêu thụ** survey; chỉ mở code trực tiếp khi cần chứng minh một mâu thuẫn cụ thể — vẫn không survey lại từ đầu.

## Nguyên tắc phân tích

### Requirement là **hợp đồng hành vi**, không phải kế hoạch implement

Phép thử nhanh — mượn từ OpenSpec: **nếu implementation đổi mà hành vi nhìn từ ngoài không đổi, thì nó KHÔNG thuộc requirement.**

| ✅ Thuộc requirement | ❌ Không thuộc |
|---|---|
| Hành vi quan sát được mà user hoặc hệ thống downstream dựa vào | Tên class / hàm / biến nội bộ |
| **Input, output, và điều kiện lỗi** | Chọn thư viện / framework |
| Ràng buộc bên ngoài: bảo mật, riêng tư, độ tin cậy, tương thích | Các bước implement |
| Kịch bản **kiểm chứng được** | Kế hoạch thực thi chi tiết |

### Dùng ngôn ngữ chuẩn tắc

Requirement bắt buộc viết bằng **PHẢI / SHALL / MUST** — tránh *"nên"*, *"có thể"*, *"xử lý phù hợp"*. Chữ mơ hồ không phải requirement, nó là **Open Question**.

### Không bịa requirement để lấp chỗ trống

Task thuần refactor / tooling / sửa docs → **không có** requirement nào đổi là chuyện bình thường. Ghi rõ `Không đổi hành vi — lý do: <…>` thay vì nặn ra một dòng cho có. Requirement mô tả hành vi; hành vi không đổi thì requirement không đổi.


- **Không invent**. Phân loại mọi mục: `Explicit` (có trong tài liệu) / `Inferred` (suy ra, ghi căn cứ) / `Open` (chưa đủ căn cứ → hỏi khách).
- Mọi dòng phải **cite nguồn**: `[Tên tài liệu | mục/trang]` hoặc `[current-state.md | file:line]`.
- Conflict ảnh hưởng hành vi/scope → `[BLOCKER]`. Nguồn: spec-vs-spec, hoặc **spec/expected ⟷ code** (current-state).
- Không bỏ qua màn hình phụ / dialog / error branch / permission branch nếu tài liệu gợi ý.

**Hai trục conflict khác nhau, xử lý khác nhau:**

- **Doc ⟷ doc** — hai tài liệu nói khác nhau về cùng một thứ. Giải bằng thang ưu tiên: `screen detail / requirement riêng cho màn hình đang phân tích` › `spec / BRD chính` › `epic / story` › `API contract / tech doc` › `testcase cũ / ghi chú`. Hai nguồn **ngang cấp** mà lệch và ảnh hưởng hành vi → `[BLOCKER]`, không tự chọn bên.
- **Doc ⟷ code** — **KHÔNG giải bằng ưu tiên.** Hai bên trả lời hai câu khác nhau: doc nói *nên làm gì*, code nói *đang làm gì*. Lệch nhau là **phát hiện cần báo**, không phải tranh chấp cần phân xử. Luôn ghi cả hai phía kèm nguồn (`[spec | 3.2]` vs `[current-state.md | file:line]`) và để khách/PO quyết bên nào là đúng ý.

## Quy trình (thích ứng feature ↔ bug)

### B1 — Scope & mục tiêu
- **Feature**: giải quyết gì; actor/role; trigger → end-state; In-scope / Out-of-scope.
- **Bug**: hành vi **expected** (theo spec/docs) vs **actual** (đang xảy ra); phạm vi (màn hình/điều kiện lỗi); mức nghiêm trọng.
- Scope/expected không rõ → tạo Open Question, không tự đoán.

### B2 — Related screens/touchpoints (map vào baseline)
Màn hình/touchpoint task đụng tới, **đối chiếu current-state.md**: cái nào ĐÃ CÓ (✅/⚠), cái nào MỚI (🆕). Mỗi dòng: định danh | vai trò flow | entry | action | dependency (impact.md) | có sẵn/mới | source.

### B3 — Cốt lõi (theo loại)
- **Feature → Requirements** atomic: `REQ-ID | Screen/Flow | Requirement | Type (UI/Validation/Behavior/BusinessRule/Permission/Integration/Abnormal/I18N) | Maps to (✅/⚠/🆕 từ current-state) | Source | Confidence`. Cột `Maps to` là cầu sang planning (🆕/⚠ → WBS item; ✅ → chỉ verify).

  **Mỗi requirement PHẢI kèm ≥1 scenario** dạng `WHEN … THEN …` (mượn OpenSpec). Đây là chỗ requirement trở nên **kiểm chứng được** — và là cầu trực tiếp sang unit test: mỗi scenario là một case tiềm năng.

  ```
  ### REQ-03 — Phí giao hàng theo hạng khách
  Hệ thống PHẢI miễn phí giao hàng cho khách VIP.

  #### Scenario: Khách VIP
  - WHEN đơn hàng của khách hạng VIP
  - THEN phí giao hàng = 0

  #### Scenario: Khách thường, dưới ngưỡng
  - WHEN khách thường, tổng đơn < 500.000đ
  - THEN phí giao hàng = 30.000đ
  ```

  Requirement **không viết được scenario nào** → nó chưa đủ rõ → **Open Question**, không phải requirement.
- **Bug → Expected behaviors**: `ID | Screen/Flow | Expected (đúng ra phải) | Actual (đang bị) | Repro steps | Scope/điều kiện | Source | Confidence`. Bảng này chính là **Problem Statement** cho RCA.

### B3b — Phân loại thay đổi so với hiện trạng (delta)

Ngoài phân loại theo *nguồn gốc* (Explicit/Inferred/Open), gắn thêm chiều **thay đổi gì so với hệ thống đang chạy** — mượn OpenSpec:

| Nhãn | Nghĩa | Bắt buộc kèm |
|---|---|---|
| `ADDED` | Hành vi hoàn toàn mới | — |
| `MODIFIED` | Hành vi cũ đổi | **Ghi ĐỦ nội dung mới**, không ghi mỗi phần đổi — ghi thiếu là mất chi tiết khi bàn giao |
| `REMOVED` | Bỏ hành vi cũ | **Lý do** + **Cách chuyển đổi** cho dữ liệu/user đang dùng |
| `RENAMED` | Chỉ đổi tên, hành vi giữ nguyên | `FROM:` / `TO:` |

Nhãn này ghép với cột `Maps to`: `🆕 + ADDED` là việc mới hoàn toàn; `⚠ + MODIFIED` là chỗ **dễ vỡ nhất** vì đụng code đang chạy — ưu tiên khi chia WBS và khi viết test hồi quy.

### B4 — Conflict & gap (grounded)
- **Conflict** — 2 nguồn khác nhau; hoặc **spec/expected ⟷ code** (`[spec | ...] vs [current-state.md | file:line]`).
- **Gap / undefined** — có hành động/trạng thái nhưng thiếu expected; boundary/error chưa mô tả.
- **Không tồn tại** — task nhắc route/màn hình/field mà survey không thấy → cờ đỏ, hỏi khách (thường khách ở bản deploy cũ / nhầm scope).
- Phân loại `[BLOCKER]` (chặn: business outcome/permission/scope/expected) hoặc `[CLARIFY]`.

### B5 — Input Contract (miền giá trị & ràng buộc) 🆕

**Đây là phần hay bị bỏ nhất, và là lý do test giá trị biên hay thiếu.** Requirement mô tả *hành vi*; phần này mô tả *dữ liệu vào được phép nhận cái gì*. Thiếu nó thì không ai biết biên nằm ở đâu để mà kiểm.

Với **mỗi tham số / trường nhập** mà task đụng tới, xác định:

| Cần xác định | Ví dụ |
|---|---|
| Kiểu dữ liệu | `int` · `string` · `list<Item>` |
| **Miền hợp lệ** — cận dưới, cận trên | `18–120` · `≤ 50 ký tự` · `> 0` |
| Bắt buộc hay không | có · không · **bắt buộc nếu <điều kiện>** |
| Giá trị đặc biệt được phép | rỗng · `null` · `0` · danh sách rỗng |
| Nguồn của ràng buộc | ← **cột quan trọng nhất** |

**Ba nguồn hợp lệ, xếp theo độ tin cậy:**

| Nguồn | Vì sao dùng được |
|---|---|
| **Spec / acceptance criteria** | Tốt nhất — viết độc lập với code |
| **Schema DB · migration** | `varchar(50)` · `NOT NULL` · `unsigned` · `CHECK` là **khai báo**, không phải logic xử lý |
| **API contract · OpenAPI** | `minimum` · `maxLength` · `enum` · `pattern` |

⚠ **Rule validate trong code KHÔNG phải nguồn hợp lệ.** Lấy miền giá trị từ đó là chép lại hành vi hiện tại — nếu rule đang sai thì ràng buộc chép ra cũng sai theo. Chỉ ghi nhận nó như **[Inferred]** kèm câu hỏi cho khách.

Không tìm được ràng buộc ở cả ba nguồn → **Open Question**, không tự đặt ra một con số.

### B6 — Đóng câu hỏi (Decision Log) 🆕

B4 **mở** câu hỏi. Bước này **đóng** chúng. Thiếu nó thì câu trả lời của khách chết trong mail hoặc Slack, và ba tuần sau không ai biết một ràng buộc có mặt vì khách chốt hay vì ai đó đoán.

Mỗi `QA-*` được trả lời → **một dòng `DEC-*`**:

| Cần ghi | Vì sao |
|---|---|
| Đóng `QA-ID` nào | nối ngược lên section 6, để thấy còn câu nào treo |
| Quyết định | phát biểu dứt khoát, không "có vẻ như" |
| Lý do | căn cứ, không phải cảm tính |
| **Phương án đã loại + vì sao loại** | ← **cột quan trọng nhất**, xem dưới |
| Ai chốt · khi nào · qua kênh nào | mail / họp / Backlog comment — phải truy được |
| `REQ-*` bị ảnh hưởng | quyết định làm đổi requirement nào |

**Cột `Phương án đã loại` là thứ đắt nhất trong bảng.** Không có nó, sáu tháng sau sẽ có người nhìn code thấy "chỗ này làm hơi lạ" rồi sửa lại thành đúng cái phương án đã bị loại có lý do. Ghi lại phương án bị loại là cách rẻ nhất để chặn việc đó.

Hai luật:

- **Chỉ ghi `DEC-*` khi có người thật chốt.** AI suy ra một câu trả lời hợp lý ≠ quyết định. Không có ai chốt thì `QA-*` vẫn treo.
- **Quyết định đổi requirement thì phải sửa section 4 luôn**, không để hai chỗ nói khác nhau. `DEC-*` là *lịch sử*; section 4 là *hiện trạng*.

Khi **mọi** `QA-*` mức `🔴 BLOCKER` đã có `DEC-*` đóng → Status chuyển `BLOCKED → READY`. Đây là quy tắc kiểm được, không phải cảm nhận "chắc đủ rồi".

## Output — 7 section (lưu `tasks/{ID}/spec-analysis.md`)

Thứ tự cố định, dùng bảng:

1. **Analysis Status** — `Status: READY / BLOCKED` | Loại (feature/bug) | Lý do | Nguồn đã đọc (input + baseline) | Mức tin cậy. Còn `[BLOCKER]` chưa có `DEC-*` đóng → `BLOCKED`.
2. **Task Summary** — feature: **Vì sao bây giờ** 🆕 | Mục tiêu | Actor | Trigger→End-state | In/Out-scope; bug: **Expected vs Actual** | Phạm vi | Mức nghiêm trọng. + Impact chính | Tài liệu dùng.

   ⚠ **`Vì sao bây giờ` khác `Mục tiêu`.** `Mục tiêu` nói *làm gì*; ô này nói *vấn đề nào đang có, vì sao phải xử lý đợt này*. Nó là thứ duy nhất để đối chiếu khi scope phình ra giữa chừng — "cái vừa thêm có phục vụ lý do ban đầu không?". Không có ô này thì mọi đề xuất thêm việc đều nghe hợp lý. Spec không nói → Open Question, **không** viết lại `Mục tiêu` bằng từ khác cho có.
3. **Related Screens / Touchpoints** — bảng như B2.
4. **Requirements** (feature) *hoặc* **Expected Behaviors / Problem Statement** (bug) — bảng như B3.
5. **Input Contract** 🆕 — `Tham số/Field | Kiểu | Miền hợp lệ (min–max) | Bắt buộc | Giá trị đặc biệt (rỗng/null/0) | Nguồn | Confidence`. Ràng buộc chưa tìm được nguồn → để trống + đẩy sang section 6, **không điền ước đoán**.
6. **Open Questions / Conflicts** — `QA-ID | Level (BLOCKER/CLARIFY) | Issue | Source A | Source B / Missing / Code-reality | Impact | Câu hỏi cho khách`.
7. **Decision Log** 🆕 — `DEC-ID | Đóng QA | Quyết định | Lý do | Phương án đã loại | Ai chốt / Khi nào / Kênh | REQ ảnh hưởng`. Lần chạy đầu bảng này thường **rỗng** — đó là bình thường, ghi *"chưa có quyết định nào"*. Nó được điền dần khi khách trả lời, và chính nó quyết định lúc nào Status thành `READY`.

Read-only mặc định (in chat); có workspace + user đồng ý lưu → ghi `tasks/{ID}/spec-analysis.md`.

**Chạy lại trên cùng task**: giữ nguyên `DEC-*` cũ, chỉ thêm dòng mới. Xoá lịch sử quyết định là mất đúng thứ section này sinh ra để giữ.

## Handoff

- **Feature → planning**: `Requirements` (Maps to ⚠/🆕) + In-scope → WBS item. Đề nghị: "lập plan (WBS) từ requirements này?".
- **Bug → RCA**: section 4 (Expected vs Actual + repro) = **Problem Statement** cho `rca-method.md`; RCA **tiêu thụ, không dựng lại**. Sau RCA (root cause) → planning.
- **→ khách**: Open Questions mức `[BLOCKER]` phải **gửi khách chốt TRƯỚC** khi planning/RCA finalize. Khách trả lời → quay lại ghi `DEC-*` (B6), **không** để câu trả lời nằm mãi trong mail.
- **Decision Log → backlog-ticket**: cột `Phương án đã loại` là nội dung cho phần *Note / lý do thiết kế* của ticket. Người code sau đọc ticket sẽ biết vì sao không làm cách hiển nhiên hơn.
- **→ unit test**: section 4 (Requirements + scenario `WHEN…THEN`) là nguồn suy `expected`; section 5 (Input Contract) là nguồn cho **giá trị biên**. Không có hai thứ này thì test biên hoặc bị bỏ, hoặc bị chép lại từ code đang chạy.
- **Artifact contract**: analyze-spec đọc survey (không survey lại); planning & RCA đọc spec-analysis (không phân tích lại).

## Guardrails

- Không viết testcase / ticket ở đây (đó là create-test-case / backlog-ticket).
- Không coi Inferred là fact; conflict spec/expected-vs-code phải cite cả 2 phía.
- Còn `[BLOCKER]` chưa có `DEC-*` đóng → `BLOCKED`, không kết luận input sẵn sàng để planning/RCA.
- **Không tự ghi `DEC-*`.** Quyết định phải có người thật chốt, kèm ai/khi nào/kênh nào. AI suy ra câu trả lời hợp lý là `[Inferred]`, không phải quyết định.
- Ghi `DEC-*` mà không cập nhật section 4 tương ứng → hai chỗ nói khác nhau, cấm.
- `Vì sao bây giờ` không có trong spec → Open Question, không diễn giải lại `Mục tiêu`.
- Không bỏ qua chữ mơ hồ ("xử lý phù hợp", "hiển thị đúng") mà không truy rule cụ thể → thành Open Question.
- Giữ nguyên chuỗi UI gốc (tiếng Nhật…) ở mọi locale.
- **Không lấy miền giá trị / biên từ rule validate trong code** — chỉ từ spec, schema DB, hoặc API contract. Lấy từ code thì đánh `[Inferred]` + Open Question.
- **Không bịa requirement** khi task không đổi hành vi (refactor/tooling/docs) — ghi rõ "không đổi hành vi" là hợp lệ.
- Requirement không viết nổi một scenario `WHEN…THEN` → chưa đủ rõ → Open Question.

## Ví dụ output đầy đủ

Xem [`example-output.md`](example-output.md) — một `spec-analysis.md` đã điền, 7 section, có sẵn ba loại conflict, một Input Contract lấy từ cả ba nguồn hợp lệ, và một `DEC-*` kéo theo hai chỗ sửa ngược lên section 3 và 4. Trong đó đánh dấu 👀 những chỗ hay bị làm sai nhất.

## Những câu tự bào chữa hay gặp

Bảng này để **tự soi mình** trước khi báo xong — mượn cách làm của `sdd-techtus`.

| Câu bào chữa | Sự thật |
|---|---|
| *"Yêu cầu rõ rồi, khỏi cần analyze"* | Rõ với người đọc spec ≠ rõ với người sẽ code. Bỏ bước này không xoá chi phí, chỉ đẩy nó xuống lúc đang code — lúc đó đắt hơn nhiều |
| *"Chỗ này chắc là ý khách muốn vậy"* | Đó là `Inferred`, phải ghi căn cứ. Viết như `Explicit` là bịa có tổ chức |
| *"Miền giá trị đọc code validate là ra"* | Ra được **hành vi hiện tại**, không phải **hành vi đúng**. Rule đang sai thì chép ra cũng sai theo |
| *"Biên thì tí nữa dev tự biết"* | Không ai tự biết. Biên không ghi ra là biên không được test — đó là chỗ bug hay nấp nhất |
| *"Task này refactor, phải có requirement gì đó chứ"* | Không. Hành vi không đổi thì requirement không đổi. Nặn thêm một dòng cho có là làm bẩn tài liệu |
| *"Còn một BLOCKER thôi, cứ planning trước"* | BLOCKER là thứ **đổi được cả scope**. Plan dựng trên nó phải làm lại từ đầu |
| *"Conflict doc vs code — chắc code đúng vì nó đang chạy"* | Đang chạy ≠ đang đúng. Hai bên trả lời hai câu khác nhau; để khách quyết, đừng tự phân xử |
| *"Khách trả lời rồi, ai cũng biết, khỏi ghi Decision Log"* | "Ai cũng biết" có hạn dùng khoảng hai tuần. Sau đó còn lại một ràng buộc không ai giải thích được — và người sau sẽ sửa nó |
| *"Phương án bị loại thì ghi làm gì, có làm đâu"* | Chính vì không làm nên phải ghi. Không ghi thì nửa năm sau có người thấy chỗ này "làm hơi lạ" rồi sửa lại thành đúng cái đã bị loại |
| *"Vì sao bây giờ" thì cũng như "Mục tiêu" thôi"* | Không. `Mục tiêu` mô tả việc; `Vì sao bây giờ` là thước để đo mọi đề xuất phình scope sau đó |

## Help

```
analyze-spec <feature | bug | path/ticket-content> [locale=vn|en|ja]
  Làm rõ INPUT task (feature HOẶC bug), ĐỐI CHIẾU current-state.md/impact.md (grounded by survey).
  - Feature → requirements (Explicit/Inferred/Open, mỗi cái ≥1 scenario WHEN/THEN) + related screens → planning.
  - Input Contract: miền giá trị/biên từng tham số + NGUỒN ràng buộc → nuôi test giá trị biên.
  - Bug → expected vs actual + repro + scope → feed Problem Statement cho RCA.
  - Luôn chạy sau task-survey; task nhỏ-rõ thì được skip. BLOCKER open questions → hỏi khách trước.
  KHÔNG viết testcase (QC analyze-spec/create-test-case) hay ticket (backlog-ticket).
```
