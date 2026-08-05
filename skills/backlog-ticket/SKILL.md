---
name: backlog-ticket
description: >-
  Generate standardized Backlog/Jira ticket content (title + markdown body) plus an evidence-based
  effort estimation for ANY project, consuming task-survey output (current-state.md / impact.md) so the
  ticket carries real file paths, dependency-walk scope, and testable outcomes. Company-standard template:
  Description / Implementation content / Completion condition, plus Scope, Risk/Impact and Estimation.
  Project specifics (title tag, ticket-number format, layers, PR targets, path conventions, examples)
  come from a runtime adapter (repo backlog config → project-context/CLAUDE.md → framework autodetect),
  never hardcoded. Trigger on "tạo backlog", "viết ticket", "backlog content", "task description",
  "draft a ticket for …", or as the post-analysis handoff of /task-toolkit:report ("generate backlog + estimation").
  Do NOT use for PR descriptions (gitflow) or for writing an investigation report (the report skill).
  Locale vn (default) / en / ja.
---

# Backlog Ticket (generic — mọi repo)

> Ngôn ngữ giao tiếp: tiếng Việt. **Nội dung ticket mặc định `vn`** — đổi bằng `locale`. Gõ `backlog-ticket help` → in phần Help cuối file, không chạy gì.

> **Hỏi locale trước khi sinh ticket.** Nếu lệnh không nêu `locale=`, hỏi đúng một câu rồi mới chạy:
> *"Ticket viết bằng ngôn ngữ nào? `vn` (mặc định) · `en` · `ja`"*
> User trả lời rỗng → `vn`. Đã nêu `locale=` trong lệnh → **không hỏi lại**.
> Gộp câu này với mọi thứ còn thiếu khác (ticket number, layer…) thành **một lượt hỏi duy nhất**, đừng hỏi rải rác.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Sinh nội dung ticket chuẩn công ty — **title + markdown body** — cùng **estimation** dựa trên evidence. Ticket chỉ tốt bằng phần khảo sát nuôi nó: skill này **tiêu thụ** artifact của `task-survey` (không khảo sát lại từ đầu). Ba mục lõi công ty — `Description` / `Implementation content` / `Completion condition` — là bắt buộc; các mục `Scope` / `Risk/Impact` / `Estimation` là chuẩn-mở-rộng của bộ này.

## Vì sao tách 3 mục lõi (giữ khi điền, đừng chép máy móc)

- **English-only** cho body: khách đọc trực tiếp; trộn tiếng Việt làm hỏng mục đích.
- **Title cố định format**: reviewer thấy layer + số ticket ngay trên board.
- **Description / Implementation / Completion tách bạch**: dev cần checklist thực thi, QA/PO cần outcome kiểm chứng được. Trộn hai thứ → sinh ra tiêu chí hoàn thành không ai verify nổi ("viết unit test" không phải thứ QA ký được).
- **Scope (bắt buộc "Out of scope")**: chặn scope-creep ở các ticket đụng UI/logic dùng chung.

## Bước 1 — Adapter: lấy quy ước dự án (theo thứ tự, dừng khi đủ)

Cần resolve các trường sau; lấy theo precedence, **không hardcode**:

| Trường | Ý nghĩa |
|---|---|
| `PROJECT_TAG` | chuỗi giữa title, vd `ACME`, `Web Renewal`, tên project hiển thị trên board |
| `TICKET_FMT` | dạng mã ticket, vd `PROJ-####`, `JIRA-###`, `#123` — lấy **nguyên văn** user đưa |
| `LAYERS` | tập layer hợp lệ, mặc định `BE / FE / BE+FE / INFRA / DOC / BUG / TE` |
| `PR_TARGETS` | nhánh đích theo gitflow của repo (vd `develop`→`staging`; hoặc Bitbucket nội bộ) |
| `PATHS` | quy ước path để survey/Scope (routes/logic/views/DB) — thường đã có từ `task-survey` |
| `EXAMPLES` | ví dụ/label đặc thù dự án (vd chuỗi UI tiếng Nhật) để minh hoạ, giữ nguyên văn |

Precedence:

1. **Repo backlog config** — file `.claude/backlog-ticket.config.md` (hoặc `.codex/…`) nếu có → dùng thẳng, nó khai báo đủ các trường trên + ví dụ đặc thù. **Repo luôn thắng.**
2. **`project-context` skill / `CLAUDE.md`** của repo → rút `PROJECT_TAG`, `PATHS`, `PR_TARGETS`, gitflow.
3. **Framework autodetect** (như `task-survey` Bước 1) cho `PATHS`; `PROJECT_TAG` chưa rõ → **hỏi user 1 câu duy nhất** ("project tag hiển thị trên board là gì?"), rồi nhớ trong phiên.

`TICKET_FMT` và số ticket luôn lấy **đúng như user đưa**, không tự chuẩn hoá.

## Bước 2 — Evidence: đọc artifact task-survey (KHÔNG khảo sát lại)

Đây là điểm khác biệt của bản tích hợp: ticket ăn thẳng output khảo sát.

- Có `tasks/{TICKET-ID}/plan.md` (do `planning` sinh) → **đọc TRƯỚC TIÊN** và hỏi ngay: *ticket này ứng với item số mấy của plan?* Plan đã cắt phạm vi rồi — xem bảng dưới.
- Có `tasks/{TICKET-ID}/current-state.md` + `impact.md` (do `task-survey` sinh, hoặc do `/task-toolkit:report` STAGE 2) → **đọc và dùng thẳng**. Không grep lại từ đầu.
- Chưa có gì → chạy `task-survey {ID|mô tả}` (cùng plugin) trước, hoặc — nếu user chỉ cần nháp nhanh — grep có mục tiêu theo `PATHS` và đánh dấu `[verify in code]` ở chỗ chưa chắc.

**Map `plan.md` → mục ticket** (khi có plan — 1 item của plan = 1 ticket):

| Trong plan | Mục ticket |
|---|---|
| Ranh giới item (đã cắt ở planning) | `Scope` — **dùng nguyên**, KHÔNG tự chia lại |
| Cột *task detail* của item | seed cho `Implementation content` |
| Cột *scope & impact* | `Scope` + đối chiếu `Risk/Impact` |
| Cột *expected outcome* | seed cho `Completion condition` |
| Est sơ bộ của item | **mốc đối chiếu** cho `Estimation`; lệch nhiều → nói rõ vì sao (đọc code chi tiết mới thấy), không im lặng ra số khác |
| Thứ tự / dependency giữa các item | `Technical Notes` — ghi ticket này phụ thuộc ticket nào |

**Map kết quả survey → mục ticket** (gap analysis của `current-state.md` — luôn áp dụng, kể cả khi có plan):

| Nhãn survey | Mục ticket |
|---|---|
| ✅ reuse — file có, không sửa | `Scope → Files to verify only` |
| ⚠ update — file có, sẽ sửa | `Scope → Files to edit` + 1 bước `Implementation content` |
| 🆕 new — chưa có | `Scope → Files to edit` + 1 bước `Implementation content` |
| ❌ conflict — đụng tên/hành vi | `Technical Notes` (đánh dấu `⚠`) |
| dependency walk (`impact.md`) | mỗi màn hình/chức năng liên quan → 1 dòng `Risk/Impact` + 1 checkbox `Regression` |

Nếu survey cho thấy hành vi khách mô tả **không tồn tại** (route/chuỗi không có trong code) → báo user TRƯỚC khi soạn: thường là sai repo, sai layer, hoặc khách đang ở bản deploy cũ.

## Bước 3 — Title

```
[{LAYER}][{PROJECT_TAG}][{TICKET-NUM}] {short task name}
```

- `LAYER` in hoa từ `LAYERS`; suy từ file đụng tới: chỉ BE-logic → BE, chỉ UI → FE, cả hai → BE+FE, deploy/docker/CI → INFRA, ticket chỉ test (không đổi code) → `TE` (đặt tên "Testing - …").
- `TICKET-NUM` nguyên văn.
- Tên: English, verb-first khi tự nhiên, không dấu chấm cuối, ≤ 60 ký tự phần tên.

## Bước 4 — Body (thứ tự section)

3 mục đầu là template công ty, **luôn có**; `Scope` bắt buộc khi đụng code có sẵn; `Risk/Impact` bắt buộc khi đổi hành vi chạy thật (infra/runtime/migration/shared component/data job); `Estimation` mặc định có (xem Bước 5). **Không chèn heading `# title` trong body** — title giao riêng.

````markdown
## **Description**

{1–3 câu: hiện trạng + đổi gì + tại sao/kết quả mong đợi. Giải thích "tại sao", đừng chép lại lời khách.}

## **Implementation content**

* [ ] {Bước — tên file/function thật từ survey}
* [ ] {Bước}
* [ ] {Unit test / cập nhật test}
* [ ] {Manual QA trên màn hình ảnh hưởng}
* [ ] {Tạo PR tới {PR_TARGETS}}

## **Completion condition / Checklist**

* [ ] {Outcome kiểm chứng được — input cụ thể, kết quả mong đợi}
* [ ] {Outcome 2}
* [ ] Regression: {flow cũ phải còn chạy}
* [ ] {Edge case: reload, switch, empty, permission…}

## Scope

- **In scope — Files to edit:** {mỗi file + ghi chú đổi gì}
- **In scope — Files to verify only:** {file trong chuỗi phụ thuộc, không sửa nhưng QA phải mở}
- **Out of scope:** {thứ giống-giống nhưng CỐ Ý không đụng}

## Risk / Impact

| Risk | Impact if it happens | Mitigation / Rollback |
|---|---|---|
| {điều cụ thể có thể sai} | {hậu quả user/env/data} | {cách chặn hoặc hoàn tác — phải là hành động CÓ THẬT} |

## Estimation

{Bảng effort suy từ survey — xem Bước 5.}

## Technical Notes

{Optional. Path, tên method/computed, endpoint, class modifier. Gợi ý thôi, không nguyên code.}

## Design / Reference

{Optional. Figma, screenshot, spec khách.}
````

### Implementation content vs Completion condition (khác nhau, đừng trộn)

| | Implementation content | Completion condition |
|---|---|---|
| Góc nhìn | Dev — "tôi phải làm gì" | QA/PO — "khi nào xong" |
| Nội dung | bước sửa file X, thêm method Y, viết test Z | hành vi kiểm chứng được (click Iwate → header ẩn) |
| Ai tick | Dev khi commit code | QA/reviewer khi verify pass |

Quy tắc: checkbox không tạo thay đổi user thấy được → thuộc Implementation. Non-dev mở app verify được → thuộc Completion.

### Impact coverage (phần bị soi nhất)

Khi ticket sửa 1 màn hình/chức năng, `Risk/Impact` phải liệt kê **mọi màn hình/chức năng khác có thể bị ảnh hưởng**, lấy từ `impact.md` (dependency walk) — **không lấy từ trí nhớ**.

- Mỗi màn hình liên quan tìm được → **1 dòng** trong Risk/Impact, hoặc ghi rõ "không ảnh hưởng vì {lý do}". Im lặng ≠ đã kiểm tra.
- **Risk table ↔ Regression checklist đồng bộ**: mỗi dòng impact map tối thiểu 1 checkbox `Completion → Regression` (1/màn hình).
- Survey ra **0** usage cho thay đổi nhiều file → cờ vàng: đi lại dependency walk trước khi giao ticket.

**Bug cũ phát hiện khi test**: không âm thầm fix, không để chặn nhập nhằng sign-off — ghi repro + evidence, báo PO/khách trong ngày (mặc định tách ticket), và ghi 1 câu vào Risk/Impact: checklist ticket này chỉ chịu trách nhiệm regression **do thay đổi này gây ra**.

### Viết Risk / Impact

- Mỗi dòng = **1 failure mode cụ thể**, không phải category ("rủi ro performance" ❌ → "CPAN modules recompile dưới Perl 5.40 có thể chạy khác" ✅).
- `Mitigation / Rollback` = hành động **có thật** (tag image giữ lại, revert PR, feature flag, test bắt được) — không phải "theo dõi kỹ".
- Luôn có 1 dòng rollback cho ticket ảnh hưởng deploy: đường về là gì, mất bao lâu.

## Bước 5 — Estimation (evidence-based)

Estimation suy từ **con số khảo sát**, không đoán. Rút từ `current-state.md`/`impact.md`:

- `N_edit` = số file *to-edit* (⚠), `N_new` = số file 🆕, `N_verify` = số file ✅ verify-only
- `N_screens` = số màn hình/chức năng trong dependency walk (feed QA effort)
- `type` (bug/feature/refactor/migration), `cross_repo?` (đụng repo anh em), `has_migration?` (DB)

Xuất bảng — chia Dev / Test / Buffer, kèm **drivers** và **confidence**:

````markdown
## Estimation

| Hạng mục | Cơ sở (từ survey) | Ước lượng |
|---|---|---|
| Dev | {N_edit} sửa + {N_new} mới{, +DB migration}{, +cross-repo} | {x} md |
| Test | {N_screens} màn hình ảnh hưởng × (PC/SP) | {y} md |
| Buffer | rủi ro: {driver chính, vd legacy nặng / thiếu spec} | {z} md |
| **Tổng** | | **{x+y+z} md** (confidence: {cao/trung bình/thấp}) |

Drivers: {2–3 yếu tố đẩy effort — vd shared component nhiều consumer, cross-repo cache, spec chưa chốt}.
{Nếu input nào chưa chắc → [Giả định — cần: …]}.
````

Quy ước: đơn vị mặc định **man-day (md)**; đổi sang story point nếu repo dùng point (adapter). Estimation là **khoảng + confidence**, không phải số cứng. Input thiếu → đánh dấu `[Giả định]` thay vì bịa.

## Content rules (mọi section)

- Body theo `locale` đã chốt; heading section giữ English kể cả locale vn/ja (`Description`, `Implementation content`… là mỏ neo template).
- Không `Co-Authored-By`, không attribution.
- Input cụ thể ở Completion ("chọn 岩手県 ẩn header `その他の市区町村`"), không mơ hồ ("user filter được").
- Tránh verb rỗng: `improve`, `optimize`, `better` → thay bằng điều kiện đo được hoặc bỏ.
- Backtick cho token dạng code: path, biến/method/class, route URL, CSS class. Code nhiều dòng → fenced block.
- **Giữ nguyên chuỗi UI gốc** (tiếng Nhật `その他の市区町村`, tên tỉnh…) ở mọi locale — dịch là mất traceability với spec khách.
- **Liệt kê inline ở mọi mục, không cross-reference.** Ticket đụng N file/page → liệt kê đủ ở Implementation, đủ ở Scope, và 1 checkbox/item ở Completion. Lặp là cố ý (dev/QA/khách nhảy thẳng mục họ cần). Cấm "các page nói ở trên".
- **1 checkbox/item khi scope số nhiều.** Đụng 12 page = 12 checkbox, không gộp "tất cả 12 page chạy" (che mất tiến độ thật 8/12).
- **Gom Completion thành sub-section khi list dài** — nhãn chuẩn: **Artifact verification** (kiểm chính file/asset đổi), **Affected pages** (page đổi trực tiếp, mở từng URL PC+SP), **Regression** (page kề, không đổi nhưng phải còn chạy), thêm **API behavior**/**Database state** khi áp dụng.
- **Scope tách "Files to edit" vs "Files to verify only"** — verify-list rỗng cho thay đổi nhiều file = cờ vàng (chưa đi dependency walk).
- **Verify URL/route trước khi viết** — đọc routes thật, đừng chế `/r/tên-blade` từ tên file.

## Bước 6 — Deliver

1 message, 2 fenced block tách bạch:

1. **Title** — 1 dòng trong code fence (copy sạch).
2. **Body** — markdown body trong fence riêng.

Sau đó: có `tasks/{TICKET-ID}/` → lưu `tasks/{TICKET-ID}/backlog.md` (ghi đè OK) và báo path 1 dòng. Kết bằng 1 dòng mời chỉnh ("siết checklist / thêm Technical Notes / đổi locale?"). Bỏ summary dài.

## Tích hợp với /task-toolkit:report

`/task-toolkit:report` sau khi chạy xong analysis (STAGE 2 survey + STAGE 3 RCA) → đề nghị **"generate backlog ticket(s) + estimation"**. Khi user đồng ý (hoặc gõ `/task-toolkit:report backlog`), gọi skill này — nó đọc `current-state.md`/`impact.md` sẵn có, **không khảo sát lại**. Đây là cách rẻ nhất để đi từ điều tra → ticket có estimation.

## Anti-patterns

- **Có `plan.md` mà tự chia lại phạm vi.** Plan đã cắt item; ticket gom/tách khác là phá ranh giới đã chốt, và est không còn đối chiếu được. Thấy plan cắt sai → **báo user**, không âm thầm chia lại.
- Trộn bước implementation vào Completion ("viết unit test cho X" — QA không ký được).
- Bỏ trống "Out of scope" vì "không đụng gì khác" — luôn nêu biên; thật sự không có thì ghi "No related modules affected".
- Dịch label UI tiếng Nhật sang English.
- Nhồi item chủ quan vào Completion ("UI trông đúng", "performance ổn").
- Chèn `# Title` trong body.
- Section `## Related` với link PR/epic — thuộc PR description (gitflow), không thuộc ticket.
- Liệt kê mọi PR target khi chỉ 1 cái áp dụng.
- "N file/page nói ở trên" thay vì liệt kê inline.
- Gộp ma trận QA nhiều page thành 1 checkbox.
- Chế URL từ tên blade.
- Bước implementation chung chung ("update component", "fix logic") — mỗi bước nêu file/function thật từ survey, hoặc mang `[verify in code]` nếu bỏ qua survey.
- Estimation bằng cảm tính thay vì suy từ con số survey.

## Help

```
backlog-ticket <TICKET-NUM|mô tả> [locale=vn|en|ja]
  Sinh title + body ticket chuẩn công ty + estimation, ăn từ task-survey (current-state.md/impact.md).
  - Repo có config .claude/backlog-ticket.config.md → repo tự thắng (project tag, PR targets, ví dụ).
  - Chưa có survey → chạy task-survey trước (hoặc grep nhanh + [verify in code]).
  - Gọi qua /task-toolkit:report sau analysis: "generate backlog + estimation" (không survey lại).
  KHÔNG dùng cho: PR description (gitflow), viết report điều tra (report).
```
