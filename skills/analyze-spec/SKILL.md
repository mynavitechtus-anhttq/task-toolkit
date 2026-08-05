---
name: analyze-spec
description: >-
  Analyze the task INPUT for a task on ANY project — a feature/change spec OR a bug report — and turn it
  into a clarified, code-grounded pack: what is being asked (feature: requirements Explicit/Inferred/Open;
  bug: expected vs actual + repro + scope), the related screens/touchpoints, and customer-facing open
  questions & conflicts. GROUNDED by the prior task-survey (reads current-state.md/impact.md) so conflict
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
- **Bug → Expected behaviors**: `ID | Screen/Flow | Expected (đúng ra phải) | Actual (đang bị) | Repro steps | Scope/điều kiện | Source | Confidence`. Bảng này chính là **Problem Statement** cho RCA.

### B4 — Conflict & gap (grounded)
- **Conflict** — 2 nguồn khác nhau; hoặc **spec/expected ⟷ code** (`[spec | ...] vs [current-state.md | file:line]`).
- **Gap / undefined** — có hành động/trạng thái nhưng thiếu expected; boundary/error chưa mô tả.
- **Không tồn tại** — task nhắc route/màn hình/field mà survey không thấy → cờ đỏ, hỏi khách (thường khách ở bản deploy cũ / nhầm scope).
- Phân loại `[BLOCKER]` (chặn: business outcome/permission/scope/expected) hoặc `[CLARIFY]`.

## Output — 5 section (lưu `tasks/{ID}/spec-analysis.md`)

Thứ tự cố định, dùng bảng:

1. **Analysis Status** — `Status: READY / BLOCKED` | Loại (feature/bug) | Lý do | Nguồn đã đọc (input + baseline) | Mức tin cậy. Còn `[BLOCKER]` → `BLOCKED`.
2. **Task Summary** — feature: Mục tiêu | Actor | Trigger→End-state | In/Out-scope; bug: **Expected vs Actual** | Phạm vi | Mức nghiêm trọng. + Impact chính | Tài liệu dùng.
3. **Related Screens / Touchpoints** — bảng như B2.
4. **Requirements** (feature) *hoặc* **Expected Behaviors / Problem Statement** (bug) — bảng như B3.
5. **Open Questions / Conflicts** — `QA-ID | Level (BLOCKER/CLARIFY) | Issue | Source A | Source B / Missing / Code-reality | Impact | Câu hỏi cho khách`.

Read-only mặc định (in chat); có workspace + user đồng ý lưu → ghi `tasks/{ID}/spec-analysis.md`.

## Handoff

- **Feature → planning**: `Requirements` (Maps to ⚠/🆕) + In-scope → WBS item. Đề nghị: "lập plan (WBS) từ requirements này?".
- **Bug → RCA**: section 4 (Expected vs Actual + repro) = **Problem Statement** cho `rca-method.md`; RCA **tiêu thụ, không dựng lại**. Sau RCA (root cause) → planning.
- **→ khách**: Open Questions mức `[BLOCKER]` phải **gửi khách chốt TRƯỚC** khi planning/RCA finalize.
- **Artifact contract**: analyze-spec đọc survey (không survey lại); planning & RCA đọc spec-analysis (không phân tích lại).

## Guardrails

- Không viết testcase / ticket ở đây (đó là create-test-case / backlog-ticket).
- Không coi Inferred là fact; conflict spec/expected-vs-code phải cite cả 2 phía.
- Còn `[BLOCKER]` → `BLOCKED`, không kết luận input sẵn sàng để planning/RCA.
- Không bỏ qua chữ mơ hồ ("xử lý phù hợp", "hiển thị đúng") mà không truy rule cụ thể → thành Open Question.
- Giữ nguyên chuỗi UI gốc (tiếng Nhật…) ở mọi locale.

## Help

```
analyze-spec <feature | bug | path/ticket-content> [locale=vn|en|ja]
  Làm rõ INPUT task (feature HOẶC bug), ĐỐI CHIẾU current-state.md/impact.md (grounded by survey).
  - Feature → requirements (Explicit/Inferred/Open) + related screens → planning.
  - Bug → expected vs actual + repro + scope → feed Problem Statement cho RCA.
  - Luôn chạy sau task-survey; task nhỏ-rõ thì được skip. BLOCKER open questions → hỏi khách trước.
  KHÔNG viết testcase (QC analyze-spec/create-test-case) hay ticket (backlog-ticket).
```
