---
description: "Bản đồ task-toolkit — plugin giúp gì, năm tình huống thường gặp đi qua flow nào, 8 skill làm gì. In hướng dẫn, không chạy điều tra."
---

# /task-toolkit:help

In bản đồ dưới đây cho user. **Không chạy skill nào, không điều tra gì.**

Nếu user hỏi kèm tình huống cụ thể ("tôi có con bug X thì gõ gì"), in bản đồ rồi chỉ thẳng dòng lệnh cho đúng tình huống đó.

---

## Plugin này làm gì cho bạn

Nó lo **cả quãng đường từ lúc nhận việc tới lúc bàn giao**: nhận một cái spec hoặc một con bug → khảo sát source thật → làm rõ yêu cầu → chẩn đoán nguyên nhân → chia kế hoạch → viết report → sinh ticket kèm estimate → và khi tới ngày deploy thì dựng release note.

Điểm khác biệt: **mọi kết luận phải có bằng chứng từ code thật**. Không đoán, không "có lẽ là". Và **mỗi khâu tái dùng kết quả khâu trước** — khảo sát một lần, dùng cho cả phân tích, kế hoạch, report lẫn ticket.

Tên lệnh giống nhau ở Claude Code và Codex: luôn là `task-toolkit:<skill>`.

---

## Bạn đang ở tình huống nào

### 1 · Vừa nhận một task mới, cần triển khai

Spec mới, tính năng mới, hoặc yêu cầu thay đổi từ khách.

```
/task-toolkit:report <mô tả task>
```

Nó tự đi: **khảo sát source** → **làm rõ yêu cầu** (tách Explicit / Inferred / Open, đối chiếu với code thật để bắt chỗ spec lệch hệ thống) → **chia WBS** → **báo cáo** → sẵn sàng sinh ticket.

Muốn đi từng bước thì gọi lẻ theo thứ tự:

```
/task-toolkit:task-init TICKET-123      ← tạo workspace, nếu cần lưu artifact
/task-toolkit:task-survey TICKET-123    ← khảo sát + phạm vi ảnh hưởng
/task-toolkit:analyze-spec <spec>       ← làm rõ yêu cầu, tìm chỗ spec mâu thuẫn code
/task-toolkit:planning TICKET-123       ← WBS + checklist tiến độ
/task-toolkit:backlog-ticket            ← ticket chuẩn công ty + estimate
```

### 2 · Có bug, cần tìm ra nguyên nhân

```
/task-toolkit:report <mô tả bug>
```

Nhánh BUG có thêm hai khâu mà nhánh task không có:

**Chẩn đoán kỹ thuật** — ⚠ *chỉ chạy khi cần*. Nếu khâu khảo sát đã lộ nguyên nhân rồi (ví dụ thấy khai báo trong CI lệch với Dockerfile) thì **bỏ qua luôn**, đưa thẳng nguyên nhân đó xuống bước sau. Còn chưa rõ thì mới khoanh vùng chỗ hỏng, đối chiếu với chỗ đang chạy đúng, mỗi lần một giả thuyết kèm một lệnh verify.

**5 Whys** — từ nguyên nhân trực tiếp đào tiếp xuống lỗ hổng hệ thống, để lần sau không tái diễn.

> **Nó không chạy một mạch rồi ném kết quả.** Cả hai khâu đều dừng lại hỏi bạn, khác kiểu và cố ý: `debug` gộp mọi câu hỏi vào **một lượt** (tìm sự thật kỹ thuật, cần nhanh), còn 5 Whys hỏi **từng câu một** và báo trước khi bắt đầu (đào bối cảnh ra quyết định, cần sâu).
>
> Trong `debug`, **bạn là người nêu giả thuyết**. Nó sinh lệnh verify cho giả thuyết *của bạn*, chạy, rồi trình kết quả thô — không diễn giải sẵn thành kết luận. Bạn đọc và tự phán.

Chỉ cần chẩn đoán, chưa cần report:

```
/task-toolkit:debug <mô tả bug>
```

> ⚠ **Skill này không sửa code.** Nó dừng ở nguyên nhân đã verify, kèm bảng các cách sửa và độ phức tạp từng cách. Bạn chọn, bạn sửa.

### 3 · Cần viết một bản report

Cho khách, cho nội bộ, hoặc để chốt một cuộc điều tra.

```
/task-toolkit:report <title> [locale=vn|en|ja] [audience=internal|customer]
```

Ba loại, nó tự nhận:

| Bạn gõ | Nó hiểu | Bố cục |
|---|---|---|
| `…report home page hiện count = 0 sau deploy` | **BUG** | Nguyên nhân gốc trước |
| `…report có nên migrate base image sang ECR khách không` | **INVESTIGATION** | Kết luận trước, rồi so sánh phương án |
| `…report tiến độ TICKET-123` | **TASK** | Trạng thái trước; đọc thẳng workspace, **không** khảo sát lại |

Report ra **hai tầng**: phần trên cho người không rành kỹ thuật, phần dưới cho dev. `locale=ja` thì tự dùng kính ngữ; `audience=customer` thì qua bước thẩm định và ẩn thông tin nhạy cảm.

### 4 · Có report rồi, cần soát trước khi gửi

```
"soát report này trước khi mình gửi khách"
```

Chạy một lượt thẩm định độc lập trên bốn trục: **bằng chứng có đủ không** · **kết luận có vượt quá bằng chứng không** · **người không rành kỹ thuật đọc có hiểu không** · **có chỗ nào lộ thông tin không nên gửi ra ngoài không**.

Chỉ **góp ý**, không chặn, không tự sửa. Quyết định cuối là của bạn.

### 5 · Tới ngày deploy, cần release note

Cho **cả một lần release nhiều ticket**, không phải một task lẻ.

```
/task-toolkit:release-note staging..main
```

Nó đọc diff của lần release, tự dựng **ma trận ảnh hưởng** (Frontend / Backend / AWS / Email / SMS / Data migration / Batch / Cache) từ đường dẫn file đã đổi, đánh giá có phải downtime không, rồi nháp các bước deploy · smoke test · rollback. Ra song ngữ **EN/JA**.

Ba thứ nó **không đoán** mà sẽ hỏi bạn một lượt: ngày giờ (JST), môi trường, và cách deploy.

---

## Bản đồ đầy đủ

```
                    ┌─────────────── nhận task / nhận bug ───────────────┐
                    ▼                                                    │
  task-init ──→ task-survey ──→ analyze-spec ──┬── BUG ──→ debug ──→ 5 Whys
  (nếu cần)      khảo sát        làm rõ input   │       (nếu cần)     RCA
                 dependency      đối chiếu code │                      │
                 walk            thật           └── TASK/FEATURE ──────┤
                                                                       ▼
                                        planning ──→ report ──→ backlog-ticket
                                         WBS +       2 tầng      ticket +
                                         checklist   VN/EN/JA    estimate
                                                        │
                                                        ▼
                                                  "soát report này"
                                                   thẩm định 4 trục

  release-note ── NGOÀI luồng trên, chạy lúc chuẩn bị deploy cho cả lần release
```

| Skill | Làm gì |
|---|---|
| `task-init` | Tạo workspace 6 file chuẩn cho ticket |
| `task-survey` | Đào source, dependency walk qua các repo liên quan → hiện trạng + phạm vi ảnh hưởng |
| `analyze-spec` | Làm rõ yêu cầu (feature) hoặc expected vs actual (bug), **đối chiếu với code thật** để bắt chỗ spec lệch hệ thống |
| `debug` | Chẩn đoán tới nguyên nhân trực tiếp **đã verify** + bảng option fix kèm estimate. **Bỏ qua nếu khảo sát đã lộ nguyên nhân.** Không sửa code |
| `planning` | Chia WBS + checklist tiến độ, tái dùng khảo sát — không điều tra lại |
| `report` | Orchestrator: chạy đủ pipeline theo loại task rồi viết report 2 tầng |
| `backlog-ticket` | Ticket chuẩn công ty + estimation có căn cứ từ khảo sát |
| `release-note` | Release note + runbook deploy cho cả lần release, song ngữ EN/JA |

Nói thẳng bằng lời cũng được, không cần nhớ tên lệnh:

```
"chỉ khảo sát thôi"        "chỉ chạy 5 whys cho sự cố X"
"chỉ tạo workspace"        "soát report này"
```

---

## Hai nguyên tắc chi phối cả plugin

**Không kết luận khi chưa có bằng chứng.** Mọi khẳng định quan trọng phải truy được về một dòng code, một lệnh đã chạy, hoặc một tài liệu cụ thể. Chưa chứng minh được thì đánh dấu là giả định, không viết thành câu khẳng định.

**Bạn nghĩ, nó gõ.** Ở mọi bước cần phán đoán — nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi — **người phụ trách quyết**. Bí thì nó đưa câu hỏi gợi mở, không đưa kết luận thay. Phần thao tác thì nó làm: grep, chạy lệnh verify, dựng bảng, soạn nháp theo template. Bạn soát từng dòng.

---

## Ngôn ngữ

**Không nêu `locale=` thì nó hỏi bạn** trước khi viết, gộp chung với những thứ còn thiếu khác thành một lượt hỏi duy nhất.

Cả `report` lẫn `backlog-ticket` mặc định **`vn`**, nhận thêm `en` · `ja`. Nêu sẵn trong lệnh (`locale=ja`) thì **không hỏi lại**.

## Xuất file

`.md` mặc định · `.docx` · `.pdf` · `.xlsx`/`.csv` cho bảng.

## Nếu lệnh không nhận

Trong Codex, tên lệnh là tên lối tắt do `install.sh` tạo. Nếu bản Codex đang dùng không nhận dấu `:`, cài lại với dấu gạch ngang:

```bash
TASK_TOOLKIT_SEP=- bash install.sh --codex
```

Cho ra `/task-toolkit-report`. Kiểm bản đã cài bất cứ lúc nào: `bash install.sh --verify`.
