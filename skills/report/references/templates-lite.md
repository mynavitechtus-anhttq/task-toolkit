# Report Templates — LITE (mặc định)

Bản rút gọn, theo mẫu TechTus (`techtus/templates/report`, `techtus/templates/ticket-specs` trong MST System Docs). Dùng khi `format=lite` hoặc không nêu `format`. Bản đầy đủ 2 tầng: [`templates.md`](templates.md) (`format=full`).

**Khác bản full:**

- **Một tầng**, không có vạch `---`, không có mục `Chi tiết kỹ thuật (cho dev)`. Chi tiết kỹ thuật cần thiết (`file:line`, lệnh, log) đặt **ngay trong ô Evidence / Căn cứ** của dòng liên quan, không gom thành mục riêng.
- Không có mục `Refs` (trừ SPECS — ticket clear specs có Refs). Nguồn then chốt ghi trong ngoặc ngay tại claim.
- Mục **đánh số** `## 1.`, `## 2.`… để người đọc trỏ được ("xem mục 4").
- Mục không có nội dung thì **bỏ hẳn**, không để heading rỗng, không ghi "Không có". Ngoại lệ: `Ảnh hưởng & phạm vi` luôn có dòng "KHÔNG bị ảnh hưởng".

**Giữ nguyên từ bản full** (xem `templates.md`): tone theo locale, quy tắc trình bày (icon tối thiểu, gạch đầu dòng, không ví von, không tự chế thuật ngữ), quy ước evidence `[Giả định — cách verify: …]`, giữ nguyên chuỗi UI sản phẩm. Pipeline thu evidence và gate **không đổi** — lite chỉ gọn phần trình bày, không gọn phần điều tra.

## Nhãn section theo locale (lite)

Nhãn chung với bản full (TL;DR, Nguyên nhân gốc, Chuỗi nguyên nhân, Ảnh hưởng & phạm vi, Kết luận, Căn cứ, Fix & phòng tái diễn, Phát hiện ngoài phạm vi) dùng bảng trong `templates.md`. Nhãn riêng của lite:

| Khối | vn | en | ja |
|---|---|---|---|
| So sánh phương án | So sánh phương án | Comparing the options | 方式の比較 |
| Kế hoạch thực hiện | Kế hoạch thực hiện | Execution plan | 実施計画 |
| Việc nhờ khách hỗ trợ | Việc nhờ khách hỗ trợ | What we need from the client | お客様へのご依頼事項 |
| Hiện trạng / yêu cầu | Hiện trạng / yêu cầu | Current state / requirement | 現状 / 要件 |
| Solutions | Solutions | Solutions | Solutions |
| Impact & risk | Impact & risk | Impact & risk | Impact & risk |
| Acceptance criteria | Acceptance criteria | Acceptance criteria | 受入基準 |
| Open question | Open question | Open questions | 未解決の質問 |
| Kết quả & bằng chứng | Kết quả & bằng chứng | Results & evidence | 結果とエビデンス |
| Rủi ro còn mở | Rủi ro còn mở | Open risks | 残存リスク |

Nhãn bảng TL;DR (BUG): vn `Mục | Nội dung` — `Nguyên nhân gốc`, `Ảnh hưởng`, `Trạng thái`, `Cần quyết định` · en `Item | Content` — `Root cause`, `Impact`, `Status`, `Decision needed` · ja `項目 | 内容` — `根本原因`, `影響`, `ステータス`, `要判断事項`.

---

## Template BUG (lite)

```markdown
# [BUG] <title>

## 1. TL;DR
| Mục | Nội dung |
|---|---|
| Nguyên nhân gốc | <1 câu> |
| Ảnh hưởng | <ai, môi trường nào, data nào — từ bao giờ, mức độ> |
| Trạng thái | <có workaround chưa, fix khi nào, đã hồi phục chưa> |
| Cần quyết định | <ai quyết, hạn khi nào — bỏ dòng nếu không có> |

## 2. Nguyên nhân gốc
- <chuyện gì sai>
- <vì sao nó xảy ra được>
- <vì sao không bị chặn lại>

## 3. Chuỗi nguyên nhân (5 Whys)
| # | Tầng | Nguyên nhân | Evidence |
|---|---|---|---|
| 1 | Hiện tượng | <sự cố đo được: cái gì, lúc nào, bao nhiêu> | <job / log / số liệu> |
| 2 | Trực tiếp | <code hoặc config nào gây ra ngay lúc đó> | <`file:line`, log> |
| 3 | Trung gian | <điều kiện nào cho phép nó xảy ra> | <…> |
| 4 | Quy trình | <bước làm việc nào để lọt> | <…> |
| 5 | Hệ thống — root cause | <thiếu checklist, test, gate, tool hay policy gì> | <…> |

## 4. Ảnh hưởng & phạm vi
- Bị ảnh hưởng: <env / màn hình / user / data>
- KHÔNG bị ảnh hưởng: <chiều ngược lại + lý do>
- Data có hỏng không, có cần backfill không: <…>

## 5. Fix & phòng tái diễn
- Fix: <PR / commit / hành động>
- Rollback: <đường lui>
- Phòng tái diễn: <thay đổi process / tool / policy — không phụ thuộc người tự nhớ>

## 6. Phát hiện ngoài phạm vi
- <thứ tình cờ phát hiện, không thuộc issue này — repro ngắn + đề xuất tách ticket>
```

## Template INVESTIGATION (lite)

```markdown
# [INVESTIGATION] <câu hỏi cần trả lời>

## 1. Kết luận
- <trả lời thẳng câu hỏi, 2–4 gạch đầu dòng>
- <khuyến nghị, nếu là đề xuất>

## 2. So sánh phương án
| # | Phương án | Ưu điểm | Nhược điểm | Effort | Đề xuất chọn | Lý do chọn |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  | ✅ |  |
| 2 |  |  |  |  |  |  |

## 3. Căn cứ
- <fact> (nguồn: `file:line` / lệnh / doc)
- [Giả định — cách verify: …] <điều chưa chắc>

## 4. Ảnh hưởng & phạm vi
- Bị ảnh hưởng: <…>
- KHÔNG bị ảnh hưởng: <… + lý do>

## 5. Kế hoạch thực hiện
| Bước | Nội dung | Thời điểm đề xuất | Downtime | Rollback |
|---|---|---|---|---|
| 1 |  |  |  |  |
- Deadline, nếu khách hoặc vendor đặt: <ngày + hậu quả nếu trễ>
- Điều kiện hoãn: <…>

## 6. Việc nhờ khách hỗ trợ
- Cấp quyền: <…>
- Setting: <…>
- Thông tin cần cung cấp: <…>

## 7. Phát hiện ngoài phạm vi
- <…>
```

Mục 2 chỉ có khi là đề xuất / so sánh; mục 5 chỉ có khi là đối ứng vận hành hoặc thay đổi quy trình; mục 6 chỉ có khi cần khách làm gì.

## Template SPECS (lite) — nội dung ticket clear specs

Chốt **làm gì** và **vì sao**. Phần **làm thế nào** (bước triển khai, Definition of Ready) thuộc ticket task — skill `backlog-ticket`, không viết ở đây. Nguồn: `analyze-spec` (requirements, Input Contract, open questions, `technical-approach.md`) + `task-survey` (`current-state.md`, `impact.md`) — đọc thẳng, không khảo sát lại.

```markdown
# [SPECS] <title>

## 1. Hiện trạng / yêu cầu

**Hiện trạng:** <hệ thống đang làm gì — kèm nguồn `file:line` khi then chốt>

**Yêu cầu:** <khách muốn thành thế nào>

## 2. Solutions

**Phương án:** <một phương án thì nêu thẳng>

Từ 2 phương án trở lên thì so sánh và nêu lý do chọn:

| # | Phương án | Ưu điểm | Nhược điểm | Estimate sơ bộ | Đề xuất chọn | Lý do chọn |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  | ✅ |  |
| 2 |  |  |  |  |  |  |

## 3. Impact & risk

**Phạm vi:**

| Phạm vi | Bị ảnh hưởng | Ghi chú |
|---|---|---|
| <màn hình / chức năng / repo> | ✅ | <…> |
| <…> | ❌ | <lý do không ảnh hưởng> |

**Risk:**

| Risk | Mức độ | Khi nào xảy ra |
|---|---|---|
|  |  |  |

## 4. Acceptance criteria

<Mỗi AC có mã `AC-xx`, pass / fail được. Chọn dạng theo bảng dưới; một ticket có thể trộn dạng.>

- [ ] AC-01: <bối cảnh> + <thao tác> → <kết quả quan sát được>

## 5. Open question

| # | Câu hỏi | Hỏi ai | Hạn | Trạng thái |
|---|---|---|---|---|
| 1 |  |  |  | Đang chờ |

## 6. Phát hiện ngoài phạm vi
- <…>

## Refs
- Design: <…>
- Ticket khách: <…>
- Official doc: <…>
```

**Acceptance criteria — chọn dạng nào** (theo `techtus/templates/ticket-specs` § Viết Acceptance criteria thế nào):

| Dạng | Dùng khi | Cách viết |
|---|---|---|
| **Checklist** (mặc định) | Quy tắc đơn giản: validation, hiển thị, giới hạn giá trị, luồng cũ không đổi | `AC-xx: [bối cảnh] + [thao tác] → [kết quả quan sát được]` |
| **Given–When–Then** | Kết quả phụ thuộc trạng thái trước khi thao tác (tin hết hạn, user đã login…) | Code block `gherkin`, một kịch bản một hành vi, 3–5 bước, dòng đầu là `AC-xx: <tên hành vi>` |
| **Bảng quyết định** | Từ 2 điều kiện trở lên kết hợp, mỗi tổ hợp một kết quả | Dòng `AC-xx: <tên quy tắc>` rồi bảng: mỗi điều kiện một cột, cột cuối là kết quả, `Bất kỳ` khi không ảnh hưởng. Quá ~10 dòng → cân nhắc tách ticket |

Quy tắc AC ở SPECS:

- 3–7 AC — **phạm vi nghiệm thu**, không phải test case; không liệt kê đủ nhánh và data (để ở ticket task / test case).
- Rà các nhóm, chỉ ghi nhóm liên quan: luồng thành công · dữ liệu sai · giá trị biên · quyền · lỗi hệ thống · luồng cũ không đổi.
- Kết quả **quan sát được** (người dùng thấy / dữ liệu nhận được), không mô tả code bên trong ("không gọi API" → "form không được gửi").
- Điều chưa chốt → mục 5 Open question, **không** viết thành AC. Lấy từ open questions của `analyze-spec`.
- Yêu cầu chung mọi ticket (review, test hồi quy, deploy) thuộc DoD — không chép vào AC.

## Template TASK (lite)

```markdown
# [TASK] <title>

## 1. TL;DR
| | |
|---|---|
| Trạng thái | Done / Đang làm / Blocked |
| Đã xong | <kết quả đo được, không phải "đã làm"> |
| Còn lại / blocker | <gì, chờ ai> |
| Next | <bước kế + thời điểm> |

## 2. Kết quả & bằng chứng
| Hạng mục | Kết quả | Evidence |
|---|---|---|
| <deploy / test / số liệu> | <pass / fail / before → after> | <link, log, số> |

## 3. Rủi ro còn mở
- <risk + biện pháp cụ thể đang có>

## 4. Phát hiện ngoài phạm vi
- <…>
```
