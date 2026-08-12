---
name: backlog-ticket
description: >-
  Generate standardized Backlog/Jira ticket content (title + markdown body) plus an evidence-based
  effort estimation for ANY project, writing one file per ticket into tasks/{ID}/backlog/ with a
  WBS-grouped README index, consuming task-survey output (current-state.md / impact.md) so the
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

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

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

- Có `tasks/{TICKET-ID}/02-plan/plan.md` (do `planning` sinh) → **đọc TRƯỚC TIÊN** và hỏi ngay: *ticket này ứng với item số mấy của plan?* Plan đã cắt phạm vi rồi — xem bảng dưới.
- Có `tasks/{TICKET-ID}/01-discovery/current-state.md` + `impact.md` (do `task-survey` sinh, hoặc do `/task-toolkit:report` STAGE 2) → **đọc và dùng thẳng**. Không grep lại từ đầu.
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

**Đầu vào bắt buộc — đọc đủ 6 artifact của `01-discovery`/`02-plan`, không bỏ cái nào:**

| Artifact | Rút gì vào ticket | Bỏ qua thì nợ gì |
|---|---|---|
| `01-discovery/spec-analysis.md` | Requirements + scenario `WHEN…THEN…` → `Completion condition`; Input Contract → biên cần test | Ticket viết theo suy đoán, tiêu chí hoàn thành không kiểm được |
| `01-discovery/impact.md` | mục 7 (impact → lưới kiểm) → checkbox `Regression`; **mục 6 (hành vi phải giữ nguyên)** → `Completion condition` dạng "vẫn phải đúng như cũ" | Degrade: sửa xong màn A, hỏng màn B, không ai kiểm |
| `01-discovery/technical-approach.md` | phương án **đã chốt** → `Technical Notes`; phương án **đã loại** → ghi kèm để không ai đề xuất lại | Bàn lại từ đầu giữa lúc làm |
| `01-discovery/security.md` | **mọi dòng `⚠ Cần làm`** → 1 checkbox `Implementation content` + 1 `Completion condition` kiểm được | Nợ bảo mật nằm lại trong file, không ai làm |
| `01-discovery/performance.md` | điểm nghẽn → bước implement; ngân sách → `Completion condition` (vd "API p95 < 200ms") | Ship xong mới biết chậm |
| `04-quality/ut-design.md` | 1 checkbox *"viết UT theo `ut-design.md`"* + viewpoint bắt buộc | UT làm theo cảm tính hoặc bỏ luôn |

⚠ **Chưa có artifact nào trong số này** → nói rõ **thiếu cái gì** trước khi sinh ticket, và đánh dấu phần tương ứng trong ticket là `[chưa phân tích]`. Sinh ticket im lặng trên nền thiếu là cách nợ kỹ thuật đi vào sprint mà không ai thấy.

⚠ **`spec-analysis.md` còn `QA-*` mức 🔴 BLOCKER chưa có `DEC-*` đóng** → **báo trước khi sinh**. Ticket dựng trên câu hỏi chưa được khách trả lời sẽ phải làm lại.

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
## Description

{1–3 câu: hiện trạng + đổi gì + tại sao/kết quả mong đợi. Giải thích "tại sao", đừng chép lại lời khách.}

## Implementation content

* [ ] {Bước — tên file/function thật từ survey}
* [ ] {Bước}
* [ ] {Unit test / cập nhật test}
* [ ] {Manual QA trên màn hình ảnh hưởng}
* [ ] {Tạo PR tới {PR_TARGETS}}

## Completion condition / Checklist

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

### Ghi file — **một ticket một file**, KHÔNG dồn vào một `backlog.md`

Có `tasks/{TICKET-ID}/` → ghi vào **thư mục** `tasks/{TICKET-ID}/03-backlog/`:

```
tasks/{TICKET-ID}/03-backlog/
├── README.md                              ← index, gom theo hạng mục WBS của plan.md
├── ticket-01-{slug}.md
├── ticket-02-{slug}.md
└── …
```

- **Tên file** `ticket-{NN}-{slug}.md` — `NN` 2 chữ số (số item trong `plan.md`, để tên tự sort đúng thứ tự thực thi), `slug` 2–4 từ kebab-case rút từ title tiếng Anh.
- **Mỗi file**: header ngắn (Ticket no — title · WBS hạng mục · Layer · Est · Trạng thái · link về README/plan), rồi `---`, rồi **nguyên văn Title + Body** để copy thẳng sang Backlog.
- **`README.md`**: bảng index **gom theo hạng mục WBS** — mỗi hạng mục một bảng `| # | Ticket (link) | Layer | Est | Trạng thái |`, cộng dòng đầu ghi tổng số ticket / tổng est / ngân sách đã chốt.

**Vì sao không dồn một file:** một file gộp 20+ ticket là vài chục KB — không review từng phần được, không gán người theo file được, và mọi lần sửa một ticket đều đụng cả file trong diff. Một ticket một file thì mở file là copy được, và git diff chỉ ra đúng ticket vừa đổi.

**Ticket bị bỏ hoặc bị gộp thì GIỮ FILE**, đánh dấu trạng thái ở header (`❌ BỎ — lý do` / `⤵ Gộp vào ticket N`) và ghi ở cột Trạng thái trong README. Nội dung của nó là nguồn khi viết ticket đã hấp thụ nó — xoá đi là mất phần đã nghĩ.

### Kèm theo: cập nhật `04-quality/test-checklist.md`

Sinh xong ticket thì **rollup luôn** sang checklist kiểm tay — nó là của người làm, khác `testcases/` (bộ chính thức cho tester/automation):

- Mỗi ticket đóng góp các dòng `Completion condition` **kiểm được bằng tay**.
- Mỗi màn hình/chức năng trong `Risk/Impact` (lấy từ `impact.md`) → **1 checkbox regression**.
- Nhóm theo: Unit · Feature · Manual · Regression. Mỗi dòng ghi rõ **thuộc ticket nào**.

Không rollup thì `Risk/Impact` chỉ là văn bản đọc cho vui — không ai tick, không ai biết đã kiểm hay chưa.

Sinh nhiều ticket một lượt → **ghi lần lượt từng file**, xong báo 1 bảng tóm tắt (số ticket / tổng est / path). Kết bằng 1 dòng mời chỉnh ("siết checklist / thêm Technical Notes / đổi locale?"). Bỏ summary dài.

### Khi ticket hấp thụ ticket khác (do cắt phạm vi)

Plan bị cắt ngân sách → vài item gộp vào item khác. Ticket nhận phải:

1. Có **block ghi chú đầu Body**: gộp từ ticket nào, phạm vi nào được mang sang, phạm vi nào **không** mang được (và chuyển đi đâu).
2. Mang các checkbox của ticket bị gộp vào `Implementation content`, đánh dấu `*(từ ticket N)*`.
3. **Cộng est có ghi dòng riêng** trong bảng Estimation, và nếu tổng est mới nhỏ hơn tổng est cũ của các ticket thành phần → ghi **cảnh báo ước lượng chật** kèm con số cũ. Đây là chỗ dễ mất dấu nhất khi cắt ngân sách.

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
- **Dồn nhiều ticket vào một `backlog.md`** — mỗi ticket một file trong `backlog/`, index ở `backlog/README.md` (Bước 6).
- **Xoá file của ticket bị bỏ/bị gộp** — giữ file, đánh dấu trạng thái; nội dung đó là nguồn cho ticket đã hấp thụ nó.
- Gộp ticket do cắt ngân sách mà **không ghi est cũ** — mất dấu chỗ ước lượng bị bóp.

## Help

```
backlog-ticket <TICKET-NUM|mô tả> [locale=vn|en|ja]
  Sinh title + body ticket chuẩn công ty + estimation, ăn từ task-survey (current-state.md/impact.md).
  - Repo có config .claude/backlog-ticket.config.md → repo tự thắng (project tag, PR targets, ví dụ).
  - Chưa có survey → chạy task-survey trước (hoặc grep nhanh + [verify in code]).
  - Gọi qua /task-toolkit:report sau analysis: "generate backlog + estimation" (không survey lại).
  - Output: tasks/{ID}/backlog/ticket-NN-slug.md (1 ticket = 1 file) + backlog/README.md (index theo hạng mục WBS).
  KHÔNG dùng cho: PR description (gitflow), viết report điều tra (report).
```
