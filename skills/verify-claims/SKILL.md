---
name: verify-claims
description: >-
  Kiểm từng khẳng định trong một tài liệu có ĐÚNG SỰ THẬT không — bóc mọi claim
  kiểm được (số lượng, tên bảng/route/hàm, phiên bản, licence, "chỉ dùng ở X",
  đường dẫn, lệnh, giá trị config), nêu cách kiểm, kiểm thật bằng
  code-evidence-method, ra bảng Claim | Cách kiểm | Thực tế | Verdict. Dùng cho
  report trước khi gửi khách, và cho tài liệu mô tả hiện trạng hệ thống
  (architecture, inventory, investigation). KHÔNG review cấu trúc, văn phong,
  IA, hay mâu thuẫn nội tại — spec/plan dùng ce-doc-review. Trigger "kiểm số
  liệu", "verify claim", "doc này có đúng không", "soát lại trước khi gửi".
---

# Verify Claims — tài liệu này có đúng sự thật không

> **Ai nghĩ, ai gõ** — AI bóc claim, nêu cách kiểm, chạy lệnh kiểm, ghi kết quả. Việc *một claim sai có nghiêm trọng không* và *sửa thế nào* là của người phụ trách. Skill này đưa bằng chứng, không đưa phán quyết.

## Nó kiểm cái gì — và không kiểm cái gì

Ba loại review khác nhau, đừng lẫn:

| Câu hỏi | Ai lo |
|---|---|
| Tài liệu này **có mâu thuẫn / khả thi / đủ** không? | `ce-doc-review` |
| Tài liệu này **có đúng sự thật** không? | ← **skill này** |
| Report này **có gửi khách được** không (lập luận, thiên kiến, độ đọc-được) | `report-reviewer` |

**Không** làm ở đây: cấu trúc, văn phong, kiến trúc thông tin, funnel, Diataxis, đoạn văn dài ngắn, mâu thuẫn nội tại. Tài liệu mạch lạc hoàn hảo mà sai sự thật vẫn trượt ở đây; tài liệu viết lủng củng mà mọi con số đều đúng vẫn đạt.

Dùng cho hai loại tài liệu:

- **Report** trước khi gửi khách — chạy cùng `report-reviewer`, hai việc khác nhau
- **Tài liệu mô tả hiện trạng** — architecture discovery, site inventory, integration catalog, investigation. Loại này sai theo kiểu nguy hiểm nhất: đọc rất trôi, không có dấu hiệu gì để nghi

---

## Bước 1 — Bóc claim

Đọc hết tài liệu, rút ra **mọi phát biểu kiểm được**. Tám loại:

| # | Loại | Ví dụ |
|---|---|---|
| 1 | **Số lượng** | "14 blog con" · "3 màn hình bị ảnh hưởng" · "893 template" |
| 2 | **Định danh** | tên bảng · cột · route · hàm · class · file · biến env |
| 3 | **Phiên bản / mốc thời gian** | "MT 8.0.6" · "EOL 2025-11-21" · "Node ≥ 20.19" |
| 4 | **Quan hệ** | "chỉ dùng ở X" · "không còn dùng" · "gọi từ Y" · "dùng chung với Z" |
| 5 | **Đường dẫn / link** | tham chiếu nội bộ doc · file thật trong repo |
| 6 | **Lệnh** | lệnh setup/test/deploy trong doc có chạy được không |
| 7 | **Bên thứ ba** | licence · quyền sở hữu · còn hỗ trợ không · giá |
| 8 | **Giá trị cấu hình** | timeout · cron · TTL · giới hạn |

**Không phải claim** — loại ngay ở bước này, không đưa vào bảng:

- Ý kiến, đánh giá: *"cách này gọn hơn"*, *"rủi ro cao"*
- Đề xuất, dự định: *"nên tách ra"*, *"đợt sau sẽ làm"*
- Dự đoán: *"sẽ mất khoảng 3 ngày"*
- Câu điều kiện chưa xảy ra: *"nếu bỏ cache thì sẽ chậm"*

Nhầm ý kiến thành claim rồi đi "kiểm" nó là cách nhanh nhất biến bảng này thành rác.

⚠ **Claim nguy hiểm nhất là claim phủ định** — *"không còn dùng"*, *"không ảnh hưởng gì"*, *"chỉ có một chỗ"*. Chúng khó kiểm hơn hẳn claim khẳng định (phải quét hết mới kết luận được), và sai thì hậu quả lớn hơn. Đánh dấu riêng, đừng để lẫn.

## Bước 2 — Nêu cách kiểm **trước khi** kiểm

Với mỗi claim, viết ra **sẽ kiểm bằng gì** trước khi chạy lệnh nào. Ép bước này để tránh chuyện tìm được cái gì thì nhận cái đó làm bằng chứng.

Thang nguồn, mạnh xuống yếu:

| Tầng | Nguồn | Ví dụ |
|---|---|---|
| **0** | **Nguồn khai báo** — mạnh nhất | schema DB · migration · `phpunit.xml` · `composer.json` · OpenAPI · file config |
| **1** | Reference trong code | CodeGraph nếu có, grep nếu không — xem [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md) |
| **2** | Coupling không qua code | tên bảng · cache key · path dạng chuỗi — **luôn grep**, CodeGraph mù chỗ này |
| **3** | Khai báo chéo layer | CI ↔ Dockerfile ↔ ECS task def — thủ công |
| **4** | Ngoài repo | DB thật · log · **web** (bắt buộc cho claim loại 7) |

Hai luật:

- **Nguồn khai báo thắng code đang chạy.** `phpunit.xml` khai bốn testsuite là sự thật về testsuite; đọc code test đoán ra là suy diễn.
- **Không dùng chính tài liệu làm bằng chứng cho tài liệu.** Claim ở trang 3 khớp với câu ở trang 8 không chứng minh gì — cả hai có thể cùng sai. Bằng chứng phải nằm **ngoài** tài liệu đang kiểm.

## Bước 3 — Kiểm, ghi verdict

Bốn verdict, không có mức thứ năm:

| Verdict | Nghĩa | Bắt buộc kèm |
|---|---|---|
| ✅ `verified` | kiểm được, đúng | nguồn + lệnh đã chạy |
| ❌ `contradicted` | kiểm được, **sai** | **thực tế là gì** — không chỉ nói "sai" |
| ⚠ `unverifiable` | không kiểm được trong tầm với | **cần gì mới kiểm được** |
| ⬜ `out-of-scope` | không thuộc loại kiểm được | (đã loại ở bước 1, hiếm khi xuất hiện) |

`unverifiable` **không phải** một loại finding nhẹ. Nó là **lỗ hổng kiểm chứng có tên** — đi vào mục Validation notes ở output, không đi vào danh sách vi phạm. Nhập nhèm hai thứ này là cách tài liệu tự khen mình đã được kiểm trong khi chưa.

### Thang confidence — neo vào *việc đã làm*, không vào cảm giác

Mượn từ `ce-doc-review`, đổi trục cho hợp việc ở đây: neo vào **cách kiểm**, không vào độ mạnh lập luận. Năm mức, không có mức giữa:

| | Nghĩa | Đi đâu |
|---|---|---|
| `0` | không đứng vững trước soi xét nhẹ | **bỏ im lặng**, không ghi |
| `25` | ngờ ngợ, chưa kiểm được | **bỏ im lặng** — hoặc kiểm tiếp cho lên `75`, hoặc chuyển thành `unverifiable` |
| `50` | có lệch nhưng **chưa dứt điểm** | → **Validation notes**, không phải vi phạm |
| `75` | kiểm bằng nguồn tầng 1–2, nhất quán nhiều chỗ | → danh sách vi phạm |
| `100` | kiểm bằng **nguồn khai báo (tầng 0)** hoặc quan sát trực tiếp — không còn chỗ diễn giải | → danh sách vi phạm |

Đây là chỗ **khác `ce-doc-review` có chủ ý**: bên đó `50` là FYI. Ở đây `50` nghĩa là *"tôi chưa kiểm xong"* — và một claim chưa kiểm xong không được trình bày như một lỗi đã tìm ra. Nó là công việc còn dở, ghi vào Validation notes.

**`100` đòi nguồn khai báo.** "Tôi grep thấy 12 chỗ" là `75`, không phải `100` — grep có thể sót cách gọi động. `phpunit.xml` khai bốn testsuite là `100`.

### Không phải finding — bỏ hẳn, đừng hạ mức

Bốn dạng dưới đây **không** vào bảng ở bất kỳ mức nào:

- Nitpick văn phong, thuật ngữ, cách đặt tên — không thuộc phạm vi skill này
- Lo lắng suy đoán về tương lai: *"sau này có thể đổi"*
- Lo lắng lý thuyết không có số liệu nền: *"chỗ này chắc chậm"*
- Ghi nhận **không cần hành động**: *"đã kiểm, đúng rồi"* → đó là dòng `verified` trong bảng, không phải một finding

**Finding theo định nghĩa là thứ phải làm gì đó.** "Không cần làm gì" không phải finding.

## Bước 4 — Ba việc kiểm bổ sung

Ba thứ không phải claim đơn lẻ nhưng thuộc cùng câu hỏi "tài liệu này có đúng không". Lấy từ playbook của `technical-documentation`.

### 4.1 · Path-map drift — ba nhãn rõ ràng

Đường dẫn giải quyết **tương đối với file khai nó**, không phải với thư mục hiện tại. Ba dạng lệch, gọi tên riêng:

| Nhãn | Nghĩa |
|---|---|
| `missing file` | đường dẫn trỏ tới thứ không tồn tại |
| `stale route` | file có nhưng đã đổi tên/chuyển chỗ |
| `wrong base path` | đúng file, sai gốc — hay gặp khi doc bị move |

Kiểm **cả hai bản đồ** khi có: đường dẫn filesystem và URL công bố. Hai cái đó là hai map khác nhau, khớp cái này không suy ra khớp cái kia.

### 4.2 · Command drift

Mọi lệnh trong tài liệu: file config nó nhắc có tồn tại không, tham số nó truyền có được khai không, đường dẫn nó trỏ có thật không.

Đây là loại lỗi rẻ nhất để tìm và đắt nhất khi bỏ sót — người mới làm theo sẽ dừng ngay ở đó và mất niềm tin vào cả tài liệu.

### 4.3 · Parity đa ngôn ngữ

Tài liệu có nhiều bản ngôn ngữ (report VN/EN/JA của chính toolkit này) → đối chiếu các phần **task-critical**: bước làm, cảnh báo, điều kiện tiên quyết, giới hạn, số liệu.

Sửa bản VN mà quên bản JA là lỗi thật và **không ai khác kiểm**. Lệch có chủ ý thì được, nhưng phải nêu lý do; lệch không giải thích được là finding.

## Bước 5 — Output

Ba phần, thứ tự cố định:

```markdown
## Verify Claims — <tên tài liệu>

**Đã bóc:** 34 claim kiểm được · **✅ 26 verified · ❌ 5 contradicted · ⚠ 3 unverifiable**

### 1 · Vi phạm (blocking)

| # | Claim | Vị trí | Cách kiểm | Thực tế | Conf |
|---|---|---|---|---|---|
| 1 | "site 介護のみらいラボ có 14 blog con" | `architecture-discovery.md:88` | đếm `blog_class='blog'` có parent_id = N trong `cms-ddl.sql` | **12** | 100 |
| 2 | "`php artisan test --testsuite=Job`" | `README.md:441` · `README.ja.md:441` | `phpunit.xml` khai testsuite nào | chỉ có `Unit` `Feature` `Unit-Tests` `Feature-Tests` — **không có testsuite theo module** | 100 |

### 2 · Không chặn (non-blocking)

| # | Claim | Vị trí | Ghi chú |
|---|---|---|---|

### 3 · Validation notes

**Đã kiểm:** claim loại 1,2,5,6 — phủ hết
**Chưa kiểm được:**
- "MTAppjQuery là sản phẩm thương mại" (`upgrade-impact.md:23`) — ⚠ `unverifiable` bằng repo. Cần tra trang phát hành/GitHub của thư viện. **Đây là claim về bên thứ ba, kiểm bằng code không bao giờ ra.**
- Giá trị `JOB_SEARCH_CACHE_TTL` ở production — không đọc config env prod theo thoả thuận. Claim liên quan để `unverifiable`, không suy từ staging.

**Rủi ro còn lại:** claim loại 4 ("chỉ dùng ở X") kiểm bằng grep nên tối đa đạt `75` — cách gọi động không bắt được.
```

**Không tìm thấy vi phạm nào thì nói thẳng ra**, kèm phần Validation notes đầy đủ. Một bản "không có vấn đề" mà không nói đã kiểm những gì và chưa kiểm được gì thì vô giá trị — người đọc không phân biệt được *đã soát kỹ* với *chưa soát*.

## Chế độ

**Mặc định `report-only`** — chỉ báo, không sửa tài liệu. Muốn sửa thì nói rõ; kể cả khi đó, chỉ tự sửa những claim ở mức `100` mà cách sửa là duy nhất (con số sai → con số đúng, tên file sai → tên file đúng). Claim `contradicted` mà sửa lại làm đổi kết luận của tài liệu → **hỏi**, không tự sửa.

## Handoff

- **→ `report-reviewer`**: chạy song song, không thay nhau. `verify-claims` kiểm *số liệu*, `report-reviewer` kiểm *lập luận*. Report đạt cả hai mới gửi khách.
- **→ `analyze-spec`**: claim `contradicted` giữa tài liệu và code chính là conflict **doc ⟷ code** — đưa vào section 6 với cả hai phía, không tự phân xử.
- **→ khách**: claim `unverifiable` loại 7 (bên thứ ba) và loại liên quan môi trường prod thường phải hỏi khách, không tự tra được.

## Guardrails

- Không review cấu trúc / văn phong / IA / mâu thuẫn nội tại — không thuộc phạm vi.
- Không dùng chính tài liệu làm bằng chứng cho tài liệu.
- `unverifiable` → nêu **cần gì mới kiểm được**, không đoán, không để trống.
- `contradicted` → phải ghi **thực tế là gì**, không chỉ "sai".
- `100` chỉ dành cho nguồn khai báo hoặc quan sát trực tiếp. Grep tối đa `75`.
- Không sửa tài liệu ở chế độ mặc định.
- Không đọc config môi trường production trừ khi được yêu cầu rõ.
- Claim phủ định ("không còn dùng") — quét hết mới kết luận; không kết luận từ một lần grep không ra kết quả.

## Ví dụ output đầy đủ

Xem [`example-output.md`](example-output.md).

## Những câu tự bào chữa hay gặp

| Câu bào chữa | Sự thật |
|---|---|
| *"Số này chắc đúng, ai viết cũng phải kiểm rồi"* | Con số sai trong tài liệu gần như luôn do người viết tin vào một lần đếm cũ. Không ai kiểm lại vì nó *trông* đúng |
| *"Grep không ra kết quả nào → không còn dùng"* | Grep không ra chỉ nghĩa là **cách grep đó** không ra. Gọi động, chuỗi ghép, tên qua config — đều lọt |
| *"Chỗ này tài liệu nói vậy hai lần rồi, chắc đúng"* | Hai lần sai vẫn là sai. Bằng chứng phải nằm ngoài tài liệu |
| *"Claim này không kiểm được, thôi bỏ qua"* | Bỏ qua im lặng làm người đọc tưởng đã kiểm. Ghi `unverifiable` + cần gì để kiểm |
| *"Đã kiểm hết rồi, không có gì"* | Vậy thì phần Validation notes đâu? Không liệt kê đã kiểm gì thì "không có gì" không ai tin được |
