# RCA Method — 5 Whys

Phương pháp phân tích nguyên nhân gốc dùng cho STAGE 3 của `/task-toolkit:report` khi type = BUG.

## Triết lý nền (bất biến)

- **System > People**: tìm **lỗ hổng quy trình (Process Gap)**, không tìm người để đổ lỗi. Sai lầm con người là *kết quả* của hệ thống kém.
- **Prevent Recurrence**: đích đến là sự cố không lặp lại. Issue lặp lại = phân tích 5 Why trước đó sai hoặc giải pháp chưa thực thi.
- **No-Blame**: mở đầu phân tích phải nói rõ — "để hiểu chuyện gì đã xảy ra nhằm cải thiện hệ thống, không truy trách nhiệm cá nhân".
- Hình ảnh tảng băng: incident là phần nổi; **System Structure** là phần chìm — nơi cần tác động.

## Kỹ thuật đặt câu hỏi (khi cần hỏi user/stakeholder)

- **Hỏi TỪNG câu một**; câu trả lời mơ hồ/mới ở mức triệu chứng → góp ý cụ thể và hỏi lại, chỉ đi tiếp khi đạt.
- **5W1H**: What · When · Where · Who · How · **Decision Context**.
- **Hỏi theo bối cảnh ra quyết định** (không truy vấn tội): ❌ "Tại sao bạn không test?" → ✅ "Thông tin nào khiến bạn kết luận việc test là không cần thiết lúc đó?"
- **Tránh Yes/No**: ❌ "Bạn có hiểu requirement không?" → ✅ "Bạn đã diễn giải yêu cầu đó thế nào? Phần nào chưa rõ?"
- Ghi trung thực, không bịa; đối chiếu đa nguồn (dev, QA, lead) để loại thiên kiến.

## Bước 1 — Problem Statement (WHAT + WHEN + Impact, đo được)

> **Tái dùng, không dựng lại:** nếu đã chạy `analyze-spec` (bug), section 4 của `spec-analysis.md` (Expected vs Actual + repro + scope) **chính là** Problem Statement — đọc thẳng, chỉ bổ sung số đo (WHEN, Impact định lượng) nếu thiếu. Chưa có analyze-spec → dựng theo bảng dưới.

| Tránh (vague) | Nên dùng (measurable) |
|---|---|
| Sprint làm chậm | Sprint 10 trễ 5 ngày so với kế hoạch |
| Code chất lượng kém | Bug thanh toán lọt Production gây mất 100 giao dịch |
| Trang lỗi | Trang thanh toán lỗi 19:05–19:40, ~300 giao dịch thất bại |

## Bước 2 — Facts & Timeline

Sắp xếp sự kiện theo thời gian (vd: Req Review → Code → Review → Deploy → Verification) — khoảng trống và hiểu lầm **tự lộ diện** khi timeline dựng xong. Với mỗi bước hỏi: *"Làm dựa trên giả định nào? Nguồn tin từ đâu?"* — nhiều sự cố nằm ở **Assumption Gap**.

| Thời điểm | Sự kiện | Giả định / Nguồn tin |
|---|---|---|

## Bước 3 — Chuỗi Why qua 3 tầng

> **Layer 1 là INPUT, không phải thứ dựng ở đây.** Immediate Cause phải là nguyên nhân kỹ thuật **đã có evidence**, đến từ một trong hai chỗ: (a) skill `debug` vừa chạy ở STAGE 3 bước 1 — lấy nguyên văn mục `IMMEDIATE CAUSE` + evidence của nó; (b) `task-survey` đã chứng minh trực tiếp (vd lệch khai báo CI↔Dockerfile). **Chưa có evidence thì DỪNG, chạy `debug` trước** — đừng suy đoán Layer 1 rồi đào tiếp: cả chuỗi Why sẽ sai theo mà vẫn đọc rất hợp lý, đây là failure mode khó phát hiện nhất của 5-Why.
>
> Layer 1 buộc phải để `[Giả định]` (không verify được trong môi trường hiện tại) → ghi rõ ngay trong bảng chuỗi Why, và root cause chốt ở Bước 4 cũng mang theo dấu đó.

```
1. Immediate Cause — "Tại sao sự cố xảy ra ngay lúc đó?"        (Layer 1: code/config trực tiếp)
2. Process Cause  — "Tại sao quy trình cho phép lỗi đó xảy ra?"  (Layer 2: quy trình lỏng)
3. System Gap     — "Tại sao tổ chức thiếu năng lực/công cụ      (Layer 3: ★ ROOT CAUSE)
                     để ngăn chặn?"
```

**3 luật bắt buộc:**
1. **Không dừng ở con người.** Kết luận dạng "sơ suất / thiếu cẩn thận / thiếu kinh nghiệm" = **chưa đủ sâu**, hỏi tiếp WHY.
2. **Kiểm tra lỗi hệ thống hay lỗi cá nhân**: hỏi "Nếu người khác làm việc đó, lỗi có xảy ra không?" — nếu **CÓ** ⇒ lỗi nằm ở hệ thống, đào tiếp.
3. **Branching — One Problem = One Why Chain**: một câu Why có 2 câu trả lời hợp lý → **tách 2 nhánh**, mỗi nhánh đào tới root cause riêng.
   - Vd "Sprint 10 trễ 7 ngày": nhánh tài nguyên (key dev nghỉ đột xuất → *thiếu contingency plan*) ∥ nhánh yêu cầu (khách clarify muộn → *thiếu change management governance*).

**Case study chuẩn** (bug lọt Production):
```
Bug nghiêm trọng lọt Production
 → QA không phát hiện          → thiếu test case cho trường hợp này
 → requirement thiếu mô tả     → không có checklist rà soát requirement
 → ROOT CAUSE: quy trình thiếu bước Review Checklist cho Requirement
```
(Không dừng ở lỗi QA/Dev — đi đến **thiếu công cụ kiểm soát**.)

**Ví dụ dẫn dắt** (rút từ phiên mẫu): user chốt "root cause là dev quên đóng connection" → hỏi lại "dev khác viết thì có xảy ra không?" → "có, vì không ai kiểm cái đó" → đào tiếp → ROOT CAUSE: quy trình release thiếu **kiểm thử tải** + thiếu **checklist rà soát giải phóng tài nguyên**.

## Bước 4 — Chốt Root Cause rồi DỪNG

- Root cause phải ở **tầng hệ thống** (process/tool/policy gap), được user xác nhận.
- Phân tích **dừng ở Root Cause** — Action Plan là bước sau, tách bạch (trong report: mục `Fix & phòng tái diễn` viết SAU khi root cause đã chốt).

## Tiêu chí cho "Fix & phòng tái diễn" (khi viết vào report)

- **Systemic Change**: đổi Process / Tool / Policy — không phải lời hứa.
- **Preventive**: ngăn tái diễn, không chỉ giảm xác suất. Có **Owner + Due Date**.
- **Kiểm tra biện pháp**: hỏi "biện pháp này có phụ thuộc con người tự nhớ / tự cẩn thận không?" → nếu CÓ = **chưa đạt** ("nhắc nhở team", "sẽ cẩn thận hơn" là weak action). Hành động tốt hoạt động **ngay cả khi người ta quên**.

## Sai lầm phổ biến (red flags khi tự soát)

- Dừng quá sớm ở Human Error.
- Nhảy cóc sang solution khi chưa hiểu nguyên nhân.
- Weak actions (lời hứa thay vì thay đổi hệ thống).
- Kết luận bằng tên một cá nhân.
- Anchoring: cả chuỗi chỉ lặp lại giả thuyết đầu tiên → **tự sinh 2–3 giả thuyết cạnh tranh**, kiểm xem facts có loại được chúng không; không loại được → ghi thành nhánh chưa xét.
- Mắt xích nhân-quả "nhảy cóc": với mỗi Why hỏi lại *"điều này có THẬT SỰ gây ra điều phía trên, hay chỉ là một khả năng?"*

## Biểu mẫu output (đổ vào report)

```
1. Problem Statement   (What + When + Impact đo được)
2. Facts & Timeline    (bảng thời điểm|sự kiện|giả định/nguồn)
3. The 5 Whys Chain    (bảng: # | Tầng | Nguyên nhân | Evidence — mắt xích chưa verify ghi [Giả định])
   + Dòng kiểm tra: "Nếu người khác làm, lỗi có xảy ra không? → CÓ ⇒ lỗi hệ thống"
4. Root Cause (System Level) — user đã xác nhận
```

Map sang template BUG của report: (1)+(2) → `TL;DR` + `Chi tiết kỹ thuật`; (3) → `Chuỗi nguyên nhân` (dạng bảng); (4) → `Nguyên nhân gốc` (gạch đầu dòng); tiêu chí action → `Fix & phòng tái diễn`.

## Áp dụng & thẩm định

- **Bắt buộc** với incident C1/C2; nên dùng cho khiếu nại khách và C3 lặp lại.
- Sau khi chốt root cause → **tự soát theo mục Red flags trên**; khi `audience=customer` bắt buộc qua agent `report-reviewer` (thẩm định độc lập, chống anchoring).
- Tiêu chí duyệt (governance): logic chặt, root cause đúng tầng hệ thống, action khả thi. Chất lượng hơn số lượng.
