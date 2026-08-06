# Code Evidence Method — kỹ thuật đào code chung

> Kỹ thuật thu thập evidence từ code, **dùng chung** bởi `task-survey` (phạm vi 1 task), `report/discovery-method` (phạm vi cả hệ thống), phần grounding của `analyze-spec`, và `release-note` (phạm vi 1 release, nhiều branch/env). Mỗi skill trỏ tới đây cho phần "how", giữ phần "what/when" của riêng nó.

## Nguyên tắc lõi

1. **Evidence-first** — mọi phát hiện trỏ về nguồn cụ thể `[repo] path/to/file:line`. Không có claim trần; chưa đọc được nguồn → đánh dấu, không đoán.
2. **Chứng minh, đừng khẳng định** — trước khi chốt một kết luận, sinh **một lệnh/thao tác verify** chứng minh nó (grep ra đúng, chạy ra đúng output, trạng thái đúng). Đọc code rồi suy là *giả thuyết*; verify mới là *evidence*.
3. **Đọc cả đơn vị, không chỉ dòng nghi** — mở nguyên function/class/config block, không dừng ở dòng highlight. Bug thật hay nằm ở context quanh nó (guard thiếu, scope sai, async sai thứ tự).
4. **Công cụ thay được thao tác, không thay được phán đoán.** Đồ thị code trả lời *"ai gọi cái này"* nhanh và chính xác hơn grep. Nó **không** trả lời *"chỗ nào coupling qua tên bảng"*, *"khai báo hai nơi có lệch không"*, hay *"đọc phía nào mới đúng"* — ba câu đó vẫn là việc của người.
5. **Đọc phía consumer, không suy từ producer** — data chảy A → B thì mở code **B** đọc thật. (Bài học: đoán "batch ghi Redis" từ config producer — thực tế batch ghi DB, chỉ lộ khi đọc code consumer.) Cross-check **hai đầu** mỗi ranh giới: producer ghi format gì ↔ consumer đọc format gì. Lệch = finding.

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

## Dependency walk — ba tầng, không tầng nào bỏ được

Mỗi tầng bắt một loại quan hệ khác nhau. Công cụ chỉ thay được **tầng 1**.

### Tầng 1 — Reference trong code *(dùng công cụ nếu có, grep nếu không)*

Quan hệ **gọi hàm, implement interface, kế thừa, inject qua DI**. Đây là chỗ grep yếu nhất: nó khớp chuỗi nên mù với dynamic dispatch, DI container, facade, magic method.

**Bước 1.1 — Dò xem có công cụ chưa:**

```bash
command -v codegraph            # CLI đã cài toàn cục chưa
codegraph status                # repo này đã index chưa + index có đủ không
```

**Bước 1.2 — Chưa có thì HỎI, không tự cài.** Nêu đủ ba điều rồi chờ đồng ý:

> **Mục đích** — dựng sẵn đồ thị symbol để tìm reference chính xác hơn grep: đi được qua interface, DI, kế thừa; kèm blast radius và map test hiện có cho từng symbol.
>
> **Sẽ làm gì trên máy** — cài CLI toàn cục (`npm i -g @colbymchenry/codegraph`), đăng ký MCP server vào agent (Claude Code / Codex / Cursor), và tạo `.codegraph/` trong repo. Index cỡ **~64 MB cho repo 1.600 file**; thư mục này tự gitignore.
>
> **Không cài cũng được** — phương pháp vẫn chạy bằng grep, chỉ chậm hơn và sót các trường hợp gọi gián tiếp.

Đồng ý → cài theo thứ tự: `npm i -g @colbymchenry/codegraph` → `codegraph install` (chọn agent) → `codegraph init` trong repo.

**Bước 1.3 — LUÔN chạy `codegraph status` trước khi tin kết quả.** Index dở dang **không báo lỗi**, chỉ thiếu cạnh im lặng:

```
⚠ 7,486 references from an interrupted run are awaiting resolution
  — some callers/impact edges are missing. Run "codegraph sync"
```

Thấy dòng đó → `codegraph sync` rồi mới hỏi tiếp.

**Bước 1.4 — Truy vấn:**

| Cần gì | Lệnh |
|---|---|
| Ai gọi symbol này | `codegraph callers <symbol>` |
| Symbol này gọi ai | `codegraph callees <symbol>` |
| Blast radius + test hiện có | `codegraph explore <symbol>` |
| Phạm vi ảnh hưởng nhiều tầng | `codegraph impact <symbol> --depth 3` |
| Test nào bị ảnh hưởng bởi file đã đổi | `codegraph affected <files...>` |

⚠ **Hỏi cả interface lẫn class.** Consumer thường đi qua interface; hỏi mỗi class sẽ chỉ ra binding trong service provider, thiếu chỗ dùng thật.

**Không có công cụ** → grep theo bảng từ vựng bên dưới, và chấp nhận sót gọi gián tiếp — ghi rõ `[UNVERIFIED]` cho phần nghi có nhưng không grep ra.

### Tầng 2 — Coupling KHÔNG qua code *(luôn grep, công cụ mù hoàn toàn)*

Đây là chỗ đồ thị code **không bao giờ thấy**, vì hai bên không gọi nhau — chúng chỉ cùng chạm một cái tên.

| Coupling qua | Grep cái gì |
|---|---|
| **Bảng / cột DB** | tên bảng dạng chuỗi trong query, tên cột, migration |
| **Cache key · queue · topic** | chuỗi key, prefix |
| **Đường dẫn file trên storage dùng chung** | path literal, biến path, mount point |
| **Route / URL / redirect** | chuỗi path, tên route |
| **Tên env var** | `env(` · `getenv` · `process.env` |

> **Đã đo:** `codegraph query mt_entry` → *No results*, trong khi `grep -rl mt_entry` ra **5 file**. Tên bảng là chuỗi trong câu query, không phải symbol — tree-sitter không dựng cạnh cho nó.
>
> Tầng này là chỗ ba phát hiện đắt nhất của một task thật đã nằm: batch ghi ngược vào thư mục publish của hệ khác · danh sách id hardcode trong config nginx · join bằng so khớp chuỗi trong nội dung. **Không cái nào là quan hệ gọi hàm.**

### Tầng 3 — Khai báo chéo layer *(luôn thủ công)*

Xem mục **Đối chiếu khai báo trùng lặp** ngay dưới. Không công cụ nào làm được vì nguồn không phải code: YAML workflow, Dockerfile, IaC, task definition.

### Phạm vi từng tầng — nhắc khi vẽ sơ đồ

Sơ đồ dựng từ tầng 1 **chỉ có quan hệ trong code**. Xuất sơ đồ ra tài liệu thì phải ghi rõ điều đó, kẻo người đọc tưởng đã đủ.

---

### Danh mục cần walk (áp cho cả ba tầng)

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
