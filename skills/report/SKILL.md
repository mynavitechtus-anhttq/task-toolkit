---
name: report
description: >-
  Entrypoint/orchestrator of task-toolkit: generate a standardized, conclusion-first report for a
  task/issue/bug by running a mandatory evidence pipeline — task-survey (source dig + dependency walk),
  system reverse-engineering when the architecture is unfamiliar (discovery-method.md), technical
  diagnosis for bugs whose cause is not yet proven (the debug skill), then 5-Whys RCA for bugs
  (rca-method.md) — then gate against checklists and render a two-tier report (non-tech on top,
  dev detail below) in VN (default) / EN / JA, with export to md/docx/pdf/xlsx. Trigger on "viết report",
  "báo cáo bug", "report bug/issue/task", "điều tra issue", "root cause", "tổng hợp kết quả điều tra",
  "báo cáo cho khách", "レポート作成", or when the user pastes a bug/issue/task title and asks for
  analysis + write-up. "report help" prints the skill map without running anything. Works in ANY repo —
  project specifics discovered at runtime. Does not draft tickets or PR descriptions inline — after
  analysis it can hand off to the backlog-ticket skill (STAGE 6: ticket + estimation). Not for
  test-case authoring.
---

# Report — Entrypoint & Orchestrator

> Ngôn ngữ giao tiếp: tiếng Việt. Ngôn ngữ report theo `locale` — **hỏi user nếu lệnh không nêu**, mặc định `vn` khi user không chọn. Nhãn section + tone xem `templates.md`.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Viết report điều tra chuẩn: **kết luận đứng trước** (BLUF), 2 tầng độc giả (non-tech trên / dev dưới). Quy ước evidence: claim đã verify là mặc định (ghi nguồn trong ngoặc khi then chốt); claim CHƯA verify bắt buộc đánh dấu **[Giả định — cách verify: …]**. Report chỉ đáng tin bằng evidence nuôi nó — vì vậy pipeline dưới đây là **bắt buộc**, không phải tùy chọn.

## Help — bản đồ bộ skill

> User gõ `report help` / `/task-toolkit:report ?` / "report làm được gì" → **in nguyên khối này** (không chạy gì), rồi hỏi muốn bắt đầu ở đâu.

```
/task-toolkit:report <title|mô tả> [locale=vn|en|ja] [audience=internal|customer]

FULL LIFECYCLE (bộ task-toolkit — mỗi stage tái dùng artifact stage trước, không điều tra lại):
  task-init → [discovery] → task-survey → analyze-spec (làm rõ input, grounded)
           ├─ BUG      → [debug] → RCA 5-Whys → report → planning (kế hoạch fix) → backlog-ticket
           └─ FEATURE  → planning (WBS + checklist) → backlog-ticket   (report tùy chọn)
  [...] = có điều kiện:  discovery khi CHƯA có bản đồ kiến trúc (repo lạ/legacy/multi-repo)
                         debug     khi type=BUG và nguyên nhân kỹ thuật CHƯA được chứng minh
  Vị trí planning khác nhau theo type: BUG lên kế hoạch fix SAU khi report chốt root cause;
  FEATURE chia WBS ngay sau analyze-spec.
  (analyze-spec chạy cho mọi task; report là 1 stage; các skill gọi lẻ được — xem GỌI LẺ bên dưới)

PIPELINE (tự chạy theo type):
  STAGE 1  task-init          workspace tasks/{ID}/ (chỉ khi cần mà chưa có)
  STAGE 2  evidence           theo domain: code → task-survey | infra/cloud → CLI/IaC/vendor docs
                              | CI-CD/process → workflow + run history | requirement → spec/PR tham chiếu
                              | vendor notice → notice + tra chéo official docs
           Discovery          (chưa có bản đồ kiến trúc) dựng project context +  [discovery-method.md]
                              kiến trúc TRƯỚC khi survey — áp cho MỌI type
  STAGE 3  phân tích theo type
           BUG               [debug] chẩn đoán → Immediate Cause đã verify       [skill debug]
                             → RCA 5-Whys 3 tầng → root cause hệ thống           [rca-method.md]
           INVESTIGATION     bảng options (Được/Mất/Effort → khuyến nghị)
           TASK              kết quả đo được kèm evidence
  STAGE 4  gate               3 checklist trong checklists.md — fail thì quay lại
  STAGE 5  render + export    template theo type + locale; audience=customer →
                              pass thẩm định report-reviewer + rà redact PII

TYPE tự nhận diện:
  BUG            lỗi/sự cố/regression        → root cause trước    (templates.md §BUG)
  INVESTIGATION  câu hỏi/đề xuất/so sánh     → kết luận trước      (templates.md §INVESTIGATION)
  TASK           tiến độ/hoàn thành          → trạng thái trước    (templates.md §TASK)

GỌI LẺ TỪNG PHẦN (không cần full report):
  task-init <ID>          chỉ tạo workspace
  task-survey <ID|mô tả>  chỉ khảo sát + impact
  analyze-spec <input>    làm rõ input MỌI task (feature→requirements | bug→expected vs actual), GROUNDED by survey
  debug <mô tả bug>       chẩn đoán kỹ thuật → Immediate Cause đã verify + option fix + estimate
                          (KHÔNG sửa code; tái dùng analyze-spec/survey, không hỏi lại)
  planning <ID|mô tả>     chia WBS overview + checklist tiến độ (từ survey/spec, KHÔNG điều tra lại)
  "chỉ chạy 5 whys ..."   chỉ chạy RCA theo rca-method.md, trả chuỗi nguyên nhân
  "soát report này ..."   chạy pass thẩm định theo agents/report-reviewer.md
  backlog                 sau analysis → sinh backlog ticket(s) + estimation
                          (skill backlog-ticket, TÁI DÙNG current-state.md/impact.md)
  release-note <a>..<b>   PER-RELEASE (N ticket), NGOÀI pipeline per-task: release note +
                          deployment runbook, auto matrix ảnh hưởng từ diff, song ngữ EN/JA

XUẤT FILE: .md (mặc định) | .docx | .pdf | .xlsx/.csv (bảng) — xem §Xuất file
```

## Routing (áp dụng theo thứ tự)

| Tín hiệu từ user | Hành động |
|---|---|
| `help` / `?` / "làm được gì" | In bản đồ trên, không chạy gì |
| Chỉ định thẳng 1 phần ("chỉ survey", "chỉ chạy 5 whys", "chỉ tạo workspace", "soát report này") | Làm đúng phần đó, không chạy pipeline |
| "báo cáo tiến độ / task X xong chưa" | Type TASK — đọc thẳng workspace (plan/notes/impact), KHÔNG survey lại |
| Có title bug/issue + muốn report | Full pipeline theo type |
| Intent chưa rõ (thiếu type/env/timeframe) | Hỏi 1 lượt duy nhất gộp mọi thứ thiếu |
| **`locale` không được nêu** | **Hỏi**, gộp chung lượt hỏi ở trên: *"Report viết bằng ngôn ngữ nào? `vn` (mặc định) · `en` · `ja`"*. User trả lời rỗng → `vn`. Đã nêu `locale=` trong lệnh → **không hỏi lại** |

## Pipeline chi tiết

### STAGE 1 — Workspace (điều kiện)
Có `TICKET-ID` và cần lưu artifact → nếu `tasks/{ID}/` chưa có, chạy `task-init` (bản riêng của repo tự thắng nếu có). User chỉ cần report nhanh trong chat → bỏ qua, artifact giữ in-context.

### STAGE 2 — Evidence collection (BẮT BUỘC cho mọi report; nguồn tùy domain)

**Cổng vào — có bản đồ kiến trúc chưa?** (áp cho MỌI type, không riêng bug hay feature)

- **Chưa** (repo lạ / legacy / multi-repo / không biết cái gì nói chuyện với cái gì) → chạy **`discovery-method.md`** TRƯỚC: Project Context (Step 0) → chọn hướng đào → Information Source Catalog → trình user xác nhận suy luận. Có bản đồ rồi mới survey được đúng chỗ.
- **Rồi** → đi thẳng bảng dưới.

> `task-survey` giả định **đã hiểu repo**, chỉ khảo path quanh 1 task; `discovery` bắt đầu từ chỗ **chưa** có bản đồ. Nhầm thứ tự → survey ra một mớ path rời rạc không ghép được thành flow.
>
> Ngoại lệ: khi câu hỏi điều tra **chính là** "hệ thống này chạy thế nào", discovery vừa là evidence vừa là kết luận — output của nó đi thẳng vào report (STAGE 5), không cần STAGE 3.

Xác định issue thuộc domain nào rồi thu evidence theo bảng — 1 issue có thể thuộc nhiều domain (thu đủ các nguồn liên quan):

| Domain của issue | Nguồn evidence | Cách thu |
|---|---|---|
| **Code/behavior trong repo** | source, git history, config | chạy `task-survey` (bản riêng của repo thắng nếu có): source dig + dependency walk. Repro/bác bỏ bằng chạy thật; timeline qua `git log -S`/`blame` |
| **Infra/cloud** (AWS/GCP notice, resource, network) | CLI read-only (`aws elasticache describe-*`, `describe-events`…), IaC repo (CDK/Terraform), console (nhờ user chụp/xác nhận), **official docs của vendor** về đúng sự kiện/service đó | Query được gì thì query; KHÔNG có quyền truy cập → ghi `[Giả định]` + đưa yêu cầu cụ thể vào mục "Việc khách/team cần làm" (vd "cần confirm maintenance window trên console") |
| **CI/CD & quy trình vận hành** (release flow, schedule, rule) | workflow files, run history (`gh run list`/`api`), branch protection, quy ước team, lịch nghỉ lễ | Đọc hiện trạng THẬT trước khi đề xuất thay đổi; điểm nào là "luật bất thành văn" → hỏi user/stakeholder |
| **Yêu cầu mới từ khách** (feature/batch request) | nội dung yêu cầu, spec/PR tham chiếu (kể cả repo khác — đọc qua `gh`), hệ thống tương tự đã có | Trích xuất: yêu cầu rõ / yêu cầu suy ra / **open questions cần khách confirm** (3 nhóm tách bạch); đối chiếu tham chiếu thật, không đoán từ mô tả |
| **Email/notice từ bên thứ 3** (AWS Health, vendor EOL…) | nguyên văn notice + tra chéo trang chính thức của vendor (health dashboard, doc sự kiện) | Rút ra: deadline, phạm vi resource bị ảnh hưởng (đối chiếu inventory thật của mình), hành động vendor yêu cầu, hậu quả nếu bỏ qua |

- Đã có artifact tươi trong workspace (`current-state.md`/`impact.md`) → dùng luôn, không thu lại.
- **Artifact contract**: mọi claim trong report phải trace về evidence đã thu ở stage này (lệnh/log/doc/URL). Report KHÔNG tự bịa evidence ngoài pipeline.
- Nguồn nào không tiếp cận được trong môi trường hiện tại → không đoán: ghi `[Giả định — cách verify]` và biến nó thành action trong "Việc khách/team cần làm".

### STAGE 3 — Phân tích sâu theo type

**BUG** → hai bước, đúng thứ tự:

1. **[debug]** — chỉ khi Immediate Cause **chưa được chứng minh** ở STAGE 2. Gọi skill **`debug`**: triage (môi trường/blast radius/dữ liệu/tái hiện) → instrument ranh giới component để biết hỏng ở ĐÂU → đối chiếu chỗ đang chạy đúng → vòng lặp 1 giả thuyết + 1 lệnh verify → chốt **Immediate Cause có evidence** + bảng option fix kèm estimate. Skill này **không sửa code**. STAGE 2 đã lộ nguyên nhân (vd lệch khai báo CI↔Dockerfile) → **bỏ qua**, đưa thẳng nguyên nhân đó xuống bước 2.
2. **RCA 5 Whys 3 tầng** theo **`rca-method.md`** (cùng thư mục): Problem Statement đo được → Facts & Timeline → chuỗi Why 3 tầng (Immediate → Process → System Gap) với 3 luật (không dừng ở con người / counterfactual / branching) → chốt root cause tầng hệ thống. **Layer 1 lấy từ bước 1, không dựng lại.** Khi facts phải lấy từ người (user/stakeholder) → dùng kỹ thuật phỏng vấn 5W1H + Decision Context trong method, **báo user 1 câu trước khi bắt đầu hỏi**.

> Cách hỏi khác nhau giữa hai bước, cố ý: `debug` gộp toàn bộ câu hỏi vào **1 lượt** (tìm sự thật kỹ thuật, cần nhanh); RCA hỏi **từng câu một** (đào bối cảnh ra quyết định, cần sâu).

- **INVESTIGATION** → bảng options (Được/Mất/Effort → khuyến nghị) trên nền evidence STAGE 2. Hệ thống lạ/legacy/multi-repo thì bản đồ kiến trúc đã dựng ở STAGE 2 (`discovery-method.md`) — dùng lại, không đào lại.
- **TASK** → kết quả đo được kèm evidence ("deploy xanh", "N/N test pass", before→after) — không phải danh sách hoạt động.
- **Bug cũ phát hiện giữa chừng** (pre-existing): KHÔNG lờ, KHÔNG âm thầm fix — ghi repro + evidence vào mục `Phát hiện ngoài phạm vi`, đề xuất tách ticket.

### STAGE 4 — Gate (fail → quay lại stage tương ứng)
Chạy đủ 3 checklist trong `checklists.md`: điều tra đủ / kết luận đạt / văn bản đạt. Hard rules: claim không evidence → hạ ⚠ hoặc quay lại STAGE 2; root cause là "what" → quay lại STAGE 3; TL;DR > 5 dòng hoặc core > 1 trang → cắt.

### STAGE 5 — Render & giao
1. Template theo type + locale (`templates.md`); cấu trúc bất biến: `TL;DR` → tầng non-tech → `---` → `Chi tiết kỹ thuật` → `Refs`. Trình bày theo Quy tắc trong `templates.md`: icon tối thiểu (không emoji heading, không icon từng dòng), gạch đầu dòng thay đoạn văn, không ví von phi kỹ thuật, chỉ đánh dấu `[Giả định]` cho claim chưa verify.
2. `audience=customer` → (a) chạy **pass thẩm định độc lập** theo `../../agents/report-reviewer.md` (4 trục: chống anchoring, soát evidence, soát non-tech readability, đúng thể thức) — môi trường có agent system thì chạy agent `report-reviewer` trong context riêng, không có thì tự chạy như một pass tách biệt; pass chỉ góp ý, bạn/user quyết; (b) rà **redact**: tên cá nhân, credential, URL nội bộ → vai trò/`***`.
3. Lưu: có workspace → `tasks/{ID}/task-toolkit:report-<type>-<yyyymmdd>.md` + in chat; không → in chat + đề nghị chỗ lưu.
4. Giao 1 message: report + 1 dòng mời chỉnh (tone/độ dài/ngôn ngữ). Kèm khối bàn giao ngắn: stage nào đã chạy, artifact nằm đâu, còn ⚠ nào mở.

### STAGE 6 — Handoff (tùy chọn, sau khi giao report)

Analysis đã sinh `current-state.md`/`impact.md` (+ `debug-<date>.md` nếu có) — đúng thứ backlog ticket cần. Sau STAGE 5, **đề nghị 1 dòng**, không tự chạy khi user chưa yêu cầu:

| Type | Đề nghị | Vì sao |
|---|---|---|
| **BUG**, fix nhiều việc / nhiều file / cần migrate | `planning` (kế hoạch fix) → rồi `backlog-ticket` | Root cause vừa chốt xong mới lên được kế hoạch sửa đúng gốc; WBS ra nhiều item thì mỗi item 1 ticket |
| **BUG**, fix khu trú (option 🟢/🟡 trong bảng của `debug`) | thẳng `backlog-ticket` | WBS cho 1 dòng sửa là thừa |
| **INVESTIGATION / TASK** | thẳng `backlog-ticket` | Không có "kế hoạch fix" để lập |

Skill được gọi **đọc thẳng artifact vừa có, KHÔNG khảo sát lại**; `backlog-ticket` tái dùng luôn estimate 🟢→⚫ mà `debug` đã ước, không ước lại từ đầu. Đây là đường rẻ nhất từ điều tra → ticket có estimation.

### Xuất file (khi user yêu cầu "xuất pdf/docx/excel…")

Mặc định output là `.md`. Convert theo bảng — luôn convert TỪ file .md đã lưu (không viết lại nội dung):

| Định dạng | Cách làm | Ghi chú |
|---|---|---|
| `.md` | mặc định — `tasks/{ID}/task-toolkit:report-<type>-<yyyymmdd>.md` | nguồn chân lý |
| `.docx` | `pandoc report.md -o report.docx`; môi trường có skill/tool docx chuyên dụng thì dùng để có template đẹp | giữ nguyên bảng, heading |
| `.pdf` | `pandoc report.md -o report.pdf --pdf-engine=typst -V mainfont="Helvetica Neue" -V monofont="Menlo"` (engine: `brew install typst`; PHẢI truyền mainfont/monofont — thiếu sẽ lỗi "font fallback list must not be empty"; report có tiếng Nhật → thêm font CJK vd `-V mainfont="Hiragino Sans"`) | hoặc skill/tool pdf của môi trường nếu có |
| `.xlsx` / `.csv` | report là văn bản nên chỉ export CÁC BẢNG (impact, kết quả, checklist); có tool xlsx thì dùng, không thì ghi CSV từng bảng | không nhét cả report vào Excel |

Sau convert: báo đường dẫn file + nhắc bản `.md` vẫn là bản gốc để sửa.

## Guardrails

- **[HARD]** Không viết report khi STAGE 2 chưa chạy — mọi domain (code, infra, process, requirement, vendor notice) đều phải thu evidence theo bảng routing trước; "tự tin nhưng sai" đến tay khách là failure mode đắt nhất.
- **[HARD]** Claim không evidence → bắt buộc đánh dấu `[Giả định — cách verify: …]`. Không có claim trần.
- **[HARD]** `audience=customer` → bắt buộc qua pass thẩm định report-reviewer + redact trước khi giao.
- **[HARD]** BUG: không chạy RCA khi Immediate Cause chưa có evidence — chưa có thì chạy `debug` trước. Layer 1 dựng trên phỏng đoán làm cả chuỗi Why sai theo, và không ai phát hiện được vì chuỗi vẫn đọc rất hợp lý.
- Pipeline **chẩn đoán, không sửa**: `debug` dừng ở option fix; report không chứa code fix. Việc sửa là task riêng sau khi user chốt option.
- Không kể chuyện điều tra theo thời gian; không trộn fix vào phần root cause; không dịch chuỗi UI sản phẩm.
- Phỏng vấn RCA (khi cần hỏi user) không tự chạy ngầm — báo user trước khi bắt đầu.
- Report ≠ ticket ≠ PR description — không tự viết ticket/PR *bên trong* report. Riêng backlog: sau khi analysis xong ĐƯỢC **đề nghị handoff** sang skill `backlog-ticket` (STAGE 6) — nó là skill riêng, tái dùng artifact; report không tự lồng nội dung ticket vào.
