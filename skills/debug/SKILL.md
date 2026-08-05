---
name: debug
description: >-
  Technical diagnosis stage of task-toolkit — turns a reported bug into a VERIFIED immediate cause
  (the technical "why"), so the 5-Whys RCA has a real Layer 1 to build on and the report has evidence
  instead of a guess. Runs INSIDE the /task-toolkit:report pipeline (STAGE 3, BUG branch) after task-survey and
  analyze-spec, only when the immediate cause is not already proven by the survey. Method: triage by
  severity/blast-radius, instrument component boundaries to locate WHERE it breaks, compare against a
  working example, then one hypothesis at a time with a verify command each. The DEV owns the judgement
  calls — they state the hypothesis (the skill offers probing QUESTIONS, never answers, when they are
  stuck) and they declare the immediate cause; the assistant runs the mechanics and presents raw
  results. Ends at a proven immediate cause plus a fix-options table with complexity estimate that the
  dev picks from — it DIAGNOSES, it does not write the fix.
  Trigger on "điều tra bug", "chẩn đoán lỗi", "vì sao lỗi này xảy ra", "chưa rõ nguyên nhân kỹ thuật",
  or as the stage before RCA when writing a bug report. For actually implementing and testing a fix,
  that is a separate coding task (use a fix-oriented debugging skill / TDD flow), not this skill.
  Locale vn (default) / en / ja.
---

# Debug — Chẩn đoán kỹ thuật

> Ngôn ngữ giao tiếp: tiếng Việt. Artifact xuất ra theo `locale` — **`vn` mặc định**, hoặc `en`/`ja`; kế thừa `locale` của `/task-toolkit:report` khi chạy trong pipeline. Là STAGE 3 (nhánh BUG) của `/task-toolkit:report`, chạy **trước** `rca-method.md`.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Mục tiêu duy nhất: biến "hệ thống sai" thành **Immediate Cause đã chứng minh** — nguyên nhân kỹ thuật trực tiếp, có evidence, đủ chắc để làm **Layer 1** cho chuỗi 5-Why.

**Skill này KHÔNG sửa code.** Dừng ở chẩn đoán + bảng option fix. Việc sửa là task lập trình riêng, sau khi report chốt và `planning` lên kế hoạch.

## Vai trò trong skill này

| Bước | Dev (người phụ trách) | AI |
|---|---|---|
| 0 Triage | Trả lời phần chỉ mình biết (môi trường, mốc bắt đầu, thay đổi gần đây) | Gộp câu hỏi 1 lượt, kèm lý do hỏi; tự đọc thứ tự đọc được |
| 1 Định vị | Xác nhận phạm vi đo có đúng chỗ không | Dựng lệnh instrument, chạy, trình kết quả thô |
| 2 Đối chiếu | Nhìn bảng khác biệt, chỉ ra cái đáng ngờ | Tìm ca chạy đúng, liệt kê **mọi** khác biệt (không tự lọc) |
| **3 Giả thuyết** | **Nêu giả thuyết** — bí thì nhận *câu hỏi gợi mở*, không nhận đáp án | Sinh lệnh verify cho giả thuyết ĐÓ, chạy, trình kết quả thô |
| **4 Chốt cause** | **Tuyên bố Immediate Cause** | Dựng hồ sơ evidence + 3 câu để dev tự soát |
| 5 Option fix | **Chọn option**, bổ sung option AI thiếu | Dựng bảng đánh đổi + estimate; khuyến nghị phải kèm cái phải trả |

Ranh giới: AI làm **thao tác** (grep, chạy, dựng bảng, soạn nháp). Dev làm **phán đoán** (nghi cái gì, chốt cái gì, chọn cái gì). AI lấn sang cột trái = skill hỏng, kể cả khi đoán đúng.

## Cổng vào — chạy hay bỏ qua

```
type = BUG?
 └─ không → bỏ qua skill này
 └─ có → Immediate Cause đã được CHỨNG MINH ở STAGE 2 chưa?
          (task-survey đã ra evidence trực tiếp: lệch khai báo CI↔Dockerfile,
           config sai env, off-by-one đọc thấy rõ trong đúng function…)
          ├─ rồi  → BỎ QUA. Đưa thẳng nguyên nhân đó vào Layer 1 của RCA.
          └─ chưa → chạy tiếp
```

Bug hiển nhiên vẫn đi nhanh như trước. Ép chạy vòng lặp giả thuyết cho ca đã rõ chỉ tổ tốn thời gian — và hệ quả là skill bị skip.

## Tái dùng, không làm lại

| Đã có từ stage trước | Skill này làm gì với nó |
|---|---|
| `analyze-spec` §Expected vs Actual + repro + scope | **Đọc thẳng.** KHÔNG hỏi lại "lỗi thế nào", "làm sao tái hiện" |
| `task-survey` → `current-state.md`, `impact.md` | Điểm khởi hành: path/service/data liên quan đã map sẵn |
| Kỹ thuật đào code (grep, consumer-side, dependency walk, đối chiếu khai báo trùng lặp, uncertainty markers) | [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md) — **không chép lại ở đây** |

Thiếu `analyze-spec` (user gọi lẻ `/task-toolkit:debug`) → dựng Problem Statement tối thiểu ở Bước 0 rồi đi tiếp.

## Bước 0 — Triage (quyết định độ sâu)

**Issue statement 1 dòng**, dựng từ artifact đã có:

> `[Component/Service]` không `[hành vi mong đợi]` khi `[điều kiện]`, gây `[tác động đo được]`.

| Trục | Hỏi | Ảnh hưởng tới cách làm |
|---|---|---|
| **Môi trường** | prod / staging / local? | prod → ưu tiên thu evidence *trước khi* trạng thái mất (log, snapshot) |
| **Blast radius** | 1 user / nhiều user / toàn service? | rộng → đào tới cùng; hẹp → chấp nhận dừng sớm hơn |
| **Dữ liệu** | có nguy cơ mất/hỏng/lộ dữ liệu? | CÓ → xử lý như ưu tiên cao bất kể effort, không vá triệu chứng |
| **Tái hiện** | mọi lần / thỉnh thoảng / 1 lần duy nhất? | ổn định → đi Bước 1; chập chờn → xem §Ca đặc biệt trước |

**Quy ước hỏi ở skill này: gộp TOÀN BỘ câu hỏi vào 1 lượt**, mỗi câu kèm lý do hỏi ("hỏi version Node vì lỗi này là regression từ một dải version cụ thể"). Không hỏi lắt nhắt.

> Khác với `rca-method.md` — phỏng vấn 5-Why hỏi **từng câu một**, cố ý, để đào sâu bối cảnh ra quyết định. Hai ngữ cảnh khác nhau, không mâu thuẫn.

Chỉ hỏi thứ **không tự tìm được**. Tự đọc được từ repo/log/CLI thì đi mà đọc.

## Bước 1 — Định vị: hỏng ở ĐÂU trước khi hỏi vì sao

Với hệ nhiều thành phần (request → service → DB, CI → build → deploy, batch → cache → web), **đừng đoán component nào lỗi**. Đo tại **ranh giới**:

```
Với MỖI ranh giới component:
  - dữ liệu ĐI VÀO là gì?
  - dữ liệu ĐI RA là gì?
  - env/config có truyền qua được không?
Chạy MỘT lượt thu đủ → đọc kết quả → biết ranh giới nào lệch → chỉ đào tiếp component đó.
```

Một lượt đo đúng chỗ tiết kiệm hơn năm vòng đoán. Lệnh cụ thể theo loại hệ thống: [`diagnostic-commands.md`](diagnostic-commands.md).

Không can thiệp được vào runtime (prod, không quyền) → đọc từ hệ thống theo §"Trạng thái đang chạy" của file chung; vẫn không được → `[MISSING-SOURCE]` + đưa vào "Việc khách/team cần làm".

## Bước 2 — Đối chiếu với chỗ đang chạy ĐÚNG

Gần như luôn tồn tại một trường hợp tương tự **không lỗi**: env khác, record khác, endpoint tương tự, commit trước đó.

1. Tìm nó.
2. Liệt kê **mọi** khác biệt — kể cả cái "chắc không liên quan". Đúng cái đó hay là nguyên nhân.
3. Khác biệt nào giải thích được triệu chứng → thành giả thuyết ở Bước 3.

Đây cũng là chỗ áp bảng **Đối chiếu khai báo trùng lặp** ở file chung: cùng một sự thật khai hai nơi mà lệch nhau — loại bug bị sót nhiều nhất, và không bao giờ lộ ra nếu chỉ đọc tuần tự.

## Bước 3 — Vòng lặp giả thuyết (giả thuyết là của DEV)

```
1. HỎI DEV TRƯỚC:  "Sau khi xem [kết quả Bước 1 + khác biệt Bước 2],
                    bạn nghi cái gì? Vì sao nghi cái đó?"
   → Dev nêu giả thuyết. ĐÂY LÀ BƯỚC CỦA DEV.
   → Dev bí → AI đưa 2–3 CÂU HỎI gợi mở, không đưa kết luận. Ví dụ:
       "Khác biệt nào ở Bước 2 xuất hiện đúng thời điểm lỗi bắt đầu?"
       "Triệu chứng này cần điều kiện gì mới xảy ra — điều kiện đó do đâu mà có?"
       "Nếu nguyên nhân nằm ở component A, ta còn phải thấy dấu hiệu gì nữa?"
     Dev chọn hướng đào từ các câu đó.
2. AI sinh lệnh/thao tác verify chứng minh HOẶC bác bỏ giả thuyết ĐÓ   ← việc AI gõ hộ
3. Chạy. Trình KẾT QUẢ THÔ, không diễn giải sẵn thành kết luận.
4. Dev đọc và tự phán: đúng → Bước 4 · sai → ghi "đã loại X vì Z", quay lại (1)
```

**Luật:**
- Một giả thuyết một lần, một biến một lần. Đổi hai thứ rồi thấy hết lỗi = không biết cái nào chữa.
- Nguyên tắc 2 của file chung: *chứng minh, đừng khẳng định*. Đọc code rồi suy = **giả thuyết**; verify xong mới = **evidence**.
- **AI không được tự chạy vòng lặp này một mình rồi báo kết quả cuối.** Mỗi vòng dừng lại ở bước (4) để dev phán. Chạy tuốt tuồn tuột = dev mất luôn cơ hội bắt lỗi ở giả thuyết sai — mà giả thuyết sai thì mọi thứ sau đó sai theo và vẫn đọc rất hợp lý.
- **3 giả thuyết bị bác liên tiếp → DỪNG, đừng lập cái thứ 4.** Sai ở tầng giả định: có thể sai phạm vi (lỗi không nằm ở component đang nhìn), sai problem statement, hoặc kiến trúc có vấn đề sâu hơn. Đưa việc chất vấn phạm vi lại cho dev, kèm dữ kiện đã có.
- Không hiểu thì nói không hiểu. `[Giả định]` trung thực > kết luận tự tin mà sai.

> Dev chủ động nêu giả thuyết ngay từ đầu (trước cả Bước 1) → tốt, đi thẳng vào (2) verify nó. Bước 1–2 là để **có dữ kiện mà nghĩ**, không phải để AI nghĩ thay.

## Bước 4 — Chốt Immediate Cause (DEV chốt, AI dựng hồ sơ)

AI **soạn** khối dưới từ evidence đã thu và **trình dev**; dev là người **tuyên bố** đây là nguyên nhân. AI không tự chốt rồi đi tiếp.

```
IMMEDIATE CAUSE:
  [phát biểu kỹ thuật chính xác: cái gì sai, ở đâu, trong điều kiện nào]
EVIDENCE:
  [repo] path/to/file:line  ·  lệnh + output đã chứng minh  ·  log/trace
ĐÃ LOẠI:
  [giả thuyết đã bác + lý do]   ← giữ lại, tránh người sau đào lại
CÒN MỞ:
  [phần chưa verify được + cách verify]  → [Giả định — cách verify: …]
```

Đạt chuẩn khi: nêu được **cơ chế** (vì sao dẫn tới triệu chứng), không phải chỗ quan sát thấy triệu chứng; và có ít nhất một verify chứng minh nó.

Trình cho dev kèm **3 câu để họ tự soát** (không phải để AI tự trả lời):
1. Cơ chế này có thật sự giải thích **toàn bộ** triệu chứng, hay chỉ một phần?
2. Nếu nguyên nhân là cái này, còn phải quan sát được dấu hiệu gì nữa — đã thấy chưa?
3. Còn cách giải thích nào khác cũng khớp với đúng bộ evidence này không?

**Đây là input Layer 1 của `rca-method.md`.** Giao thẳng, RCA không dựng lại — nên chốt sai ở đây thì cả chuỗi 5-Why sai theo.

## Bước 5 — Option fix + estimate (không viết code)

AI dựng **các lựa chọn kèm đánh đổi**; **dev chọn**. Có option nào dev nghĩ ra mà bảng chưa có → hỏi họ trước khi chốt bảng. AI được nêu khuyến nghị, nhưng phải kèm lý do và cái đánh đổi phải trả — không nêu khuyến nghị trần.

Bảng theo đúng quy ước `INVESTIGATION` của report:

| Option | Được | Mất | Effort | Rủi ro hồi quy |
|---|---|---|---|---|

| Mức | Thời gian | Đặc điểm |
|---|---|---|
| 🟢 Trivial | < 1h | đổi config, sửa 1 dòng, sai env var |
| 🟡 Simple | 1–4h | sửa khu trú, thêm validate, sửa query |
| 🟠 Moderate | 0.5–2d | refactor 1 function/module, thêm lớp xử lý lỗi |
| 🔴 Complex | 2–5d | đổi kiến trúc, sửa xuyên service, migrate dữ liệu |
| ⚫ Critical | cần scoping riêng | thiết kế lại, sự cố bảo mật, khôi phục dữ liệu |

Ước lượng này đi thẳng vào `backlog-ticket` (§Estimation) — không ước lại từ đầu.

Kèm: **file/thành phần sẽ đụng**, **cách verify sau khi fix**, và **[Giả định]** nếu option nào chưa chắc.

## Ca đặc biệt

| Ca | Hướng đào |
|---|---|
| **Chập chờn / flaky** | race condition, tranh chấp tài nguyên, thời điểm invalidate cache, API ngoài không ổn định. Hỏi: tần suất, khung giờ, có tương quan tải không. Chưa bắt được → đề xuất **thêm log có correlation ID** rồi chờ lần tái hiện sau — đừng đoán bừa |
| **"Máy tôi chạy được"** | Luôn là khác biệt môi trường. Chụp trạng thái **cả hai** máy rồi diff: OS, version runtime, env var, file config, version dependency đã resolve (lock file, không phải khai báo) |
| **Hiệu năng** | Tách trước: chậm mọi lúc / chỉ khi tải cao / chỉ với dữ liệu nhất định. Đo trước khi đoán — EXPLAIN query, profile, đếm số lần gọi (N+1) |
| **Chỉ xảy ra trên prod** | Khác biệt dữ liệu (edge case chỉ prod có), khác biệt quy mô, khác biệt config. Không sửa mò trên prod — tái hiện bằng shape dữ liệu của prod ở môi trường thấp hơn |

## Red flags — thấy là dừng, quay lại Bước 1

| Ý nghĩ | Thực tế |
|---|---|
| "Chắc là X, sửa thử xem" | Sửa thử = đoán. Verify trước. |
| "Sửa tạm đã, điều tra sau" | Không có "sau". Vá triệu chứng làm nguyên nhân thật chìm luôn. |
| "Đổi mấy chỗ rồi chạy lại" | Hết lỗi cũng không biết nhờ cái nào. |
| "Bug đơn giản, khỏi cần quy trình" | Bug đơn giản thì quy trình chạy cũng nhanh. |
| "Thử thêm một cái nữa" (sau 2–3 lần bác) | 3 lần bác = sai tầng giả định, không phải thiếu giả thuyết. |
| "Chưa hiểu hẳn nhưng chắc thế này" | Chưa hiểu thì ghi `[Giả định]`, đừng viết như đã biết. |
| "Chỗ này chắc không liên quan" | Khác biệt bị bỏ qua là chỗ bug hay nằm nhất. |
| (AI) "Để mình chạy hết vòng lặp rồi báo kết quả" | Dev mất chỗ bắt lỗi giả thuyết. Dừng ở mỗi vòng. |
| (AI) "Dev chắc đồng ý thôi, khỏi hỏi" | Đồng ý mà không đọc = approve-all. Nợ kỹ thuật rơi vào dev, không rơi vào AI. |

## Output & bàn giao

Có workspace → ghi `tasks/{ID}/task-toolkit:debug-<yyyymmdd>.md`; không → giữ in-context.

```
1. Issue statement + triage (môi trường | blast radius | dữ liệu | tái hiện)
2. Định vị: ranh giới nào lệch (bảng vào/ra từng component)
3. Giả thuyết: bảng  # | giả thuyết | verify | kết quả (đúng/bác + lý do)
4. IMMEDIATE CAUSE + evidence + còn mở
5. Option fix + estimate
```

Đổ tiếp:
- (4) → **Layer 1** chuỗi Why của `rca-method.md`
- (2)(3) → `Chi tiết kỹ thuật` của report
- (5) → `Fix & phòng tái diễn` (report) và `backlog-ticket` (estimation)

**Kèm khối "cần soát kỹ"** (bắt buộc — để review từng dòng khả thi, không đẩy dev vào thế approve-all):

```
CẦN SOÁT KỸ:
- Giả thuyết chưa verify được: …            (vì sao chưa, cách verify)
- Kết luận dựa trên SUY LUẬN, không phải verify trực tiếp: …
- Evidence đọc gián tiếp (log/doc/lời kể) thay vì chạy thật: …
- Phần AI đề xuất mà dev CHƯA xác nhận: …
```

## Guardrails

- **[HARD]** Giả thuyết là của dev. AI không tự nêu giả thuyết rồi tự verify rồi tự kết luận. Dev bí → AI đưa **câu hỏi**, không đưa đáp án.
- **[HARD]** AI không tuyên bố Immediate Cause. AI dựng hồ sơ (cause + evidence + đã loại + còn mở) và trình; **dev chốt**.
- **[HARD]** Không sửa code trong skill này. Phát hiện fix 1 dòng hiển nhiên → vẫn ghi vào bảng option, để dev quyết.
- **[HARD]** Không chốt Immediate Cause khi chưa có ít nhất 1 verify. Chưa verify được → `[Giả định — cách verify: …]`, và RCA phải biết Layer 1 đang là giả định.
- **[HARD]** Không hỏi lại thứ `analyze-spec`/`task-survey` đã có.
- Trình kết quả lệnh ở dạng **thô** trước, diễn giải sau và tách bạch — để dev đọc được dữ kiện trước khi đọc kết luận của AI.
- Bug cũ phát hiện giữa chừng → không lờ, không âm thầm sửa: ghi repro + evidence vào `Phát hiện ngoài phạm vi`, đề xuất tách ticket.
- Prod + có nguy cơ dữ liệu → báo user **trước** khi chạy bất kỳ lệnh nào có thể đổi trạng thái. Mặc định chỉ dùng lệnh read-only.
