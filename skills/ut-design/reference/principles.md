# Ba nguyên tắc cốt lõi

> Ba nguyên tắc dưới đây là **nền tảng**. Mọi thứ còn lại trong bộ này — 30 viewpoint, playbook, adapter, script — chỉ là diễn giải và cách thực thi chúng. Gặp tình huống không có luật nào phủ, quay về đây quyết.

## 1 · Xác định quan điểm trước, viết mã test sau

Thiết kế quan điểm kiểm thử là **một bước độc lập và review được**, hoàn tất **trước** khi viết mã test. Không để agent chuyển thẳng sang sinh code khi chưa chốt quan điểm.

**Vì sao tách hai bước:** nhảy thẳng vào code thì **cả người lẫn agent** đều có xu hướng chỉ test happy path. Tách "quan điểm" thành bước riêng buộc phải liệt kê case bất thường, biên, ngoại lệ **trước** — lúc còn rẻ, và lúc còn review được bằng mắt thường.

Đây là lý do `ut-generate` từ chối chạy khi chưa có bảng thiết kế. Không phải thủ tục.

## 2 · Độ phủ là mức tối thiểu, không phải mục tiêu

"Đủ test" nghĩa là **đã bao phủ toàn bộ quan điểm áp dụng**, không phải đạt một tỷ lệ phần trăm.

**Độ phủ 100% nhánh vẫn có thể bỏ sót hành vi.** Chạy qua hết mọi dòng code không chứng minh đã kiểm đúng hành vi — đó là hai câu hỏi khác nhau. Đạt 100% branch mà thiếu nhóm D (tương tác, side-effect) hoặc E (thứ tự, bất định) là **chưa xong**.

Con số 90–100% nhìn rất an tâm, và chính vì thế nó là chỉ số **dễ bị làm đẹp** nhất. Điều kiện dừng là cổng DoD §3, không phải phần trăm.

## 3 · Chất lượng phải chứng minh được, không chỉ "pass"

Mỗi test gắn với **mã quan điểm**; kết quả kèm **bảng truy vết** quan điểm → test. Test "pass" nhưng không chứng minh được độ bao phủ quan điểm thì **chưa đạt**.

Đây là lý do mọi test phải có `// viewpoint:<ID>` và mọi lần chạy phải xuất bảng truy vết. Không có hai thứ đó thì "đã test rồi" là một lời khẳng định không ai kiểm được.

---

## Điểm chung của cả ba

Cả ba nguyên tắc kéo chất lượng Unit Test từ chỗ **đánh giá cảm tính hoặc dựa trên con số** sang **tiêu chí kiểm chứng và review được** — kể cả với test do AI sinh ra.

> **"Chạy được" và "đúng" là hai chuyện khác nhau. Coverage cao và chất lượng test cũng vậy.**

## Vì sao việc này không chỉ là chuyện của developer

Ba thứ đang đổi cùng lúc, và cả ba đều đẩy rủi ro chất lượng ra khỏi tay riêng của người viết code:

| | |
|---|---|
| **AI sinh test tràn vào** | Agent viết hàng loạt test trong vài giây, rất tự tin. Nhưng nó dễ tạo test **"xanh giả"** — chạy qua code mà không thực sự bắt được bug |
| **Coverage cao đánh lừa người quản lý** | Đây là con số APM/TL đo hằng ngày. Chỉ nhìn coverage % là **đang đo sai thứ** |
| **Bug lọt UT càng đi xa càng đắt** | Một bug lẽ ra UT bắt được, nếu lọt xuống integration hay production thì chi phí sửa tăng gấp nhiều lần và ảnh hưởng khách hàng Nhật trực tiếp |

## Vì sao có guardrail §1

Agent **không xấu** — nó tối ưu cho "test xanh". Không chặn thì nó sẽ đạt màu xanh bằng những cách vô hiệu hoá chính mục đích của test.

> **Guardrail không phải để làm khó agent. Nó để agent không thể đánh lừa reviewer.**

Sáu chiêu quen thuộc, và playbook chặn từng cái:

| Chiêu "xanh giả" | Playbook |
|---|---|
| Sửa code production cho khớp test | MUST NOT — test đỏ = **báo nghi vấn bug**, dừng & hỏi |
| Làm yếu assertion để pass (`!= null`, bỏ assert) | MUST NOT nới/bỏ assertion |
| Xoá / skip test đang đỏ | MUST NOT skip/xoá/comment-out |
| Chạy code rồi dán output làm `expected` | `expected` PHẢI suy từ spec — cấm golden-by-implementation |
| Assert tautology / assert lại giá trị mock tự trả | Cấm |
| Dừng khi coverage % đẹp | Điều kiện dừng là **cổng Done**, không phải % |

## Ai chủ trì, ai review

**Developer chủ trì UT.** Cả bước 2 (quan điểm) lẫn bước 3 (mã test) đều **có thể yêu cầu review** tuỳ loại dự án — mức review do APM/Team Lead quyết định theo **Ma trận Yêu cầu Review** của dự án.

Nghĩa là: bảng kế hoạch viewpoint và bảng truy vết không chỉ là output kỹ thuật. Chúng là **thứ người review cầm để soát**. Viết cho người đọc được, không viết cho máy đọc xong rồi thôi.
