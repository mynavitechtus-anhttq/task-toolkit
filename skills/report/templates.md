# Report Templates — BUG / INVESTIGATION / TASK

## Nhãn section theo locale

Cấu trúc không đổi giữa các ngôn ngữ — chỉ đổi nhãn. Chuỗi UI sản phẩm, file path, class/method, URL **không bao giờ dịch**.

| Khối | vn (default) | en | ja |
|---|---|---|---|
| TL;DR | TL;DR | TL;DR | 要点 |
| Nguyên nhân gốc | Nguyên nhân gốc | Root Cause | 根本原因 |
| Chuỗi nguyên nhân | Chuỗi nguyên nhân (5 Whys) | Cause chain (5 Whys) | 原因の連鎖（なぜなぜ分析） |
| Ảnh hưởng & phạm vi | Ảnh hưởng & phạm vi | Impact & Scope | 影響範囲 |
| Kết luận | Kết luận | Conclusion | 結論 |
| So sánh phương án | So sánh phương án | Options | 選択肢の比較 |
| Căn cứ | Căn cứ (evidence) | Evidence | 根拠 |
| Fix & phòng tái diễn | Fix & phòng tái diễn | Fix & Prevention | 対応と再発防止 |
| Kết quả | Kết quả & bằng chứng | Results & Evidence | 結果とエビデンス |
| Việc các bên | Việc khách/team cần làm — việc mình lo | Your side / our side | ご依頼事項・弊社対応 |
| Phát hiện ngoài phạm vi | Phát hiện ngoài phạm vi | Out-of-scope findings | 対象外の検出事項 |
| Chi tiết kỹ thuật | Chi tiết kỹ thuật (cho dev) | Technical Detail | 技術詳細 |
| Tham chiếu | Refs | Refs | 参考資料 |

**Tone theo locale (bắt buộc):**

- **JA**: Write in Japanese, formal tone, short and easy to understand for both technical and non-technical Japanese readers. `audience: internal` → です・ます đơn giản; `audience: customer` → keigo chuẩn thư tín (いたします/おります), mở đầu 「お世話になっております。」khi là văn bản gửi trực tiếp.
- **VN**: Viết bằng tiếng Việt, giọng văn trang trọng, ngắn gọn, dễ hiểu cho cả người đọc có kỹ thuật và không chuyên về kỹ thuật.
- **EN**: Write in English, formal tone, short and easy to understand for both technical and non-technical readers.

**Quy tắc trình bày (mọi template):**

- **Icon tối thiểu.** Không emoji ở heading. Không gắn icon từng dòng.
- **Evidence**: claim đã verify là mặc định — không cần đánh dấu, chỉ ghi nguồn trong ngoặc khi then chốt `(job 123, log dòng 61)`. Claim CHƯA verify bắt buộc đánh dấu **[Giả định — cách verify: …]**. Nhìn lướt report: chỗ nào không có [Giả định] nghĩa là đã có evidence.
- **Không ví von phi kỹ thuật** ("cửa hàng", "cánh cửa", "tảng băng"…). Phần cho người non-tech = tiếng Việt phổ thông + thuật ngữ IT giữ nguyên, kèm giải thích ngắn trong ngoặc khi cần (vd "PECL (kho phân phối extension chính thức của PHP)").
- **Gạch đầu dòng thay cho đoạn văn** ở mọi phần giải thích; đoạn văn chỉ dùng khi lập luận cần liền mạch, tối đa 3-4 câu.
- **Không tự chế thuật ngữ/tên gọi mới** (kể cả dịch từ tiếng Anh: "counterfactual", "litmus test", "phép thử X"…). Các bước kiểm tra của phương pháp viết thẳng thành CÂU HỎI đầy đủ trong report — vd: "Nếu người khác làm, lỗi có xảy ra không?", "Biện pháp này có phụ thuộc con người tự nhớ không?" — người đọc hiểu ngay không cần định nghĩa.

---

## Template BUG (root cause trước)

```markdown
# [BUG] <title>

## TL;DR
| | |
|---|---|
| Nguyên nhân gốc | <1 câu> |
| Ảnh hưởng | <ai/env/data, từ bao giờ, mức độ> |
| Trạng thái | <workaround? fix ETA? đã hồi phục?> |
| Cần quyết định | <nếu có — ai, deadline> |

## Nguyên nhân gốc
- <gạch đầu dòng: chuyện gì sai — thuật ngữ IT giữ nguyên, giải thích ngắn trong ngoặc nếu cần>
- <vì sao nó xảy ra được>
- <vì sao không bị chặn lại (gap quy trình/hệ thống)>

## Chuỗi nguyên nhân (5 Whys)
| # | Tầng | Nguyên nhân | Evidence |
|---|---|---|---|
| 1 | Hiện tượng | <sự cố đo được: cái gì, lúc nào, bao nhiêu> | <job/log/số liệu> |
| 2 | Trực tiếp | <code/config nào gây ra ngay lúc đó> | <file:line / log> |
| 3 | Trung gian | <điều kiện nào cho phép nó> | <…> |
| 4 | Quy trình | <bước làm việc nào để lọt> | <…> |
| 5 | Hệ thống — ROOT CAUSE | <thiếu checklist/test/gate/tool/policy gì> | <…> |

Kiểm tra lỗi hệ thống hay lỗi cá nhân: nếu người khác làm, lỗi có xảy ra không? → CÓ = lỗi hệ thống, không phải lỗi cá nhân
<Nhánh phụ nếu 1 why có nhiều nguyên nhân: mỗi nhánh 1 bảng riêng>

## Ảnh hưởng & phạm vi
- Bị ảnh hưởng: <env/màn hình/user/data>
- KHÔNG bị ảnh hưởng: <chiều ngược lại + lý do>
- Data hỏng? cần backfill?

## Fix & phòng tái diễn
- Fix: <PR/commit/hành động> | Rollback: <đường lui>
- Phòng tái diễn: <thay đổi process/tool/policy — kiểm tra: "biện pháp này có phụ thuộc con người tự nhớ / tự cẩn thận không?" — nếu có thì chưa đạt>

## Phát hiện ngoài phạm vi (nếu có)
- <bug/issue có sẵn tình cờ phát hiện: repro ngắn + đề xuất tách ticket>

---
## Chi tiết kỹ thuật (cho dev)
<file:line, code path, repro steps, log nguyên văn, timeline commit>

## Refs
<official docs, ticket, PR, run link>
```

## Template INVESTIGATION / PROPOSAL (kết luận trước)

```markdown
# [INVESTIGATION] <câu hỏi cần trả lời>

## Kết luận
- <trả lời thẳng câu hỏi, 2-4 gạch đầu dòng>
- <khuyến nghị nếu là đề xuất>

## So sánh phương án (nếu là đề xuất)
| Phương án | Được | Mất | Effort | Chọn? |
|---|---|---|---|---|

## Căn cứ (evidence)
- <fact> (nguồn: file:line / lệnh / doc)
- [Giả định — cách verify: …] <điều chưa chắc>

## Ảnh hưởng & phạm vi
- <màn hình/chức năng/repo liên quan từ dependency walk; ghi cả "không ảnh hưởng vì…">

## Kế hoạch thực hiện (khi issue là đối ứng vận hành / thay đổi quy trình)
| Bước | Nội dung | Thời điểm đề xuất | Downtime? | Rollback |
|---|---|---|---|---|
- Deadline (nếu vendor/khách đặt): <ngày + hậu quả nếu trễ>
- Điều kiện skip/hoãn: <ngày lễ, không có release, v.v.>
- Cần confirm trước khi thực hiện: <maintenance window, quyền truy cập…>

## Việc khách/team cần làm — việc mình lo
| Phía khách/team | Phía mình |
|---|---|

## Phát hiện ngoài phạm vi (nếu có)

---
## Chi tiết kỹ thuật (cho dev)
## Refs
```

## Template TASK (trạng thái trước)

```markdown
# [TASK] <title>

## TL;DR
| | |
|---|---|
| Trạng thái | Done / Đang làm / Blocked |
| Đã xong | <kết quả đo được, không phải "đã làm"> |
| Còn lại / blocker | <gì, chờ ai> |
| Next | <bước kế + thời điểm> |

## Kết quả & bằng chứng
| Hạng mục | Kết quả | Evidence |
|---|---|---|
| <deploy/test/số liệu> | <pass/fail/before→after> | <link, log, số> |

## Rủi ro còn mở
- <risk + biện pháp cụ thể đang có>

## Phát hiện ngoài phạm vi (nếu có)

---
## Chi tiết kỹ thuật (cho dev)
## Refs
```
