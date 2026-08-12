---
name: perf-check
description: >-
  Performance gate for ANY project — triage what one change costs at runtime and write
  01-discovery/performance.md, or audit a whole surface against Core Web Vitals and backend budgets.
  Enforces measure-before-optimize: every claim needs a number with the condition it was measured under
  (environment, data volume, device class), and "seems slow" is not a finding. Carries concrete budgets
  (LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB <800ms · JS <200KB gz · API p95 <200ms) and triages six
  layers in diagnostic order — TTFB breakdown (DNS/TLS/server-think/transfer/queue) · backend (N+1,
  missing index, expensive counts) · frontend · NETWORK (compression, cache headers, CDN, round trips,
  payload size, connection reuse) · INFRASTRUCTURE (connection-pool vs instance count, autoscale warm-up,
  cold start, timeout/retry storms, storage IOPS, Redis eviction and cache stampede, batch colliding with
  peak) · load & data growth · and whether the system is observable in production at all. Trigger on "check
  performance", "task này có ảnh hưởng hiệu năng không", "trang chậm", "tối ưu tốc độ", "perf budget",
  or as the performance gate of analyze-spec. NOT for security review (that is security-check) and NOT
  for load testing itself — it decides what to measure and reads the numbers, it does not generate traffic.
  Locale vn (default) / en / ja.
---

# Perf Check — cổng hiệu năng

> **Cấu trúc workspace + skill nào ghi vào đâu**: [`../_shared/workspace-layout.md`](../_shared/workspace-layout.md) — nguồn duy nhất, đừng chép lại đường dẫn.

> Ngôn ngữ giao tiếp: tiếng Việt. Output theo `locale` (mặc định vn). Gõ `perf-check help` → in Help cuối file, không chạy gì.

> **Luật số một: đo trước, tối ưu sau.** Không có số đo thì không có vấn đề hiệu năng — chỉ có cảm giác. Mọi kết luận trong file này phải kèm **số** và **điều kiện đo** (môi trường, lượng dữ liệu, loại máy).

## Bước 1 — Có cần chạy không (6 tín hiệu)

Chạy nếu task chạm **ít nhất một**:

1. **Truy vấn dữ liệu** — thêm/sửa query, join, vòng lặp gọi DB, batch
2. **Danh sách / phân trang / tìm kiếm** — nơi lượng dữ liệu tăng theo thời gian
3. **Tài nguyên trang** — thêm ảnh, font, thư viện JS/CSS, script bên thứ ba
4. **Đường đi mạng** — thêm lời gọi API, webhook, service ngoài
5. **Xử lý nặng** — export, import, sinh file, ảnh, cron/batch
6. **Hạ tầng** — đổi sizing/autoscale, thêm instance, đổi loại lưu trữ, đổi cấu hình pool/timeout/cache

Không chạm mục nào → ghi vào `technical-approach.md`: **"không ảnh hưởng hiệu năng"** kèm lý do. Không tạo `performance.md` rỗng.

## Bước 2 — Ngân sách (dùng làm mốc, không phải để trang trí)

| Chỉ số | Tốt | Cần cải thiện | Kém |
|---|---|---|---|
| **LCP** — nội dung chính hiện ra | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** — phản hồi khi bấm | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** — layout nhảy | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| **TTFB** — byte đầu tiên | < 800ms | | |
| **JS bundle** (initial) | < 200KB gzip | | |
| **API p95** | < 200ms | | |
| **Long task** | < 50ms mỗi tác vụ | | |
| **Nén** | bật cho mọi text response | | |
| **Server think time** | < 200ms (phần TTFB thuộc backend) | | |
| **DB connection pool** | tổng kết nối < 70% giới hạn DB | | |

Dự án có ngân sách riêng (SLA khách, ràng buộc hạ tầng) → **dùng số của dự án**, ghi rõ nguồn. Không có thì dùng bảng trên và nói rõ đó là mốc chung.

## Bước 3 — Triage theo tầng

> **Thứ tự tìm, không tìm ngẫu nhiên.** Đi từ ngoài vào trong: *người dùng thấy chậm ở đâu* → **TTFB** (mạng hay server?) → nếu server thì **backend** → nếu sau TTFB thì **frontend**. Checklist không kèm thứ tự thì người ta tick từ trên xuống và bỏ sót đúng chỗ nghẽn.

### TTFB — tách nhỏ để biết nghẽn nằm đâu

TTFB gộp 5 phần rất khác nhau; không tách thì mọi kết luận đều là đoán:

| Phần | Nghi ngờ khi | Xử lý thuộc tầng |
|---|---|---|
| DNS | lần đầu chậm, lần sau nhanh | Mạng |
| TCP + TLS handshake | chậm đều, xa vùng đặt server | Mạng / hạ tầng |
| **Server think time** | chậm cả khi mạng tốt | Backend |
| Truyền dữ liệu | payload lớn, không nén | Mạng |
| Chờ hàng đợi / cold start | chậm lẻ tẻ, chậm sau lúc rảnh | Hạ tầng |

Đọc từ waterfall trong devtools hoặc log của reverse proxy. **TTFB > 800ms mà server think time nhỏ → vấn đề ở mạng/hạ tầng, tối ưu query là tối ưu nhầm chỗ.**

### Backend

- [ ] **N+1** — vòng lặp có gọi DB bên trong; ORM lazy-load trong `foreach`. *Đây là nguyên nhân số một và rẻ nhất để tìm.*
- [ ] **Index** — cột trong `WHERE` / `JOIN` / `ORDER BY` đã có index chưa; đọc `EXPLAIN`, đừng đoán
- [ ] **Lấy thừa** — `SELECT *`, load cả bảng rồi lọc trong code, không phân trang
- [ ] **Đếm đắt** — `COUNT(*)` trên bảng lớn mỗi lần render
- [ ] **Cache** — dữ liệu ít đổi có cache chưa; cache có invalidate đúng chỗ không
- [ ] **Gọi ngoài** — API bên thứ ba có timeout và fallback chưa; có gọi tuần tự thứ song song được không
- [ ] **Việc nặng chạy đồng bộ** — gửi mail, sinh file, resize ảnh nên đẩy sang queue

### Frontend

- [ ] **Ảnh** — đúng kích thước hiển thị · định dạng hiện đại · `width`/`height` để không nhảy layout · lazy-load ảnh dưới màn hình *(nhưng **không** lazy-load ảnh LCP)*
- [ ] **JS** — bundle initial < 200KB gz · tách code theo route · bỏ thư viện chỉ dùng một hàm
- [ ] **CSS** — không chặn render bởi CSS không dùng
- [ ] **Font** — 2–3 họ, 2–3 độ đậm · `font-display` để chữ không biến mất
- [ ] **Script bên thứ ba** — mỗi cái là một khoản chi; cái nào chặn render?
- [ ] **Render** — danh sách dài có ảo hoá không · có tính toán nặng trong render không

### Mạng

- [ ] **Nén** — gzip/brotli đã bật cho HTML/CSS/JS/JSON chưa
- [ ] **Cache header** — `Cache-Control`, `ETag` đúng cho tài nguyên tĩnh; tài nguyên có hash tên file thì cache dài
- [ ] **CDN** — tài nguyên tĩnh có qua CDN không · CDN có ở gần người dùng không (khách Nhật mà origin ở vùng khác là cộng thẳng độ trễ mỗi request)
- [ ] **Số vòng lượt** — một màn hình gọi bao nhiêu request tuần tự; có gộp được không · có waterfall chờ nhau không
- [ ] **Kích thước payload** — API trả thừa trường không dùng · ảnh/JSON không nén
- [ ] **Kết nối lại** — HTTP/2 hoặc keep-alive đã bật chưa; mỗi request bắt tay TLS lại là rất đắt

### Hạ tầng

- [ ] **Connection pool** — số kết nối DB tối đa **so với** số instance × pool size. Đây là lỗi giết hệ thống êm nhất: chạy tốt ở 2 instance, sập ở 10
- [ ] **Sizing & autoscale** — CPU/RAM giới hạn bao nhiêu · ngưỡng scale-out · **thời gian khởi động** (scale ra sau 3 phút thì lúc cần nhất vẫn không có)
- [ ] **Cold start** — serverless/container mới lên mất bao lâu; có ảnh hưởng request thật không
- [ ] **Timeout & retry** — timeout mỗi tầng có ngắn dần từ ngoài vào trong không · retry có backoff không (**retry không backoff biến một sự cố nhỏ thành bão request**)
- [ ] **Lưu trữ** — IOPS/throughput của volume (mạng-attached như EFS/NFS chậm hơn đĩa cục bộ nhiều lần cho thao tác nhiều file nhỏ)
- [ ] **Cache tầng ứng dụng** (Redis/Memcached) — số kết nối · kích thước key/value · TTL · chính sách eviction · **cache stampede** khi key hết hạn đồng loạt
- [ ] **Batch/cron** — có chạy trùng giờ cao điểm không · có khoá bảng lâu không
- [ ] **Log** — ghi log đồng bộ vào đường đi request không · lượng log có làm nghẽn I/O không

### Tải & tăng trưởng dữ liệu

Đây là nhóm **không lộ ra ở môi trường dev** và là nguyên nhân của phần lớn sự cố "tự nhiên chậm":

- [ ] **Dữ liệu tăng theo thời gian** — query này 6 tháng nữa chạy trên bao nhiêu bản ghi? Nhanh ở 10k dòng, chết ở 10M
- [ ] **Cao điểm vs trung bình** — con số đo lúc vắng không nói gì về lúc đông; biết giờ cao điểm của hệ thống chưa
- [ ] **Hành vi khi quá tải** — chậm dần hay sập? Có hàng đợi, có giới hạn tốc độ, có ngắt mạch không
- [ ] **Nhân theo tỉ lệ** — thay đổi này chạy 1 lần/request hay 1 lần/bản ghi? ×1000 bản ghi thì thành bao nhiêu

### Quan sát được không

Không đo được ở prod thì luật "đo trước" chỉ là khẩu hiệu:

- [ ] Có số liệu người dùng thật không, hay chỉ đo trên máy dev
- [ ] Slow query log có bật không · ngưỡng bao nhiêu
- [ ] Có theo dõi được p95/p99 không — **trung bình che mất đúng nhóm người dùng đang khổ**
- [ ] Có cảnh báo khi vượt ngân sách không, hay đợi người dùng báo

## Bước 4 — Đo, rồi mới kết luận

Thứ tự bắt buộc: **đo hiện trạng → xác định điểm nghẽn → sửa → đo lại**. Bỏ bước đo đầu thì không chứng minh được đã cải thiện, và rất hay tối ưu nhầm chỗ.

Ghi lại **điều kiện đo** cùng con số — thiếu điều kiện thì con số vô nghĩa:

- Môi trường nào (local / dev / stg / prod)
- Lượng dữ liệu (bao nhiêu bản ghi — 10 dòng và 100k dòng là hai bài toán khác nhau)
- Loại máy / mạng (đo trên máy dev cấu hình cao che mất vấn đề của người dùng thật)
- Lần đo thứ mấy (lần đầu có thể chưa có cache)

````markdown
# Performance — {task}

> Tín hiệu: {liệt kê} · Ngân sách áp dụng: {nguồn}

## Kết luận
{1–3 câu: task này làm gì chậm đi/nhanh lên, số bao nhiêu, có vượt ngân sách không}

## Số đo
| Chỉ số | Trước | Sau | Ngân sách | Điều kiện đo |
|---|---|---|---|---|
| Thời gian trang X | 3.2s | 0.9s | ≤ 2.5s | stg · 24k bản ghi · Chrome desktop · lần 2 |

## Điểm nghẽn tìm được
| Điểm nghẽn | Bằng chứng | Xử lý | Ticket |
|---|---|---|---|
| N+1 khi render danh sách | 41 query/request (log) | eager load | 12 |

## Chưa đo được
| Gì | Vì sao | Cách đo khi có điều kiện |
|---|---|---|
````

## Guardrails

- **[HARD] Không tối ưu khi chưa đo.** "Chỗ này chắc chậm" không phải phát hiện. Không đo được thì ghi vào mục *Chưa đo được* kèm cách đo — đừng sửa mò.
- **[HARD] Không dùng số đo trên máy dev làm kết luận cho người dùng thật.** Máy dev nhanh hơn, mạng tốt hơn, dữ liệu ít hơn.
- Không gộp nhiều thay đổi rồi đo một lần — không biết cái nào có tác dụng.
- Không tối ưu thứ chạy 1 lần/tháng trong khi thứ chạy mỗi request đang chậm. Ưu tiên theo **tần suất × chi phí**.
- **Không kết luận từ một lần đo.** Lần đầu chưa có cache, lần sau có — đo ít nhất 3 lần và ghi rõ lần thứ mấy.
- **Không suy hiệu năng prod từ dev.** Khác cấu hình, khác lượng dữ liệu, khác độ trễ mạng — ba thứ đủ để đảo ngược kết luận.
- Cache không phải câu trả lời mặc định. Cache sai chỗ đổi một bug chậm lấy một bug **dữ liệu cũ** — khó tìm hơn nhiều.

## Help

```
perf-check <TICKET-ID> [locale=vn|en|ja]
  Triage ảnh hưởng hiệu năng của 1 thay đổi → 01-discovery/performance.md.
  Chạy khi task chạm: truy vấn dữ liệu · danh sách/phân trang · tài nguyên trang · gọi mạng · xử lý nặng · hạ tầng.
  Triage 6 tầng theo thứ tự chẩn đoán: TTFB → backend → frontend → mạng → hạ tầng → tải & tăng trưởng dữ liệu.
  Ngân sách mặc định: LCP ≤2.5s · INP ≤200ms · CLS ≤0.1 · TTFB <800ms · JS <200KB gz · API p95 <200ms.
  Luật cứng: đo trước — mọi số phải kèm điều kiện đo (môi trường · lượng dữ liệu · loại máy).
```
