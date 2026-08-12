# Cổng spec — chạy TRƯỚC mọi việc khác

> Dùng chung bởi `ut-design`, `ut-generate`. `ut-audit` không cần cổng này (nó chỉ đọc test đã có).

Playbook §0 bước 3 là **cổng spec**: không đủ spec để suy ra `expected` thì STOP. Cổng đó chỉ chặn được nếu biết spec ở đâu. Đây là bước biết.

⚠ **Đây là lý do plugin này tồn tại.** Không có spec thì vẫn viết được test — nhưng `expected` sẽ lấy từ code đang chạy, tức là **golden-by-implementation**, thứ playbook §1 cấm tuyệt đối. Bỏ qua bước này là sinh ra hàng loạt test trông xanh mà không chứng minh gì.

---

## Bước 1 — Dò trước, đừng hỏi trống

Trước khi hỏi, tự tìm. Hỏi "spec đâu?" khi file spec đang nằm ngay trong repo là làm phiền vô ích.

```bash
# artifact của các plugin cùng bộ
ls tasks/*/01-discovery/spec-analysis.md 2>/dev/null
ls openspec/changes/*/specs/*/spec.md 2>/dev/null
ls docs/superpowers/specs/*-design.md 2>/dev/null
# tài liệu rời hay gặp
ls docs/spec*.md docs/specs/*.md spec/*.md 2>/dev/null
```

Có kết quả → nêu **đường dẫn cụ thể** làm lựa chọn 1. Không có → lựa chọn 1 biến mất, bắt đầu từ 2.

## Bước 2 — Hỏi, một lần, đủ đường

> Để thiết kế UT tôi cần spec của unit — chính xác thì cần **`expected` suy từ đâu**, và **miền giá trị** để ra biên. Không có hai thứ đó thì test chỉ chép lại hành vi code hiện tại.
>
> *(nếu bước 1 tìm thấy)* Tôi thấy `tasks/TICKET-4821/spec-analysis.md` — dùng file này chứ?
>
> | | Bạn đang ở đâu | Làm gì |
> |---|---|---|
> | **1** | File tôi vừa tìm thấy đúng rồi | dùng luôn |
> | **2** | Có spec, nhưng ở chỗ khác | chỉ đường dẫn |
> | **3** | Spec ngắn, tôi dán vào đây | dán thẳng |
> | **4** | **Có tài liệu** (ticket, BRD, screen detail) nhưng rời rạc, chưa gom | → `task-toolkit` |
> | **5** | **Chỉ có ý tưởng**, chưa có tài liệu nào | → `sdd-techtus` |
> | **6** | Không có spec và cũng không định làm | → characterization ⚠ |

**Trục phân biệt 4 và 5 là *đã có tài liệu hay chưa*, không phải *code đã chạy hay chưa*.** `task-toolkit` làm rõ tài liệu sẵn có — kể cả cho tính năng chưa viết dòng code nào. `sdd-techtus` viết ra spec chưa từng tồn tại. Hỏi nhầm trục là đẩy người ta sang plugin sai.

Chọn xong thì **không hỏi lại**. Ghi lựa chọn vào output để người sau biết `expected` gốc ở đâu.

---

## Xử lý từng nhánh

### 1 · 2 · 3 — đã có spec

Đọc, rồi trả lời được **hai** câu trước khi đi tiếp:

| Cần | Không có thì |
|---|---|
| Suy ra `expected` cho từng case | STOP — `TODO(spec)`, playbook §7 |
| Miền giá trị (min/max, rỗng, độ dài) → nhóm B | Nhóm B thành `missing`, **không** được đoán |

Spec có nhưng thiếu miền giá trị là chuyện **rất** hay gặp — spec thường tả hành vi, không tả biên. Gặp thì nói thẳng: nhóm B sẽ hở, gợi ý bổ sung từ **schema DB** hoặc **API contract** (hai nguồn hợp lệ còn lại).

### 4 — có tài liệu, chưa gom → `task-toolkit`

Kiểm ba trạng thái, **chỉ khi** người dùng chọn nhánh này:

```bash
ls ~/.claude/plugins/*/task-toolkit ~/claude-plugins/task-toolkit 2>/dev/null
ls tasks/*/01-discovery/spec-analysis.md 2>/dev/null
```

| Trạng thái | Nói gì |
|---|---|
| Đã cài **và** có `spec-analysis.md` | chỉ file, quay lại nhánh 1 |
| Đã cài, chưa có artifact | chạy `/task-toolkit:analyze-spec`. ⚠ **Nó read-only mặc định — in ra chat rồi thôi.** Phải bảo nó lưu `tasks/{ID}/01-discovery/spec-analysis.md`, không thì quay lại đây vẫn tay trắng |
| Chưa cài | đưa lệnh cài, **không tự cài** |

```bash
claude plugin marketplace add https://github.com/mynavitechtus-anhttq/task-toolkit
claude plugin install task-toolkit@task-toolkit
```

Cái lấy được từ `spec-analysis.md`, đúng hai chỗ:

- **§4 Requirements + scenario `WHEN…THEN`** → nguồn suy `expected` (nhóm A, C, D, E)
- **§5 Input Contract** → nguồn ra biên (nhóm B) — cột `Miền hợp lệ` và `Giá trị đặc biệt` map thẳng vào B1/B2/B3/B4

Còn `[BLOCKER]` chưa đóng → những REQ dính BLOCKER **không** sinh test, ghi `TODO(spec)`. REQ khác vẫn chạy bình thường; đừng chặn cả task vì một câu hỏi.

### 5 — chỉ có ý tưởng → `sdd-techtus`

```bash
ls ~/.claude/skills/sdd-techtus ~/claude-plugins/skill-sdd-techtus 2>/dev/null
command -v openspec
```

Chưa cài thì đưa lệnh, không tự chạy:

```bash
npm install -g @fission-ai/openspec@latest
git clone https://github.com/mynavitechtus-thachlh/skill-sdd-techtus ~/claude-plugins/skill-sdd-techtus
bash ~/claude-plugins/skill-sdd-techtus/install.sh --link
```

Nói trước cho đúng kỳ vọng: nhánh này **dài hơn hẳn** — brainstorm, viết spec, người duyệt, rồi mới sinh OpenSpec artifact. Không phải mười phút. Đổi lại là spec thật, có người chốt.

Xong thì `openspec/changes/<name>/specs/<capability>/spec.md` — khối `#### Scenario:` `- **WHEN**` `- **THEN**` map thẳng sang Given–When–Then của viewpoint. Đây là nhánh cho `expected` sạch nhất, vì spec được viết ra *trước* code.

### 6 — không có spec: characterization ⚠

Chỉ đi nhánh này khi người dùng **hiểu và chấp nhận** đánh đổi. Nói đủ, đừng nói khéo:

> Không spec thì `expected` chỉ có thể lấy từ hành vi code hiện tại. Việc đó có tên: **characterization test** — chụp lại hành vi đang có để lần sau sửa mà lệch thì biết.
>
> **Nó không kiểm tra được code đúng hay sai.** Code đang có bug thì test sẽ đóng băng luôn cái bug đó thành "hành vi mong muốn", và người sửa bug về sau sẽ thấy test đỏ rồi tưởng mình làm hỏng.
>
> Đây đúng là thứ playbook §1 gọi là **golden-by-implementation** và cấm. Chạy được, nhưng phải đánh dấu rõ và không được coi là UT đã xong.

Chấp nhận thì đổi luật, ba chỗ:

1. Mọi test gắn thêm `// characterization: expected chụp từ hành vi hiện tại, CHƯA đối chiếu spec`
2. Bảng truy vết đổi `covered` → **`characterized`**. Không có ô nào được ghi `covered` — cột đó dành cho test suy từ spec.
3. Output mở đầu bằng cảnh báo, kèm câu: *"cần soát lại khi có spec"*.

Không chấp nhận → quay lại menu.

---

## Ghi lại nguồn (bắt buộc)

Mọi output của `ut-design` và `ut-generate` phải mở đầu bằng:

```markdown
> **Nguồn spec:** `tasks/TICKET-4821/spec-analysis.md` §4 + §5 (task-toolkit, 2026-08-06)
> **Độ tin `expected`:** suy từ spec · **Miền giá trị:** có, từ Input Contract
```

Ba dạng `Độ tin` — *suy từ spec* / *một phần* / *characterization ⚠*. Người review nhìn một dòng là biết bộ test này chứng minh được gì, và đó là điều họ cần biết trước tiên.
