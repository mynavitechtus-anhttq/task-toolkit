# Code Evidence Method — kỹ thuật đào code chung

> Kỹ thuật thu thập evidence từ code, **dùng chung** bởi `task-survey` (phạm vi 1 task), `report/discovery-method` (phạm vi cả hệ thống), phần grounding của `analyze-spec`, và `release-note` (phạm vi 1 release, nhiều branch/env). Mỗi skill trỏ tới đây cho phần "how", giữ phần "what/when" của riêng nó.

## Nguyên tắc lõi

1. **Evidence-first** — mọi phát hiện trỏ về nguồn cụ thể `[repo] path/to/file:line`. Không có claim trần; chưa đọc được nguồn → đánh dấu, không đoán.
2. **Chứng minh, đừng khẳng định** — trước khi chốt một kết luận, sinh **một lệnh/thao tác verify** chứng minh nó (grep ra đúng, chạy ra đúng output, trạng thái đúng). Đọc code rồi suy là *giả thuyết*; verify mới là *evidence*.
3. **Đọc cả đơn vị, không chỉ dòng nghi** — mở nguyên function/class/config block, không dừng ở dòng highlight. Bug thật hay nằm ở context quanh nó (guard thiếu, scope sai, async sai thứ tự).
4. **Đọc phía consumer, không suy từ producer** — data chảy A → B thì mở code **B** đọc thật. (Bài học: đoán "batch ghi Redis" từ config producer — thực tế batch ghi DB, chỉ lộ khi đọc code consumer.) Cross-check **hai đầu** mỗi ranh giới: producer ghi format gì ↔ consumer đọc format gì. Lệch = finding.

## Bước 0 — Source Catalog (trước khi phân tích)

Liệt kê nguồn cần đọc, gắn mức: 🔴 REQUIRED / 🟡 RECOMMENDED / 🟢 OPTIONAL. REQUIRED phải đọc được, hoặc user xác nhận **NOT AVAILABLE**, mới đi tiếp. Ghi rõ **nhánh nào + phạm vi nào** đã đọc (module/service) — không đọc mông lung.

## Từ vựng grep theo hướng đào

Điều chỉnh theo stack thực tế của repo:

| Cần tìm | Grep |
|---|---|
| Entrypoint | routes/router · `cron`/`schedule` · queue consumer · CLI/command |
| Gọi đồng bộ | `fetch` · `axios` · `HttpClient` · `requests\.` · `.proto`/gRPC |
| Bất đồng bộ | `amqp` · `rabbitmq` · `kafka` · `sqs` · `redis.*pub` · `EventBus`/`EventEmitter` |
| Background job | `cron` · `scheduler` · `queue` · `worker` · `daemon` |
| Data access | ORM model/entity · migration dir · raw query (`SELECT`/`INSERT`) |
| Tích hợp ngoài | OAuth/SAML · mail/SMS client · payment · webhook |
| Cấu hình runtime | `env(` · `getenv` · `process.env` · secret/param store |

## Dependency walk — app + infra

Với MỖI thứ sẽ đụng, grep tiếp **usage ở nơi khác**. Mỗi item liên quan → 1 dòng kèm evidence, hoặc "không ảnh hưởng vì {lý do}". **Im lặng ≠ đã kiểm.**

**App-level:** component/partial/layout dùng chung → màn nào khác render? · service/usecase/helper → flow nào khác gọi (API/batch/page)? · CSS/JS bundle → page nào khác load (build config)? · DB table/cache key/config → producer/consumer nào, **kể cả repo anh em**? · URL/route/redirect/SEO?

**Infra/runtime-level** (task đụng base image / Dockerfile / workflow / config hạ tầng):
- **Artifact runtime dùng chung**: container image / base image / task definition có **service khác dùng chung** không? (1 image chạy cả web service lẫn scheduled task → đổi base ảnh hưởng cả hai, dù diff không có file batch.)
- **Hạ tầng dùng chung**: nhiều service chung **1 load balancer** (định tuyến path/host) → đo/đổi 1 cái ảnh hưởng cái khác; chung 1 DB/cache cluster.
- **CI/CD**: workflow trigger + secret/var **theo từng environment**; build phụ thuộc nhau (base build phải xong trước app build).

## Đối chiếu khai báo trùng lặp (loại bug hay bị sót nhất)

Một lớp bug **không phải lỗi logic**: cùng một sự thật khai ở **hai nơi khác layer**, và hai nơi lệch nhau — không nơi nào tự sai, chỉ không khớp và không nhìn thấy nhau.

**Cách làm: liệt kê MỌI chỗ khai báo TRƯỚC, so SAU.** Đọc lần lượt rồi mong tự phát hiện thì gần như luôn sót.

| Khai ở A | Đối chiếu B |
|---|---|
| Tên service (IaC/compose) | host/endpoint default trong code |
| Route/location (web server) | base path/URL trong app config |
| Tên resource dùng chung (cache zone, volume, queue, topic) | chỗ khai ở layer khác (base image, infra repo) |
| Branch kích hoạt deploy (`on.push`) | map branch trong workflow khác |
| Schema/format bên **ghi** | bên **đọc** |
| Env var trong code | `.env` / secret store / task definition |
| Version pin ở CI | version pin ở Dockerfile/manifest |

Lệch **im lặng** (không crash, chỉ sai hành vi) là nguy hiểm nhất — ghi rõ *cách phát hiện*, không chỉ *đã sửa*.

## Trạng thái đang chạy — đọc từ hệ thống

Version/config mỗi env, PR đã merge chưa, revision đang chạy → đọc **từ hệ thống** (git theo branch, container, console), **KHÔNG** từ memory/ghi chú/PR title. Một PR có thể vẫn OPEN dù mọi người tưởng đã merge; ghi chú phản ánh thời điểm ghi, không phải hiện tại.

## Multi-repo / multi-branch

- Lập **Repo Map**: `repo | sub-project | vai trò | tech stack | ghi chú`. Hybrid repo (BE tách, FE gộp 1 repo) → ghi source đầy đủ `[repo-fe]/apps/app-a/...`, không trộn finding giữa các app.
- Task trải nhiều scope/branch → **1 báo cáo/scope** (file riêng), ghi rõ nhánh + phạm vi đã đọc mỗi scope.
- Config runtime (env/SSM/secret) không đọc được từ code → `[MISSING-SOURCE]`, "cần verify trên env thật", không đoán.

## Uncertainty markers

| Theo nguồn | Theo độ tin | Ý nghĩa |
|---|---|---|
| `[FROM-CODE]` suy từ source | `[CONFIRMED]` đã verify | dùng được |
| `[FROM-DOCS]` từ tài liệu | `[UNVERIFIED]`/`[NEEDS-CONFIRMATION]` | kèm cách verify |
| `[FROM-TEAM]` team cung cấp | `[MISSING-SOURCE]` không thấy nguồn | ghi rõ thiếu |
| | `[OUTDATED?]` tài liệu có thể cũ | đối chiếu code hiện tại |
