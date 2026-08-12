# Phân tích impact — làm sao đủ và đúng, để không degrade

> Dùng bởi `task-survey` (sinh `01-discovery/impact.md`), và tiêu thụ bởi `backlog-ticket` (Risk/Impact + regression),
> `ut-design`, `security-check`, `perf-check`, `test-checklist`.
> Kỹ thuật đào code nền: [`code-evidence-method.md`](code-evidence-method.md).

## Vì sao walk "ai gọi hàm này" là chưa đủ

Tìm call-site trả lời được câu **"code tôi sửa được dùng ở đâu"**. Nhưng regression đắt nhất không đến từ nơi gọi — nó đến từ nơi **dựa vào một chi tiết của hành vi cũ** mà không ai ghi ra:

- thứ tự phần tử trong danh sách trả về
- định dạng chuỗi (dấu phân cách, số chữ số, thứ tự tham số trong URL)
- giá trị khi không có dữ liệu (`null` vs chuỗi rỗng vs `0`)
- tác dụng phụ (có ghi log không, có bắn event không, có xoá cache không)
- thời điểm (chạy trước hay sau một việc khác)

Những chỗ đó **vẫn biên dịch được, vẫn không có lỗi nào**, và chỉ lộ ra khi người dùng thấy sai. Đây là lý do impact phải đi **hai chiều**: xuôi (ai gọi) và **ngược (ai dựa vào)**.

## Bước 1 — Phân loại thay đổi, vì mỗi loại lan toả một kiểu

| Loại thay đổi | Lan theo hướng | Phải đi tìm gì |
|---|---|---|
| **Thêm mới, không đụng cũ** | gần như không lan | chỉ kiểm nơi mới xuất hiện |
| **Đổi hành vi hàm/service dùng chung** | mọi caller, kể cả gián tiếp | call-site + **nơi dựa vào chi tiết hành vi** |
| **Đổi cấu trúc dữ liệu / schema** | mọi nơi đọc **và** ghi, kể cả batch, repo anh em, báo cáo | grep tên bảng/cột — công cụ reference **không thấy** |
| **Đổi định dạng trao đổi** (API response, file, message queue) | consumer ngoài tầm repo | đọc **phía consumer**, không suy từ producer |
| **Đổi UI dùng chung** (component, layout, CSS/JS bundle) | mọi màn hình render/nạp nó | đọc build config, không chỉ import |
| **Đổi cấu hình / biến môi trường** | mọi môi trường, và **chỉ lệch ở một môi trường** | so bảng cấu hình 4 môi trường |
| **Đổi hạ tầng** (image, workflow, hạ tầng chung) | mọi service dùng chung artifact/hạ tầng | đối chiếu khai báo trùng lặp |
| **Xoá / đổi tên** | mọi tham chiếu, kể cả chuỗi động ghép tên | grep cả **mảnh tên**, vì tên ghép runtime thì công cụ mù |

Ghi loại thay đổi **trước**, rồi mới đi tìm — đi tìm mà không biết mình tìm kiểu gì thì sẽ tìm theo thói quen (chỉ call-site).

## Bước 2 — Chiều xuôi: bề mặt bị chạm (3 tầng)

Giữ nguyên walk 3 tầng của [`code-evidence-method.md`](code-evidence-method.md):

1. **Reference trong code** — công cụ tìm được
2. **Coupling qua tên** — bảng, cache key, đường dẫn, tên file, tên biến môi trường. **Luôn grep**, công cụ mù ở tầng này
3. **Khai báo chéo layer** — cùng một giá trị khai ở hai nơi (service ↔ host, branch trigger ↔ map env, version pin CI ↔ Dockerfile). Lệch = bug âm thầm

## Bước 3 — Chiều ngược: ai đang dựa vào hành vi CŨ ⭐

Với mỗi thứ sắp đổi, hỏi **"nếu tôi đổi cái này thì ai đang ngầm trông chờ nó giữ nguyên?"**

| Dựa vào | Cách phát hiện |
|---|---|
| **Thứ tự** kết quả / tham số | tìm nơi lấy phần tử theo chỉ số, nơi so chuỗi đã ghép, snapshot test, URL sinh sẵn |
| **Định dạng** chuỗi/số/ngày | tìm nơi parse ngược lại, regex, so sánh chuỗi, hiển thị thẳng ra UI |
| **Giá trị khi rỗng** | tìm `if (!x)`, `?? ''`, `isset()` phía consumer — đổi `null` thành `''` là đổi nhánh của họ |
| **Tác dụng phụ** | tìm nơi trông chờ cache bị xoá / event được bắn / log được ghi sau khi gọi |
| **Thời điểm** | cron/batch nào chạy trước–sau; ai đọc dữ liệu ngay sau khi mình ghi |
| **Hiệu năng ngầm** | nơi gọi trong vòng lặp — đổi hàm nhanh thành hàm gọi DB là biến 1 query thành N |

**Ba nguồn tìm nhanh nhất:** test cũ đang assert hành vi đó · code phía consumer (đọc thẳng, đừng suy từ producer) · nơi hard-code giá trị/định dạng.

> Ví dụ thật: thứ tự tham số `fd_` / `wk_` trên URL tìm kiếm đổi giữa hai bản. Không hàm nào gọi sai, không lỗi nào ghi lại — nhưng phía đối tác so chuỗi URL nên kết quả lệch. Đây là "dựa vào thứ tự", tầng 3 chứ không phải tầng 1.

## Bước 4 — Ràng buộc ngầm: không có tham chiếu nào trong code

Nhóm này **không tìm được bằng công cụ**, phải hỏi thẳng:

| Loại | Câu hỏi | Cách kiểm |
|---|---|---|
| **Dữ liệu dùng chung** | còn ai đọc/ghi cùng bảng, cùng cache key, cùng thư mục file? | grep tên; hỏi repo anh em |
| **Thứ tự thời gian** | có batch/cron nào chạy trước–sau và trông chờ trạng thái? | đọc lịch cron, đọc queue |
| **Giả định về dữ liệu** | nơi khác có giả định "trường này luôn có giá trị" không? | đọc consumer, đọc validate của họ |
| **Đường vào khác** | màn hình này còn vào được từ đâu nữa — deep link, email, QR, bookmark cũ? | grep route, đọc mail template |
| **Người dùng khác vai trò** | vai trò khác nhìn màn này có khác không? | đọc phân quyền |
| **Môi trường** | hành vi có khác giữa dev/stg/prod không (flag, plugin, cấu hình)? | so bảng cấu hình các môi trường |

> Cột cuối là chỗ hay lọt nhất: thứ **bật ở prod mà tắt ở dev** thì test ở dev không bao giờ thấy.

## Bước 5 — Chấm bán kính ảnh hưởng → quyết độ sâu kiểm

| Mức | Nghĩa | Bắt buộc kiểm tới đâu |
|---|---|---|
| **R1** | 1 màn hình, không dùng chung | tự đi hết luồng đó một lần |
| **R2** | 1 module / vài màn cùng nhóm | + regression các màn trong nhóm |
| **R3** | thành phần dùng chung toàn site | + **so sánh trước/sau trên môi trường giống prod** |
| **R4** | nhiều repo · schema · batch · hạ tầng | + kiểm **phía consumer** · + có đường lùi · + thông báo bên liên quan |

Bán kính do **chiều ngược và ràng buộc ngầm** quyết định, không phải số dòng code. Sửa 1 dòng trong hàm dùng chung vẫn là R3.

## Bước 6 — Mỗi impact phải sinh ra một việc kiểm ⭐

Đây là chỗ impact **thật sự chống degrade**. Danh sách "màn hình liên quan" mà không nói phải kiểm gì ở đó thì không ai kiểm.

| Impact item | Ai bắt được | Đưa vào đâu |
|---|---|---|
| Hành vi hàm thuần đổi | **Unit test** | `04-quality/ut-design.md` — viewpoint tương ứng |
| Màn hình dùng chung component | **Self-test + so sánh môi trường** | `04-quality/test-checklist.md` |
| Luồng nghiệp vụ đi qua nhiều màn | **Test case / e2e** | `04-quality/testcases/` |
| Dữ liệu / batch / repo khác | **Kiểm phía consumer bằng tay** | `test-checklist.md` + ghi rõ ai kiểm |
| Chỉ khác ở một môi trường | **Kiểm đúng môi trường đó** | `test-checklist.md`, ghi rõ môi trường |

**Luật:** mỗi dòng trong bảng impact phải trỏ được sang **ít nhất một** dòng ở `test-checklist.md`, `ut-design.md`, hoặc `testcases/`. Dòng nào không trỏ được → hoặc nó không phải impact thật, hoặc đang thiếu lưới. Cả hai đều phải xử lý, không để lửng.

## Bước 7 — Hợp đồng hành vi: cái PHẢI GIỮ NGUYÊN ⭐

Ghi tường minh những hành vi **không được đổi** dù task có làm gì. Đây là mốc để self-test, UT và tester biết cái gì là "vẫn phải đúng như cũ":

```markdown
## Hành vi phải giữ nguyên
- Thứ tự tham số trên URL tìm kiếm — đối tác so chuỗi
- Định dạng ngày hiển thị `YYYY年M月D日` — có nơi parse ngược
- Trả `null` khi không có dữ liệu (không đổi thành chuỗi rỗng) — consumer đang `?? 'chưa có'`
```

Không viết ra thì mỗi người tự hiểu một kiểu, và người sửa sau không có cách nào biết.

## Mẫu `impact.md`

````markdown
# Impact — {task}

## 1. Loại thay đổi
| Thay đổi | Loại | Hướng lan toả |
|---|---|---|

## 2. Bề mặt bị chạm
| Màn hình / chức năng | Vì sao liên quan | Evidence | Tầng |
|---|---|---|---|

## 3. Ai đang dựa vào hành vi cũ
| Nơi dựa vào | Dựa vào chi tiết gì | Evidence | Đổi thì vỡ thế nào |
|---|---|---|---|

## 4. Ràng buộc ngầm
| Loại | Cụ thể | Đã kiểm chưa |
|---|---|---|

## 5. Bán kính: R{1–4} — {lý do}

## 6. Hành vi phải giữ nguyên
- …

## 7. Impact → lưới kiểm
| Impact | Lưới | Ở đâu |
|---|---|---|

## 8. Đã kiểm và KHÔNG ảnh hưởng
| Nghi ngờ ban đầu | Vì sao không ảnh hưởng | Evidence |
|---|---|---|
````

**Mục 8 quan trọng ngang các mục trên.** Nó phân biệt *"đã kiểm, không dính"* với *"chưa nghĩ tới"* — hai thứ nhìn giống hệt nhau khi bảng để trống. **Im lặng ≠ đã kiểm tra.**

## Guardrails

- **[HARD] Không kết luận "không ảnh hưởng" mà không có evidence.** Ghi vào mục 8 kèm cách đã kiểm.
- **[HARD] Không suy impact từ phía producer.** Muốn biết ai dựa vào gì thì **đọc code phía họ**.
- Không dừng ở tầng 1 (call-site). Tầng 2 và 3 là nơi bug đắt nhất nấp.
- Không chấm bán kính theo số dòng code sửa.
- Dòng impact không sinh ra được việc kiểm nào → xử lý, đừng để lửng.
