---
name: task-init
description: >-
  Initialize a generic task workspace tasks/{TICKET-ID}/ for ANY project — a 5-stage folder layout
  (01-discovery, 02-plan, 03-backlog, 04-quality, 05-delivery) where every folder carries its own
  README telling the reader what belongs there, who writes it and what to read first. Folders and
  placeholder files are created up front so the shape of the work is visible before any stage runs.
  Trigger on "khởi tạo task", "init task workspace", "tạo workspace cho ticket", or as STAGE 1 of the
  /task-toolkit:report pipeline when a workspace is needed but missing. If the current repo has its own
  /task-toolkit:task-init command (e.g. kaigo's version with legacy-PR fetching), that version wins —
  this is the generic fallback. Locale vn (default) / en / ja.
---

# Task Init (generic — mọi repo)

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

> Gõ `task-init help` → in phần **Help** cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Tạo workspace chuẩn cho 1 task để mọi artifact có chỗ ở cố định — nền cho `task-survey`, `analyze-spec`, `planning`, `backlog-ticket`, `ut-design` và `/task-toolkit:report`.

## Cấu trúc — 5 stage, mỗi thư mục có README riêng

```
tasks/{TICKET-ID}/
├── README.md                    cổng vào: task là gì · đang ở stage nào · đọc gì trước
├── notes.md                     nhật ký chạy suốt task (không thuộc stage nào)
│
├── 01-discovery/                HIỂU — hiện trạng, yêu cầu, chọn hướng
│   ├── README.md
│   ├── current-state.md             ← task-survey
│   ├── impact.md                    ← task-survey (dependency walk)
│   ├── spec-analysis.md             ← analyze-spec
│   └── technical-approach.md        ← analyze-spec (kỹ thuật · bảo mật · môi trường · rủi ro)
│
├── 02-plan/                     CHIA — khối lượng và lịch
│   ├── README.md
│   ├── plan.md                      ← planning (WBS item + checklist tiến độ)
│   └── wbs-schedule.md              ← planning (lịch gửi khách)
│
├── 03-backlog/                  GIAO VIỆC — 1 ticket = 1 file
│   ├── README.md                    ← backlog-ticket (index theo hạng mục WBS)
│   └── ticket-NN-slug.md            ← backlog-ticket
│
├── 04-quality/                  KIỂM — trước và trong khi làm
│   ├── README.md
│   ├── test-checklist.md            ← backlog-ticket (rollup từ Completion condition + regression)
│   ├── ut-design.md                 ← ut-design
│   ├── testcases/                   ← QC skill / e2e-automator (csv, tc-*.md)
│   └── test-report.md               ← kết quả chạy: pass/fail + evidence
│
└── 05-delivery/                 GIAO RA NGOÀI
    ├── README.md
    ├── report-{type}-{YYYYMMDD}.md  ← report
    ├── release-note.md              ← release-note
    └── evidence/                    ảnh chụp, log, file đính kèm gửi kèm report
```

**Tạo sẵn đủ thư mục và file placeholder, kể cả khi chưa có nội dung** — gồm cả `04-quality/testcases/` và `05-delivery/evidence/` (dùng `.gitkeep`). Lý do: người mở workspace phải thấy **hình dạng đầy đủ của công việc** ngay, kể cả phần chưa làm. Thư mục rỗng kèm README là *chỗ đã dành sẵn*; thư mục rỗng không README mới là rác.

File placeholder ghi rõ **trạng thái chưa có nội dung + skill nào sẽ điền**, không để trống trơn:

| File | Nội dung placeholder |
|---|---|
| `technical-approach.md` | `> Chưa phân tích. Sinh bởi analyze-spec khi task có ≥2 phương án kỹ thuật, hoặc đụng bảo mật/hạ tầng/môi trường.` |
| `test-checklist.md` | `> Chưa có ticket. Sinh bởi backlog-ticket — rollup Completion condition của từng ticket + màn hình regression từ impact.md.` |
| `ut-design.md` | `> Chưa thiết kế. Chạy /task-toolkit:ut-design.` |
| `test-report.md` | `> Chưa chạy test.` |
| `release-note.md` | `> **Chưa triển khai release.**` |

## Bước thực hiện

1. Repo có `/task-toolkit:task-init` riêng → dùng bản đó, dừng.
2. Xác định `TICKET-ID` từ arguments/context. Không có ticket → `MISC-<slug>` (đổi tên folder khi có ticket thật).
3. Tạo cây trên (nội dung theo `locale`, mặc định vn). **Không ghi đè file đã tồn tại** — chỉ tạo file/thư mục còn thiếu, để chạy lại được trên workspace cũ.
4. `tasks/` chưa nằm trong `.gitignore` → hỏi user có thêm không (workspace thường cá nhân, không commit).
5. Echo next steps: fill `README.md` → `task-survey {TICKET-ID}` → `analyze-spec` → `planning` → `backlog-ticket`.

## README gốc — `tasks/{TICKET-ID}/README.md`

Là **cổng vào**, không phải bản sao của plan. Đủ 5 khối, field chưa biết ghi `TODO`:

````markdown
# {TICKET-ID} — {tên task}

| | |
|---|---|
| **Status** | ⚪ Draft / 🟡 Đang làm / 🟢 Xong / 🔴 Blocked |
| **Type** | feature · bug · refactor · infra · investigation |
| **Ticket / spec / design** | {link} |
| **Người phụ trách** | {tên} |

## Task này là gì
{1–3 câu — vấn đề cần giải, không chép lại lời khách}

## Đang ở đâu
- [ ] 01 Discovery — điều tra hiện trạng, làm rõ yêu cầu
- [ ] 02 Plan — chia việc, ước lượng
- [ ] 03 Backlog — sinh ticket
- [ ] 04 Quality — test case, UT design
- [ ] 05 Delivery — report, release note

## Đọc gì trước
{2–3 link vào file quan trọng nhất hiện tại — đổi theo stage}
````

## README từng thư mục — 3 khối, ngắn

Mỗi `NN-*/README.md` chỉ cần trả lời 3 câu, **không dài hơn một màn hình**:

````markdown
# 0N — {Tên stage}

**Thư mục này chứa gì:** {1 câu}

| File | Ai ghi | Nội dung |
|---|---|---|
| `x.md` | skill nào | mô tả 1 dòng |

**Đọc theo thứ tự:** {file nào trước, file nào sau, và vì sao}
````

Nội dung cụ thể cho từng stage:

- **01-discovery** — "Hiểu hệ thống và yêu cầu trước khi chia việc. Không có kết luận nào ở đây được phép thiếu evidence." Thứ tự đọc: `current-state.md` (code đang có gì) → `impact.md` (sửa thì đụng đâu) → `spec-analysis.md` (khách muốn gì, còn hỏi gì) → `technical-approach.md` (đi đường nào, rủi ro gì).
- **02-plan** — "Khối lượng và lịch. `plan.md` là nội bộ, `wbs-schedule.md` là bản gửi khách — Σ est hai file phải khớp."
- **03-backlog** — "Một ticket một file, copy thẳng sang Backlog. Ticket bị bỏ/gộp vẫn giữ file, đánh dấu ở header."
- **04-quality** — "Kiểm chất lượng: cái gì test tự động, cái gì kiểm tay. `test-checklist.md` là của người làm; `testcases/` là bộ chính thức cho tester/automation."
- **05-delivery** — "Thứ đi ra khỏi team. Viết cho người không đọc code: kết luận trước, chi tiết sau."

## Help

```
task-init <TICKET-ID> [locale=vn|en|ja]
  Tạo tasks/{TICKET-ID}/ theo 5 stage: 01-discovery · 02-plan · 03-backlog · 04-quality · 05-delivery.
  - Mỗi thư mục có README riêng (chứa gì · ai ghi · đọc theo thứ tự nào).
  - Tạo sẵn đủ thư mục + file placeholder, kể cả phần chưa làm (ghi rõ skill nào sẽ điền).
  - Repo có /task-toolkit:task-init riêng → bản repo tự thắng.
  - Không ghi đè file đã có; TICKET-ID giữ nguyên format dự án (MAG_UNEI-####, ABC-123, GH-123).
```
