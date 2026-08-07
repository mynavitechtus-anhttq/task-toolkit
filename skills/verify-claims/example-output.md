# Ví dụ output — `verify-claims`

> Few-shot cho agent và mẫu đối chiếu cho người. Dựa trên một bộ tài liệu phân tích hệ thống có thật về hình dạng: khảo sát một CMS trước khi nâng cấp. Đánh dấu 👀 những chỗ hay bị làm sai nhất.

---

## Verify Claims — `analysis/technical/architecture-discovery.md` + `README.md`

**Chế độ:** `report-only` · **Đã bóc:** 34 claim kiểm được (loại bỏ 11 câu là ý kiến/đề xuất)

| | |
|---|---|
| ✅ verified | 26 |
| ❌ contradicted | 5 |
| ⚠ unverifiable | 3 |

👀 **Con số 11 câu bị loại ở bước 1 cũng phải nói ra.** Nó cho người đọc biết phạm vi: 34 claim được kiểm, 11 câu là ý kiến nên không kiểm. Chỉ ghi "kiểm 34 claim" thì không ai biết 11 câu kia bị bỏ có chủ ý hay bị sót.

## 1 · Vi phạm (blocking)

| # | Claim | Vị trí | Cách kiểm | Thực tế | Conf |
|---|---|---|---|---|---|
| 1 | site `介護のみらいラボ` có **14** blog con | `architecture-discovery.md:88` | đếm `mt_blog` có `blog_class='blog'` và `blog_parent_id = 7` trong `reference/cms-ddl.sql` | **12** | `100` |
| 2 | `php artisan test --testsuite=Job` | `README.md:441` | `phpunit.xml` khai testsuite nào | chỉ có `Unit` · `Feature` · `Unit-Tests` · `Feature-Tests` — **không có testsuite theo module**. Lệnh trả `Unknown testsuite` | `100` |
| 3 | *(như trên)* | `README.ja.md:441` | — | **bản JA sai y hệt** → parity §4.3 | `100` |
| 4 | `pest src/Job/Tests/Feature/JobApiTest.php` | `README.md:460` | file có tồn tại không | ✖ `missing file`. Thư mục đó chỉ có `JobCountApiTest.php` | `100` |
| 5 | template dùng `GetHashVar` ở "một vài chỗ" | `function-list.md:142` | grep `GetHashVar` trên 893 template thật | **0 chỗ**. Claim khẳng định một thứ không tồn tại | `100` |

👀 **Dòng 1 và dòng 5 là hai loại sai khác nhau, đừng gộp.** Dòng 1 là *sai số lượng* — có thật, đếm nhầm. Dòng 5 là *khẳng định một thứ không tồn tại* — nguy hiểm hơn, vì nó kéo theo cả một hạng mục công việc không cần làm. Trong report gửi khách, hai cái này dẫn tới hai hành động khác nhau.

👀 **Dòng 2 và 3 tách riêng dù cùng một lỗi.** Cùng nội dung nhưng **hai file phải sửa**. Gộp một dòng thì người sửa gần như chắc chắn quên bản JA — đó chính là lỗi parity mà §4.3 sinh ra để bắt.

👀 **Cột `Thực tế` không được để trống hoặc ghi "sai".** Dòng 1 ghi `12`, dòng 4 ghi tên file thật. Không có cột này thì người sửa phải đi điều tra lại từ đầu, và bảng chỉ tiết kiệm được đúng một nửa công.

## 2 · Không chặn (non-blocking)

| # | Claim | Vị trí | Ghi chú |
|---|---|---|---|
| 6 | "batch chạy lúc 15:00 JST" | `integration-catalog.md:56` | Đúng với crontab hiện tại, nhưng crontab có comment `# tạm, chờ khách chốt` ngay trên. Claim đúng **tại thời điểm kiểm**, không đúng lâu dài — nên ghi kèm điều kiện |

## 3 · Validation notes

**Đã kiểm — phủ hết:**

| Loại claim | Số | Nguồn dùng |
|---|---|---|
| 1 · số lượng | 9 | `cms-ddl.sql`, đếm file thật |
| 2 · định danh | 12 | grep + CodeGraph |
| 5 · đường dẫn/link | 7 | kiểm tồn tại trên đĩa |
| 6 · lệnh | 4 | đối chiếu `phpunit.xml`, `composer.json` |

**Chưa kiểm được (`unverifiable`) — 3 claim:**

| Claim | Vị trí | Vì sao không kiểm được | Cần gì mới kiểm được |
|---|---|---|---|
| "MTAppjQuery là sản phẩm thương mại" | `upgrade-impact.md:23` | Claim về **bên thứ ba**. Không có dấu vết nào trong repo trả lời được câu này | Tra trang phát hành / GitHub của thư viện. Kiểm bằng code **không bao giờ ra** |
| "`JOB_SEARCH_CACHE_TTL` ở prod là 3600" | `impact.md:31` | Không đọc config môi trường production — theo thoả thuận | Khách xác nhận, hoặc được phép đọc. **Không suy từ staging** |
| "chức năng cộng đồng không còn ai dùng" | `function-list.md:88` | Claim **phủ định** về hành vi người dùng, không phải về code | Log truy cập, hoặc khách xác nhận |

👀 **Ba dòng này là phần có giá trị nhất của cả bản kiểm, không phải phần thừa.** Chúng nói chính xác chỗ nào tài liệu **chưa được ai chứng minh** — và trong ba dòng thì hai dòng phải hỏi khách, không có cách nào tự làm. Nhét chúng xuống danh sách vi phạm là sai (chưa chứng minh được là sai), im lặng bỏ qua còn tệ hơn (người đọc tưởng đã kiểm hết).

👀 **Claim phủ định luôn khó nhất.** Dòng thứ ba là ví dụ: "không còn ai dùng" không thể chứng minh bằng repo — code vẫn còn đó, chỉ có log mới trả lời được. Đừng để một lần grep không ra kết quả biến thành `verified`.

**Rủi ro còn lại:**

- 12 claim loại 2 (định danh) kiểm bằng grep + CodeGraph nên **tối đa đạt `75`**. Gọi động, tên ghép chuỗi, tên qua config đều lọt. Nếu cần chắc hơn thì phải chạy thật và quan sát.
- Không kiểm claim loại 3 (phiên bản) của các thư viện phụ thuộc gián tiếp — chỉ kiểm mức khai báo trực tiếp trong `composer.json`.

---

## Đối chiếu nhanh trước khi báo xong

- [ ] Mọi dòng `contradicted` có cột **`Thực tế`** điền cụ thể, không ghi "sai"
- [ ] Mọi dòng `unverifiable` có **"cần gì mới kiểm được"**
- [ ] `100` chỉ dùng cho nguồn khai báo hoặc quan sát trực tiếp — grep tối đa `75`
- [ ] Bằng chứng nằm **ngoài** tài liệu đang kiểm
- [ ] Claim phủ định đã quét hết, không kết luận từ một lần grep không ra
- [ ] Tài liệu đa ngôn ngữ → đã đối chiếu bản khác, mỗi bản một dòng riêng
- [ ] Ý kiến / đề xuất / dự đoán đã bị loại ở bước 1, có ghi số lượng đã loại
- [ ] Không có vi phạm → vẫn phải có **Validation notes** đầy đủ, không được để trống
