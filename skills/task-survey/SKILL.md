---
name: task-survey
description: >-
  Generic source survey for ANY project — discover routes/controllers/services/views/DB/assets related
  to a task, run the dependency walk (shared components/services/data across screens and sibling repos),
  and fill tasks/{TICKET-ID}/current-state.md + impact evidence that feeds backlog tickets and reports.
  Trigger on "khảo sát source", "survey task", "điều tra hiện trạng code", or as STAGE 2 of the /task-toolkit:report
  pipeline. Project specifics come from a runtime adapter (project-context skill / CLAUDE.md / framework
  autodetect) — never hardcoded. If the current repo has its own /task-toolkit:task-survey command, that version wins.
  Locale vn (default) / en / ja.
---

# Task Survey (generic — mọi repo)

> Ngôn ngữ giao tiếp: tiếng Việt. Nội dung ghi file theo `locale` (mặc định vn). Gõ `task-survey help` → in phần **Help** cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Khảo sát source liên quan 1 task/issue và ghi thành evidence có cấu trúc. Đây là **nguồn sự thật cho Impact coverage** của analyze-spec (grounding), planning, backlog-ticket và report — khảo sát sai thì mọi thứ phía sau sai.

> **Kỹ thuật đào code** (evidence-first, chứng-minh-đừng-khẳng-định, từ vựng grep, dependency walk app+infra, đối chiếu khai báo trùng lặp, đọc consumer-side, uncertainty markers): xem [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md). Skill này = kỹ thuật đó **áp vào phạm vi 1 task**, output là gap analysis + impact.

## Bước 1 — Adapter: lấy tri thức dự án (theo thứ tự, dừng khi đủ)

1. Repo có command `/task-toolkit:task-survey` hoặc skill `project-context` riêng → **dùng bản đó, dừng skill này** (bản repo luôn thắng vì đã tune theo kiến trúc).
2. `CLAUDE.md` của repo (kiến trúc, path convention, env URLs).
3. **Framework autodetect** (nhìn manifest) → dùng patterns mặc định:

| Dấu hiệu | Framework | Routes | Logic | Views/UI | DB |
|---|---|---|---|---|---|
| `composer.json` + `artisan` | Laravel | `routes/`, `src/*/routes/` | `app/`, `src/*/{Application,Domain}/` | `resources/views/`, `*.vue` | `database/migrations/` |
| `package.json` + `next.config.*` | Next.js | `app/` / `pages/` | `lib/`, `services/` | `components/` | `prisma/` / `drizzle/` |
| `Gemfile` | Rails | `config/routes.rb` | `app/{models,services}/` | `app/views/` | `db/migrate/` |
| `pom.xml` / `build.gradle` | Spring | grep `@RequestMapping` | `service/`, `domain/` | `templates/` | `resources/db/` |
| `*.cgi` + `lib/MT*` | Movable Type | nginx conf + `*.cgi` | `lib/`, `plugins/`, `addons/` | `tmpl/`, `themes/` | MT schema |
| Khác | — | grep keywords toàn repo, thu hẹp dần | | | |

## Bước 2 — Survey theo keywords

Từ title/mô tả task rút keywords (tên màn hình, route, chuỗi UI — **giữ nguyên tiếng Nhật**), grep song song các nhóm: routes / controllers-handlers / services-logic / views-components / DB-migrations / assets-config. Ghi bảng: `path | vai trò | liên quan gì đến task`.

## Bước 3 — Dependency walk (quan trọng nhất — feed Impact coverage)

> **Chạy đủ BA TẦNG** theo [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md) §Dependency walk:
> **1** reference trong code (có `codegraph` thì dùng — chưa có thì **hỏi user trước khi cài**, không tự cài) · **2** coupling qua tên bảng/cache key/đường dẫn (luôn grep, công cụ mù) · **3** khai báo chéo layer (luôn thủ công).
> Bỏ tầng 2–3 là bỏ đúng chỗ bug đắt nhất hay nấp.

Với MỖI file sẽ sửa (⚠ update), grep tiếp **usages của nó ở nơi khác**:

- Component/partial/layout dùng chung → màn hình nào khác render nó?
- Service/UseCase/helper dùng chung → flow nào khác gọi (API? batch? page khác)?
- CSS/JS bundle chung → page nào khác load bundle đó (check build config)?
- DB table / cache key / config → producer/consumer nào khác, **kể cả repo anh em** (đọc code phía consumer, không đoán từ producer)?
- URL / route / redirect / SEO surface?

**Chiều infra / runtime + đối chiếu khai báo trùng lặp** (dễ sót nhất — task đụng base image / Dockerfile / workflow / config hạ tầng): áp đúng phần **Dependency walk (infra/runtime-level)** và bảng **Đối chiếu khai báo trùng lặp** trong [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md). Điểm chốt: artifact runtime dùng chung (1 image chạy cả web lẫn scheduled task), hạ tầng chung (1 LB/DB/cache), và cùng giá trị khai ở HAI nơi phải khớp (service↔host, branch trigger↔map env, version pin CI↔Dockerfile) — lệch = bug âm thầm.

Kết quả: danh sách "màn hình/chức năng liên quan" — mỗi item kèm evidence (file:line) — hoặc ghi rõ "không ảnh hưởng vì {lý do}". **Im lặng ≠ đã kiểm tra.**

## Bước 4 — Ghi kết quả

- Có `tasks/{TICKET-ID}/` → fill `current-state.md` (bảng survey + gap analysis ✅ reuse / ⚠ update / 🆕 new / ❌ conflict); phần dependency walk ghi vào `impact.md`. Chưa có workspace → đề nghị chạy `task-init` (cùng plugin) hoặc in ra chat nếu user chỉ cần nhanh.
- **Artifact contract**: output của bước này là input trực tiếp cho `analyze-spec` (grounding), `planning`, `/task-toolkit:report` và `backlog-ticket` — các skill đó KHÔNG khảo sát lại từ đầu, chỉ đọc artifact này (in-context hoặc file path).

## Bước 5 — Summary

≤10 dòng: bao nhiêu file reuse/update/new, conflict nào, **màn hình/chức năng liên quan phát hiện được**, đề xuất bước kế (viết ticket / `/task-toolkit:report` / bắt đầu code).

## Help

```
task-survey <TICKET-ID|mô tả task> [locale=vn|en|ja]
  Khảo sát source liên quan task → current-state.md + impact.md (dependency walk).
  - Repo có /task-toolkit:task-survey riêng → bản repo tự thắng.
  - Không có workspace → gợi ý task-init trước, hoặc in kết quả ra chat.
  Output là input cho analyze-spec (grounding), planning, /task-toolkit:report (STAGE 2) và backlog-ticket (Impact coverage).
```

## Lưu ý

- File path, class name, route, chuỗi UI tiếng Nhật: giữ nguyên ở mọi locale.
- Mỗi dòng kết luận trong survey phải có evidence (file:line) — survey là nơi SINH ra nhãn ✅ cho report.
