---
name: planning
description: >-
  Break a task/epic into a work-breakdown plan for ANY project — a WBS overview table (item no, task
  title, task detail, preliminary estimate, scope & impact, expected outcome per item) PLUS a per-item
  progress checklist to tick as work lands. Consumes prior evidence (analyze-spec requirements,
  task-survey current-state.md/impact.md) and does NOT re-investigate. Bridges the pipeline: each plan
  item hands off to backlog-ticket (detailed ticket + refined estimate); the plan also feeds the report.
  Also produces wbs-schedule.md — the customer-facing schedule that converts effort into calendar dates
  (hours per unit, hours allocated per day, stretch factor, holidays, stated assumptions) whenever the
  task carries an external time commitment. Project specifics (estimate unit, conventions) via runtime adapter. Trigger on "lập kế hoạch",
  "planning", "chia task", "WBS", "kế hoạch làm", or as the stage between investigate and tickets.
  Locale vn (default) / en / ja. Do NOT use to write a single detailed ticket (that is backlog-ticket).
---

# Planning — Work-breakdown (generic mọi repo)

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

> Ngôn ngữ giao tiếp: tiếng Việt. Nội dung plan theo `locale` (mặc định vn). Gõ `planning help` → in Help cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Chia 1 task/epic thành **kế hoạch các việc sẽ làm**: một **bảng WBS tổng quan** (nhìn toàn cảnh + tổng est) và một **checklist theo item** (tick tiến độ khi làm). Đây là stage giữa *điều tra* và *sinh ticket* — mỗi item của plan sẽ thành 1 backlog-ticket chi tiết sau.

## Bước 1 — Adapter: quy ước dự án (dừng khi đủ)

Cần: `EST_UNIT` (mặc định man-day `md`; đổi story point nếu repo dùng point), `PROJECT conventions` (gitflow, layer). Precedence như các skill khác: repo config (`.claude/*.config.md`) → `project-context`/`CLAUDE.md` → hỏi 1 câu nếu thiếu `EST_UNIT`.

## Bước 2 — Đọc evidence stage trước (KHÔNG điều tra lại)

Plan ăn từ artifact đã có:

- `analyze-spec` output (requirements rõ / suy ra / open questions) → nếu task bắt đầu từ spec.
- `task-survey` → `current-state.md` (gap ✅⚠🆕❌) + `impact.md` (dependency walk).
- RCA/discovery output → nếu là bug/kiến trúc lạ.

Chưa có evidence → gọi stage tương ứng trước (`analyze-spec` / `task-survey`), hoặc — nếu user chỉ cần plan nháp — grep nhanh + đánh dấu `[verify in code]`.

## Bước 3 — Chia item (granularity)

Nguyên tắc tách:

- **1 item = 1 deliverable mạch lạc** ≈ 1 PR / 1 ticket, thường **0.5–3 md**. To hơn 3 md → tách nhỏ; nhỏ hơn 0.5 md và cùng file → gộp.
- Tách theo **ranh giới tự nhiên**: layer (BE/FE), màn hình, endpoint, bước migration, nhóm regression.
- Mỗi item **độc lập test được** nếu có thể; item phụ thuộc nhau → ghi thứ tự/dependency ở Bước 4.
- Item suy thẳng từ `current-state.md`: mỗi cụm ⚠update/🆕new liên quan → 1 item; ✅reuse → không thành item (chỉ verify).
- **Phép thử ranh giới**: chỉ tách khi reviewer **có thể từ chối item này mà vẫn duyệt item bên cạnh**. Không tách được theo tiêu chí đó thì đang tách theo cảm tính, gộp lại.
- **Setup / config / scaffolding / doc không thành item riêng** — gộp vào item có deliverable cần chúng. Một item "chuẩn bị môi trường" không ai review độc lập được, và nó che mất tiến độ thật.

## Bước 4 — WBS overview (bảng tổng quan)

````markdown
## Kế hoạch (WBS) — {task/epic}

| No | Task title | Task detail | Est ({EST_UNIT}) | Scope & Impact | Expected outcome |
|---|---|---|---|---|---|
| 1 | {tiêu đề ngắn} | {làm gì — file/function thật từ survey} | {est sơ bộ} | edit: {file}; ảnh hưởng: {màn hình liên quan từ impact.md} | {kết quả kiểm chứng được ở item này} |
| 2 | … | … | … | … | … |

**Tổng est:** {Σ} {EST_UNIT} (confidence: {cao/tb/thấp}).
**Thứ tự / phụ thuộc:** {item nào chặn item nào; critical path; song song được cái nào}.
**Rủi ro kế hoạch:** {2–3 yếu tố có thể trượt — spec chưa chốt, shared component nhiều consumer, cross-repo}.
````

Cột:
- **Est sơ bộ** = ước lượng nhanh theo độ phức tạp + số file (⚠/🆕) + số màn hình impact. Là **khoảng thô** để lập kế hoạch; est tinh để ở backlog-ticket từng item.
- **Scope & Impact** = file sẽ sửa (từ ⚠/🆕) + màn hình/chức năng liên quan (từ dependency walk `impact.md`). Không nhớ tay — lấy từ evidence.
- **Expected outcome** = mỗi item đạt được gì, **kiểm chứng được** (không "làm xong phần X" chung chung).

## Bước 5 — Checklist tiến độ (detail, tick khi làm)

Với mỗi item ở bảng, sinh 1 khối checkbox để theo dõi thực thi:

````markdown
### [ ] Item {No} — {task title}   ({est} {EST_UNIT})
- [ ] {sub-task thực thi 1 — file/function thật}
- [ ] {sub-task 2}
- [ ] {test / QA của item}
- [ ] Outcome đạt: {điều kiện kiểm chứng ở cột Expected outcome}
````

Bảng WBS = **overview** (toàn cảnh + tổng est, xuất xlsx dễ); checklist = **detail** để tick `4/12` tiến độ thật.

## Bước 5.5 — Tự soát (chạy trước khi ghi file, không dispatch subagent)

Ba phép kiểm, tự làm, thấy lỗi thì sửa luôn rồi đi tiếp — không cần soát lại vòng hai:

1. **Coverage** — mở lại `spec-analysis.md`, rà từng requirement có `Maps to` = 🆕 hoặc ⚠: **chỉ được đúng vào một WBS item nào**. Requirement nào không trỏ được vào item nào = **thiếu item**, thêm ngay. Đây là phép kiểm cơ học duy nhất bắt được việc bỏ sót phạm vi.
2. **Đối chiếu overview ↔ checklist** — tên item, số thứ tự, est, dependency ở Bước 4 phải khớp Bước 5. Item số 3 tên khác nhau ở hai bảng là lỗi, không phải cách diễn đạt.
3. **Quét chữ rỗng** — `hoàn thiện`, `cải thiện`, `xử lý`, `optimize`, `refactor cho tốt hơn` ở cột task detail hoặc expected outcome. Thay bằng điều kiện đo được, hoặc bỏ item nếu không nói được nó giao ra cái gì.

## Bước 6 — Lịch gửi khách (`wbs-schedule.md`)

Plan xong mới ra được **khối lượng**. Lịch là bước dịch khối lượng → **ngày**, và nó là artifact **thứ hai, cho người đọc khác**:

| | `plan.md` | `wbs-schedule.md` |
|---|---|---|
| Người đọc | nội bộ team | **khách / PM** |
| Độ mịn | từng item (0.5–3 {EST_UNIT}) | **gom theo hạng mục** — mỗi hạng mục 1 dòng |
| Nội dung riêng | đánh đổi, phương án cắt, item bị bỏ, ghi chú kỹ thuật | ngày bắt đầu/kết thúc, giả định lập lịch |
| Ngôn ngữ | theo `locale` | theo `locale`; khách nước ngoài → **song ngữ** (vn/ja hoặc vn/en), phân cách `ーーー` |

Chỉ sinh khi task có **giao kèo thời gian với bên ngoài** (deadline khách, EOL, release window). Task nội bộ thuần thì bỏ qua bước này — đừng đẻ lịch cho thứ không ai hỏi ngày.

**Hỏi trước khi lập lịch — 3 tham số không suy được từ code, thiếu cái nào thì hỏi cái đó:**

1. **Ngày bắt đầu** và deadline cứng (nếu có).
2. **Quy đổi**: 1 {EST_UNIT} = mấy giờ; người thực hiện dành **mấy giờ/ngày** cho task này. Hai số này ra **hệ số kéo dài** — vd 1 MD = 7h, dành 5h/ngày → 1.4 ngày lịch / 1 MD. Không hỏi mà lấy 1 MD = 1 ngày là **sai hệ thống**, lịch ngắn hơn thực tế ~40%.
3. **Số người / có chạy song song không.** Mặc định: 1 người, tuần tự.

````markdown
# WBS Schedule — {task}

> Bắt đầu **{start}** · Tổng **{Σ} {EST_UNIT}** · Kết thúc dự kiến **{end}**
> {Deadline ngoài nếu có} → còn {n} tuần đệm sau khi xong.
>
> **Quy đổi:** 1 {EST_UNIT} = **{h}h**. Người thực hiện dành **{x}h/ngày** cho task này
> → hệ số kéo dài **{h/x} ngày lịch / 1 {EST_UNIT}**. Tổng {Σ} = {Σ·h}h = **{n} ngày làm việc**.

**Giả định khi lập lịch — đổi giả định thì đổi ngày:**

1. **{Tuần tự / song song}, {n} người, {x}h/ngày.** Cột Est ghi cả **{EST_UNIT}** (khối lượng) và **ngày lịch** (đã nhân hệ số). Đổi phân bổ giờ hoặc thêm người → ngày đổi, khối lượng giữ nguyên.
2. **Chỉ trừ T7/CN.** ⚠ Ngày lễ: {liệt kê ngày lễ rơi vào khung, cả phía khách nếu khác quốc gia} — cần dời hoặc cộng ngày.
3. **Buffer:** {có/không}. Mốc phụ thuộc bên ngoài ({liệt kê}) có thể trượt, ngoài tầm kiểm soát của team.

| No | Category | Detail | Est | Start | Due |
|---|---|---|---|---|---|
| 1 | {tên hạng mục} | {gạch đầu dòng: đã xong ✅ / còn lại / rủi ro đã biết} | {n} {EST_UNIT}<br>({n·hệ số} ngày) | {date} | {date} |
| | **Total** | | **{Σ}**<br>({n} ngày) | **{start}** | **{end}** |
````

**Ba luật của bước này:**

- **Σ {EST_UNIT} của lịch = Σ của plan.** Lệch là lỗi, không phải làm tròn. Nếu buộc phải gửi khách con số khác (đã cam kết trước, hoặc đã cắt phạm vi) → ghi **một mục lệch số liệu** trong `plan.md`: số nào gửi khách, số nào là thực tế, chênh bao nhiêu, vì sao. Im lặng để hai file khác nhau là cách chắc chắn nhất để cả hai cùng sai.
- **Mọi con số trong lịch phải cùng nguồn với `current-state.md`.** Số site, số màn hình, số file — lịch là bản gửi khách nên số sai ở đây đắt hơn nhiều so với sai trong ghi chú nội bộ. Ghi rõ **nguồn** của số ngay tại chỗ dùng.
- **Ngày không tự trượt theo phạm vi.** Phạm vi dày lên mà {EST_UNIT} giữ nguyên thì lịch giữ nguyên — nhưng phải ghi thành **rủi ro vượt khung**, đừng để nó im lặng biến thành trễ hạn.

## Bước 7 — Ghi & handoff

- Có `tasks/{TICKET-ID}/` → ghi `tasks/{TICKET-ID}/02-plan/plan.md` (bảng WBS + checklists) và `02-plan/wbs-schedule.md` (nếu có Bước 6). Chưa có → in chat + đề nghị `task-init`.
- **Handoff xuống ticket**: mỗi row WBS → 1 `backlog-ticket` chi tiết (Description/Implementation/Completion/Scope/Risk + est tinh). Đề nghị 1 dòng: "sinh backlog-ticket cho từng item?".
- **Handoff lên report**: plan là input cho phần "kế hoạch/đề xuất" của `/task-toolkit:report` (type INVESTIGATION/TASK).
- **Artifact contract**: plan tái dùng evidence stage trước; ticket/report tái dùng plan — không stage nào điều tra lại từ đầu.

## Content rules

- Mỗi item nêu **file/function thật** từ survey; thiếu evidence → `[verify in code]`, không bịa.
- Est là **khoảng + confidence**, không số cứng; input thiếu → `[Giả định — cần: …]`.
- Expected outcome kiểm chứng được; cấm "hoàn thiện", "cải thiện" trần.
- Giữ nguyên chuỗi UI gốc (tiếng Nhật…) ở mọi locale.
- Scope & Impact của item phải khớp `impact.md` — im lặng ≠ đã kiểm tra.
- Không nhồi mọi việc thành 1 item khổng lồ; không đẻ item < 0.5 md rời rạc.
- Lịch (Bước 6): không tự chọn hệ số quy đổi giờ → **hỏi**; không tự thêm buffer im lặng → **ghi thành giả định**.

## Help

```
planning <TICKET-ID|mô tả> [locale=vn|en|ja]
  Chia task/epic → bảng WBS (No|Title|Detail|Est sơ bộ|Scope&Impact|Expected outcome) + checklist tiến độ/item.
  - Ăn từ analyze-spec / task-survey (current-state.md, impact.md) — KHÔNG điều tra lại.
  - Ra 2 artifact: plan.md (nội bộ, từng item) + wbs-schedule.md (gửi khách, gom theo hạng mục, có ngày)
    → wbs-schedule chỉ sinh khi task có giao kèo thời gian với bên ngoài.
  - Mỗi item → handoff backlog-ticket (est tinh); plan → feed /task-toolkit:report.
  KHÔNG dùng để viết 1 ticket chi tiết (đó là backlog-ticket).
```
