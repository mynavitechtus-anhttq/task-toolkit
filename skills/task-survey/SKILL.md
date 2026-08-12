---
name: task-survey
description: >-
  Generic source survey for ANY project — discover routes/controllers/services/views/DB/assets related
  to a task, then run a full impact analysis — not just who calls the code being changed, but who depends
  on its CURRENT behaviour (ordering, formatting, empty values, side effects, timing), the implicit
  couplings that have no code reference at all (shared tables and cache keys, cron ordering, data
  assumptions, alternate entry points, per-environment differences), a blast-radius rating that sets how
  deep testing must go, and an explicit behaviour contract of what must NOT change. Every impact row must
  map to a concrete check in test-checklist / ut-design / testcases — that mapping is what actually
  prevents regressions. Fills tasks/{TICKET-ID}/01-discovery/current-state.md and impact.md, which feed
  backlog tickets, UT design and reports.
  Trigger on "khảo sát source", "survey task", "điều tra hiện trạng code", or as STAGE 2 of the /task-toolkit:report
  pipeline. Project specifics come from a runtime adapter (project-context skill / CLAUDE.md / framework
  autodetect) — never hardcoded. If the current repo has its own /task-toolkit:task-survey command, that version wins.
  Locale vn (default) / en / ja.
---

# Task Survey (generic — mọi repo)

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

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

## Bước 3 — Impact analysis (quan trọng nhất — feed mọi lưới kiểm)

> **Phương pháp đầy đủ 7 bước: [`../_shared/impact-analysis.md`](../_shared/impact-analysis.md).** Đọc file đó, đừng chỉ làm phần dưới.
>
> Ba điều dễ bỏ nhất — bỏ cái nào là mở đường cho degrade:
> 1. **Chiều ngược** — không chỉ *ai gọi code tôi sửa*, mà *ai đang dựa vào hành vi cũ* (thứ tự · định dạng · giá trị rỗng · tác dụng phụ · thời điểm). Đây là nơi regression đắt nhất sinh ra, và nó **không có tham chiếu nào trong code**.
> 2. **Mỗi impact phải sinh ra một việc kiểm** — trỏ được sang `test-checklist.md`, `ut-design.md` hoặc `testcases/`. Danh sách màn hình liên quan mà không nói kiểm gì thì không ai kiểm.
> 3. **Mục "đã kiểm và KHÔNG ảnh hưởng"** — phân biệt *đã soi, không dính* với *chưa nghĩ tới*. Bảng để trống thì hai thứ này nhìn giống hệt nhau.

### Tầng 1–3: bề mặt bị chạm

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

### Tầng 4–7: chiều ngược, ràng buộc ngầm, bán kính, hợp đồng hành vi

Làm theo [`../_shared/impact-analysis.md`](../_shared/impact-analysis.md) Bước 3→7. Tối thiểu phải trả lời:

- **Ai dựa vào hành vi cũ** (Bước 3) — tìm ở: test cũ đang assert · code phía consumer · nơi hard-code định dạng
- **Ràng buộc ngầm** (Bước 4) — dữ liệu dùng chung · thứ tự cron/batch · giả định về dữ liệu · đường vào khác · vai trò khác · **khác biệt giữa môi trường**
- **Bán kính R1–R4** (Bước 5) — quyết định độ sâu kiểm bắt buộc, chấm theo mức lan toả **không phải theo số dòng sửa**
- **Hành vi phải giữ nguyên** (Bước 7) — mốc cho self-test, UT và tester

Kết quả: `impact.md` đủ 8 mục theo mẫu trong file method — mỗi item kèm evidence (`file:line`), **và mỗi item trỏ được sang một lưới kiểm**. Nghi ngờ rồi loại thì ghi vào mục 8 kèm lý do. **Im lặng ≠ đã kiểm tra.**

## Bước 4 — Ghi kết quả

- Có `tasks/{TICKET-ID}/` → fill `01-discovery/current-state.md` (bảng survey + gap analysis ✅ reuse / ⚠ update / 🆕 new / ❌ conflict); phần dependency walk ghi vào `01-discovery/impact.md`. Chưa có workspace → đề nghị chạy `task-init` (cùng plugin) hoặc in ra chat nếu user chỉ cần nhanh.
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
