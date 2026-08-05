---
name: task-init
description: >-
  Initialize a generic task workspace tasks/{TICKET-ID}/ with 6 markdown files (README, plan,
  current-state, impact, test-checklist, notes) for ANY project. Trigger on "khởi tạo task",
  "init task workspace", "tạo workspace cho ticket", or as STAGE 1 of the /task-toolkit:report pipeline when a
  workspace is needed but missing. If the current repo has its own /task-toolkit:task-init command (e.g. kaigo's
  version with legacy-PR fetching), that version wins — this is the generic fallback.
  Locale vn (default) / en / ja.
---

# Task Init (generic — mọi repo)

> Gõ `task-init help` → in phần **Help** cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Tạo workspace chuẩn cho 1 task để mọi artifact (survey, impact, plan, test, notes) có chỗ ở thống nhất — nền cho `task-survey`, `backlog-ticket` và `/task-toolkit:report`.

## Bước thực hiện

1. Repo có `/task-toolkit:task-init` riêng → dùng bản đó, dừng.
2. Xác định `TICKET-ID` từ arguments/context. Không có ticket → `MISC-<slug>` (đổi tên folder khi có ticket thật).
3. Tạo `tasks/{TICKET-ID}/` với 6 file (nội dung theo `locale`, mặc định vn; **không ghi đè file đã tồn tại** — chỉ tạo file thiếu):

| File | Nội dung khởi tạo |
|---|---|
| `README.md` | Title, status ⚪ Draft, type (feature/bug/refactor/infra/investigation), links (ticket/spec/design), scope 1–3 câu — field thiếu ghi `TODO` |
| `plan.md` | Checkbox các bước thực hiện (điền sau khi survey) |
| `current-state.md` | Heading rỗng — `task-survey` sẽ fill |
| `impact.md` | Heading: Màn hình/chức năng liên quan (dependency walk) / Risk / Rollback — `task-survey` fill phần đầu |
| `test-checklist.md` | Heading: Unit / Feature / Manual / Regression (quy tắc: 1 checkbox mỗi màn hình liên quan lấy từ `impact.md`) |
| `notes.md` | Daily log: quyết định, blocker, open questions |

4. `tasks/` chưa nằm trong `.gitignore` → hỏi user có thêm không (workspace thường cá nhân, không commit).
5. Echo next steps: fill README → `task-survey {TICKET-ID}` → plan/impact → code/điều tra → `/task-toolkit:report` khi cần báo cáo.

## Help

```
task-init <TICKET-ID> [locale=vn|en|ja]
  Tạo tasks/{TICKET-ID}/ với 6 file chuẩn (README, plan, current-state, impact, test-checklist, notes).
  - Repo có /task-toolkit:task-init riêng → bản repo tự thắng.
  - Không ghi đè file đã có; TICKET-ID giữ nguyên format dự án (MAG_UNEI-####, ABC-123, GH-123).
```
