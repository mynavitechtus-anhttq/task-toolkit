---
name: ut-design
description: >-
  Design the unit-test viewpoints for a task before any test code is written — walk the 30-viewpoint
  matrix (A equivalence · B boundary · C branch/condition · D exception & interaction · E state &
  non-determinism · F Japanese-locale and project-specific logic), decide which apply and why, and emit
  a reviewable plan of Given–When–Then cases into 04-quality/ut-design.md. Runs a SPEC GATE first:
  `expected` must be derived from the spec, never from the current implementation. Offers to install the
  companion unittest-toolkit plugin for the full design → generate → audit flow; if declined, does the
  design here with the knowledge bundled in reference/. Trigger on "thiết kế UT", "ut design", "quan
  điểm unit test", "viết test cho hàm/module nào", "cần test những gì", or as the 04-quality stage of the
  task pipeline. Does NOT generate test code — that is ut-generate in the companion plugin.
  Locale vn (default) / en / ja.
---

# UT Design — thiết kế quan điểm Unit Test

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

> Ngôn ngữ giao tiếp: tiếng Việt. Output theo `locale` (mặc định vn). Gõ `ut-design help` → in Help cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (chọn viewpoint nào áp dụng, chốt `expected`, quyết định đánh đổi) là của **người phụ trách**; AI duyệt checklist và soạn nháp, người soát từng dòng. Xem README §Nguyên tắc gốc.

Thiết kế **quan điểm kiểm thử** cho phần logic task đụng tới, ra bảng kế hoạch review được — **trước** khi viết một dòng test code. Không sinh mã test.

## Vì sao tách thiết kế khỏi viết code

Nhảy thẳng vào code thì **cả người lẫn agent** đều có xu hướng chỉ test happy path. Tách "quan điểm" thành bước riêng buộc phải liệt kê case bất thường, biên, ngoại lệ **trước** — lúc còn rẻ, và lúc còn review được bằng mắt thường.

Chi tiết ba nguyên tắc nền: [`references/principles.md`](references/principles.md).

## Bước 0 — Chọn đường: plugin đầy đủ hay thiết kế tại chỗ

Hỏi **một câu, một lần** rồi nhớ trong phiên:

> Bạn muốn cài plugin **unittest-toolkit** để dùng full flow `design → gen → audit` không?
> `github.com/mynavitechtus-anhttq/unittest-toolkit`
> - **Có** → cài rồi gọi sang, có thêm bước sinh mã test và cổng audit tự động.
> - **Không** → thiết kế ngay tại đây bằng kiến thức có sẵn trong skill này (đủ để ra bảng quan điểm + case).

**Nếu chọn Có:** hướng dẫn cài (thêm marketplace → cài plugin), sau đó **gọi `/unittest-toolkit:design`** và dừng skill này — không làm trùng. Vẫn nhắc nó ghi kết quả vào `04-quality/ut-design.md` để khớp workspace.

**Nếu chọn Không** (hoặc user đã trả lời trước đó): chạy tiếp Bước 1 → 5 ở đây.

## Bước 1 — Cổng spec (BẮT BUỘC, chạy trước mọi thứ)

`expected` **phải suy từ spec**, không được lấy từ code đang chạy. Lấy từ code là *golden-by-implementation*: test sẽ xanh kể cả khi code sai, vì nó chỉ chép lại hành vi hiện tại.

Thứ tự tìm — **tự dò trước, đừng hỏi trống**:

1. `tasks/{ID}/01-discovery/spec-analysis.md` — mục **Requirements** + **Input Contract** là nguồn tốt nhất: mỗi `WHEN … THEN …` là một case, mỗi dòng Input Contract là biên nhóm B.
2. `tasks/{ID}/01-discovery/technical-approach.md` — ràng buộc kỹ thuật, bảo mật, môi trường.
3. Tài liệu rời trong repo (`docs/`, spec khách, API contract, business rule).
4. Không có gì → **STOP và hỏi**, kèm câu hỏi cụ thể (xem [`references/spec-intake.md`](references/spec-intake.md)).

Chi tiết 6 lối vào của cổng spec: [`references/spec-intake.md`](references/spec-intake.md).

⚠ Không có spec mà vẫn muốn đi tiếp → chỉ được viết test **mô tả hành vi hiện tại**, và phải ghi rõ nhãn `[characterization test — expected lấy từ code, chưa có spec đối chiếu]` trên từng case. Không được trình bày như test kiểm đúng.

## Bước 2 — Chọn unit để test

Từ `current-state.md` (⚠ update / 🆕 new) và `plan.md`, liệt kê phần logic task đụng tới, rồi phân 3 tầng:

| Tầng | Nhận diện | Xử lý |
|---|---|---|
| **1 · Hàm thuần có sẵn** | nhận tham số, không đụng global/DB/I/O | **Test ngay, 0 refactor** |
| **2 · Logic trộn trong controller/page script** | validate, dựng dữ liệu lẫn với I/O | **Tách hàm nhận tham số** → test hàm đó. Dữ liệu từ DB/request thành **tham số** — không cần mock |
| **3 · Không đáng unit test** | markup/echo, query thực thi, gửi mail, gọi bên thứ ba | **Không UT.** Lưới đúng: self-test luồng chính · e2e · so sánh môi trường |

Quy tắc tầng 2 — *"cái bánh kẹp"*: **đọc input (ngoài, không test) → logic thuần (giữa, test kỹ) → ghi/xuất (ngoài, không test)**. Tách sao cho phần giữa nhận vào trả ra, không đụng thế giới bên ngoài.

## Bước 3 — Duyệt 30 viewpoint

Với **mỗi unit**, đi hết checklist [`references/viewpoints-matrix.md`](references/viewpoints-matrix.md) — **A→E áp cho mọi hàm**, **F chỉ khi hàm chạm đúng loại logic tương ứng**:

| Nhóm | Nội dung | Số viewpoint |
|---|---|---|
| **A** | Phân vùng tương đương — happy path, vùng hợp lệ, vùng không hợp lệ | A1–A3 |
| **B** | Giá trị biên — min/max ±1, 0/rỗng/null, chuỗi, collection | B1–B4 |
| **C** | Độ phủ nhánh — branch, condition, vòng lặp | C1–C… |
| **D** | Ngoại lệ & tương tác — loại exception, cleanup, lỗi dependency, kiểm tương tác, idempotency | D1–D5 |
| **E** | Trạng thái & bất định — state machine, thời gian/random/thứ tự, bug lịch sử, đồng thời | E1–E4 |
| **F** | Đặc thù domain (locale Nhật) — trim full/half-width, kana, sort, era/ngày, tiền yên, độ dài chuỗi, rule dự án, mã bưu chính, bắt buộc có điều kiện, trigger nghiệp vụ | F1–F10 |

**Mỗi viewpoint phải có kết luận rõ ràng:** *áp dụng* (→ ≥1 case) hoặc *không áp dụng* (→ **ghi lý do**). Bỏ trống không phải là câu trả lời — nó là chỗ để lọt case, và là thứ reviewer không cách nào phát hiện.

## Bước 4 — Bảng kế hoạch + case Given–When–Then

````markdown
# UT Design — {task}

> Spec nguồn: {file · mục} · Ngày: {yyyy-mm-dd} · Người thiết kế: {tên}

## Unit trong phạm vi
| Unit | File | Tầng | Vì sao test / không test |
|---|---|---|---|

## Kế hoạch viewpoint — {tên unit}
| VP | Áp dụng | Case | Lý do nếu không áp dụng |
|---|---|---|---|
| A1 | ✅ | UT-01 | |
| A2 | ✅ | UT-02, UT-03 | |
| B2 | ✅ | UT-05 | |
| E4 | ❌ | — | hàm đồng bộ, không có shared state |
| F4 | ❌ | — | không xử lý ngày |

## Case
### UT-01 — {tên case}  `viewpoint:A1`
- **Given** {trạng thái/đầu vào}
- **When** {gọi gì}
- **Then** {kết quả mong đợi — **suy từ spec**, ghi nguồn}
- **Nguồn expected:** `[spec | mục 3.2]`

## Không phủ ở đây
| Vùng | Vì sao | Lưới nào bắt |
|---|---|---|
````

## Bước 5 — Tự soát trước khi ghi file

1. **Mọi viewpoint A→E có kết luận** — không ô nào trống.
2. **Mọi `Then` có nguồn** — dòng nào không cite được spec thì đánh dấu `[chưa có nguồn]`, đừng để trôi.
3. **Không có case tautology** — `expect(x).toBe(x)`, hoặc assert lại đúng giá trị mock vừa trả về.
4. **Case đủ loại, không đủ nhiều** — mỗi vùng 1 đại diện là đủ; 10 case cùng một vùng là lãng phí, không phải kỹ.

Ghi `tasks/{ID}/04-quality/ut-design.md`. Chưa có workspace → in chat + đề nghị `task-init`.

## Handoff

- **→ viết test**: bảng này là đầu vào để code test, mỗi test gắn `viewpoint:<ID>` để truy vết ngược. Có cài unittest-toolkit → `/unittest-toolkit:gen`.
- **→ `04-quality/test-checklist.md`**: case nào **không** phủ bằng UT (mục "Không phủ ở đây") phải xuất hiện ở checklist kiểm tay hoặc test case e2e — không được rơi vào khoảng trống giữa hai lưới.
- **→ ticket**: `Implementation content` của ticket liên quan thêm checkbox *"viết UT theo `04-quality/ut-design.md`"*.

## Anti-patterns

- Lấy `expected` bằng cách chạy code rồi dán output — **cấm tuyệt đối**, xem `references/principles.md`.
- Sinh mã test trong skill này — đây là bước thiết kế, code là bước sau.
- Duyệt viewpoint kiểu tick hàng loạt cho xong — mỗi ô phải có case hoặc lý do.
- Dừng vì "coverage đã đẹp" — điều kiện dừng là **phủ hết viewpoint áp dụng**, không phải phần trăm.
- Ép UT vào code tầng 3 (markup, I/O thực thi) — tốn công, test giòn, không bắt được gì.

## Help

```
ut-design <TICKET-ID|tên hàm/module> [locale=vn|en|ja]
  Thiết kế quan điểm UT → bảng viewpoint (A1…F10) + case Given-When-Then, ghi 04-quality/ut-design.md.
  - Hỏi 1 lần: cài plugin unittest-toolkit (full flow design→gen→audit) hay thiết kế tại chỗ?
  - Cổng spec chạy trước: expected PHẢI suy từ spec, không lấy từ code đang chạy.
  - Ăn từ 01-discovery/spec-analysis.md (Requirements + Input Contract) — không phân tích lại.
  KHÔNG sinh mã test (đó là ut-generate của unittest-toolkit).
```
