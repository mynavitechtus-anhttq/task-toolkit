---
name: release-note
description: >-
  Build a release note / deployment runbook for a RELEASE (many tickets at once) on ANY project — not for
  a single task. Anchors on the release diff (a ref range such as staging..main or the merged-PR list
  since the last release), enriches each item from the task artifacts this toolkit already wrote
  (tasks/{ID}/backlog.md, impact.md, report-*.md) and falls back to PR title/body/diff for tickets that
  never went through the toolkit. Auto-derives the Affected Matrix (Frontend / Backend / AWS Config /
  Email / SMS / Data Migration-Seeder / Batch / Cache) from changed paths, plus a downtime & coordination
  assessment, then drafts deployment / smoke-test / rollback steps from those signals. Always asks three
  things it must not guess — date & time (JST), environment (STG or PRODUCTION), and deploy method
  (CI/CD, AWS CLI/CDK, FTP, manual console) — plus version, PIC and UAT status, all in one round. Output
  is BILINGUAL EN/JA (labels and content). Renders md (source of truth) + xlsx (fills the company
  template) + pdf/docx. Runs as its OWN process at deploy-prep time — NOT a stage of the per-task
  pipeline. Trigger on "viết release note", "release note cho lần release này", "làm runbook deploy",
  "リリースノート作成".
---

# Release Note / Deployment Runbook (per-release — quy trình riêng)

> Ngôn ngữ giao tiếp: tiếng Việt. **Output SONG NGỮ EN/JA** — cả nhãn section lẫn nội dung đều viết 2 thứ tiếng (như template công ty: `詳細 / DETAIL`, và mỗi mô tả có dòng EN + dòng JA, phân cách `ーーーー` như file mẫu). Gõ `release-note help` → in Help cuối file, không chạy gì.

> **Ai nghĩ, ai gõ** — bước *phán đoán* (nêu giả thuyết, chọn hướng, chốt kết luận, quyết định đánh đổi) là của **người phụ trách**; AI chỉ đưa *câu hỏi* hoặc *lựa chọn kèm đánh đổi* khi họ bí, không kết luận thay. Bước *thao tác* (grep, chạy lệnh verify, dựng bảng, soạn nháp theo template) AI làm, người soát từng dòng. Xem README §Nguyên tắc gốc.

Sinh **release note kiêm deployment runbook** cho MỘT LẦN RELEASE (gồm N ticket). Khác mọi skill còn lại của bộ: chúng chạy trên **1 task**, skill này chạy trên **1 release**.

**KHÔNG nằm trong pipeline per-task.** Gọi riêng lúc chuẩn bị deploy, sau khi task/ticket đã done và merge.

```
[per-task]  task-init → survey → analyze-spec → planning → report → backlog-ticket
                              ↓ artifact tích trong tasks/{ID}/
[per-release, gọi riêng]                    release-note  ← lúc chuẩn bị deploy
```

## Bước 1 — Adapter: quy ước dự án

| Cần | Lấy từ |
|---|---|
| `TEMPLATE_XLSX` | `.claude/release-note-template.xlsx` của repo → fallback `assets/release-note-template.xlsx` trong plugin |
| `ENV_URL` | URL production (CLAUDE.md / repo config) |
| `VERSION_FMT` | vd `WEB: v1.0.32` |
| `RELEASE_FLOW` | cặp ref mặc định (vd `staging..main`) — suy từ PR gần đây hoặc gitflow của repo |
| `PIC` mặc định | nếu repo có khai; không thì hỏi |

## Bước 2 — Xác định phạm vi release (BẮT BUỘC, làm trước mọi thứ)

Release note sai phạm vi thì mọi mục sau đều sai. Lấy phạm vi bằng **dữ liệu**, không hỏi trí nhớ:

- Cặp ref: `git log <from>..<to>` (vd `main..staging` = thứ sắp lên prod), hoặc tag trước → HEAD.
- Hoặc danh sách PR đã merge: `gh pr list --base <target> --state merged` từ lần release trước.
- Đối chiếu 2 nguồn; lệch → báo user chốt, không tự chọn.

Xuất: danh sách `ticket-id | PR# | title | merge date`. Ticket không rút được ID → vẫn liệt kê, đánh dấu `[không trace được ticket]`.

## Bước 2.5 — Đối chiếu hiện trạng (4 thứ KHÔNG suy được từ diff)

Bước 4 và 5 lấy tín hiệu từ diff. Diff nói **thay đổi gì**, không nói **đang ở đâu**. Bốn thứ dưới đây phải đọc từ hệ thống — không đoán, không lấy từ ghi chú cũ.

> Đây là hai kỹ thuật lõi ở [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md) — **"Trạng thái đang chạy — đọc từ hệ thống"** (2.5.1/2.5.2) và **"Đối chiếu khai báo trùng lặp"** (branch trigger ↔ map env, version pin CI ↔ Dockerfile) — áp ở **phạm vi release** (N ticket, nhiều branch/env cùng lúc). Bước 4 (matrix) chính là **dependency walk** ở file chung, chạy trên diff cả release.

**2.5.1 — Trạng thái thực tế đang chạy của từng môi trường.** Mục "施策内容" là câu *"từ X sang Y"*; đoán sai X là sai cả câu. Đọc thứ mang version **theo từng branch**, đừng đọc ở working tree:

```bash
for b in <dev> <stg> <prod>; do git show origin/$b:<file-mang-version> | grep -m1 '<pattern>'; done
```

Chắc hơn thì đọc version thật trong artifact/container đang chạy. **Ghi chú và PR cũ không phải bằng chứng** — một PR release có thể vẫn đang mở dù mọi người tưởng đã merge, và môi trường vẫn ở bản cũ.

**2.5.2 — Branch ↔ môi trường, và chiều đi thật của code.** Lấy map từ **trigger của chính CI** (nhánh nào kích hoạt deploy nào), không suy từ tên branch. Rồi kiểm chiều đi thật bằng quan hệ tổ tiên: một commit **có** nằm trong branch kia không (`git merge-base --is-ancestor <commit> origin/<branch>`). Nhiều dự án có nhánh dev là **ngõ cụt** — code lên staging/prod bằng đường khác. Không biết thì viết sai phần điều phối và không hiểu vì sao PR vào dev lại conflict.

**2.5.3 — Kiểm kê đường lùi, theo hiện vật cụ thể.** Câu "rollback: revert PR" là vô dụng khi có sự cố. Ba tầng, mỗi tầng một hiện vật, và phải xác nhận nó **còn tồn tại**:

| Tầng | Hiện vật lùi về | Điều kiện |
|---|---|---|
| Artifact (image/package) | phiên bản trước trong registry | chưa bị xoá / lifecycle policy chưa thu hồi |
| Deployment (orchestrator) | revision/generation đang chạy | **chỉ tồn tại nếu ghi lại TRƯỚC khi deploy** |
| Dữ liệu | snapshot/backup | chỉ khi release có migration |

Tầng giữa là chỗ hay mất nhất: sau deploy, revision cũ đã bị đẩy xuống và không còn cách nào biết chắc cái nào là ngay trước. Vì vậy nó **sinh ra một bước prep bắt buộc** — ghi lại revision hiện tại — chứ không phải một dòng trong mục rollback.

**2.5.4 — Baseline những thứ ĐÃ hỏng từ trước.** Chạy chính các thao tác smoke trên môi trường **trước khi deploy**. Thứ nào fail sẵn thì ghi vào `その他補足` là *pre-existing, ngoài phạm vi release này*, và loại khỏi bộ test case hoặc đánh dấu rõ.

Không có baseline thì lỗi cũ sẽ bị quy cho release: tester báo regression, mất thời gian điều tra một bug có sẵn, và có thể chặn cả sign-off. Đây cũng là cách duy nhất để test suite không chứa case fail sẵn.

> **Đặc điểm chung của 2.5.3 và 2.5.4**: chỉ đúng nếu thu thập **trước** khi deploy. Sau deploy thì revision cũ đã mất dấu, và không còn cách phân biệt "lỗi có sẵn" với "lỗi do release".

> Mục nào không tra được → ghi `[Giả định — cách verify: <lệnh/nơi xem>]`. Im lặng bỏ qua khiến người đọc tưởng đã kiểm.

## Bước 3 — Enrich từng item (tái dùng artifact, có fallback)

| Ticket đi qua toolkit (có `tasks/{ID}/`) | Ticket KHÔNG qua toolkit |
|---|---|
| 機能 ← Description trong `backlog.md` (đã viết hướng người dùng) | 機能 ← PR title/body, diễn đạt lại hướng người dùng |
| 問題 ← known issues / out-of-scope trong ticket | ← ghi chú trong PR nếu có |
| màn hình ảnh hưởng ← `impact.md` (dependency walk) | ← suy từ path trong diff |
| bug: sửa gì ← root cause trong `report-bug-*.md` | ← PR body |
| **nhãn** | ✅ có evidence | ⚠ **đánh dấu "suy từ PR"** |

Giữ tinh thần evidence-first: mục nào suy từ PR/diff thay vì artifact thì **ghi rõ**, đừng để lẫn với mục đã verify.

## Bước 4 — Auto-tick 影響箇所マトリックス (giá trị lớn nhất — người điền tay hay sót)

Quét path trong diff của cả release, tick từng cột:

| Cột matrix | Dấu hiệu path |
|---|---|
| Frontend | `*.vue`, `*.blade.php`, `*.jsx/tsx`, `resources/js`, `resources/css`, vite/webpack config |
| Backend | `src/**/{Application,Domain,Infrastructure,Presentation}`, `app/`, `routes/`, controller/service/repository |
| AWS Config | repo infra (CDK/Terraform), `ecs/`, `.github/workflows/`, task definition, Dockerfile |
| Email | Mail class, mail template/notification |
| SMS | tích hợp SMS |
| **Data Migration / Seeder** | `database/migrations/`, `database/seeders/` |
| Batch | `app/Console/Commands/`, scheduler, repo batch anh em |
| Cache | cache key/store, Redis/ElastiCache/Valkey config |

Adapter cho phép repo bổ sung/ghi đè pattern. Cột nào không có path khớp → để trống, **không đoán**.

## Bước 5 — Suy tín hiệu vận hành + nháp steps

Từ matrix + diff, suy ra **đánh giá deploy** rồi seed các bảng steps (khối prep / deployment / smoke / rollback). Đây là nháp cho người sửa, không phải chân lý:

| Tín hiệu phát hiện | Kéo theo |
|---|---|
| Có `database/migrations/` | prep: **backup DB**; deployment: chạy migrate; rollback: restore snapshot. **Cân nhắc maintenance mode** |
| KHÔNG có migration + không đổi schema | ghi rõ **không cần maintenance mode / không cần backup DB** |
| Dockerfile / base image đổi | deployment: rolling update + verify health check; rollback: trỏ tag image cũ rồi redeploy |
| Infra/CDK/workflow đổi | deployment: deploy infra trước; ghi chú điều phối thứ tự |
| Cache / ElastiCache config | prep: snapshot; rollback: restore từ snapshot |
| Batch | ghi chú ảnh hưởng lịch chạy; có cần dừng batch khi deploy không |
| Nhiều repo cùng release | **cảnh báo điều phối**: thứ tự deploy, và repo nào nên hoãn release trong thời gian soak |

**Phương thức deploy định hình bảng deployment steps** (hỏi ở Bước 6 — đừng giả định):

| Phương thức | Steps sinh ra |
|---|---|
| **CI/CD** (GitHub Actions…) | trigger workflow nào · theo dõi run · chờ service stable · verify health check |
| **AWS CLI / CDK** | `cdk diff` trước khi apply · `cdk deploy <stack>` · thứ tự stack nếu nhiều |
| **FTP** | upload path nào · backup file cũ trước · kiểm phân quyền sau upload |
| **Thao tác tay (Console)** | từng bước click + điểm verify sau mỗi bước |

Chưa biết phương thức → **KHÔNG tự viết steps**; để trống và ghi rõ đang chờ xác nhận.

**Môi trường (STG / PRODUCTION)** cũng đổi nội dung: PRODUCTION → siết chặt (backup, maintenance mode nếu có migration, rollback rõ ràng, cần approve); STG → nhẹ hơn, nhưng vẫn ghi rollback.

**Đánh giá downtime** — kết luận từ evidence, không nói chung chung: có migration không · deploy theo cơ chế gì (rolling? desiredCount? min/max healthy percent trong IaC) · có bước maintenance mode trong workflow không. Không tra được → `[Giả định — cách verify: …]`.

### Quy tắc viết `作業詳細 / Task Detail` (BẮT BUỘC — áp cho deployment / smoke / rollback steps)

Cột này **không được viết 1 câu chung chung**. Phải là **checklist đánh số các thao tác thực thi được**, người khác cầm là làm theo được mà không cần hỏi lại:

1. Mỗi dòng = **1 hành động cụ thể**: mở công cụ/màn hình nào → chọn resource **tên thật** → bấm gì / chạy lệnh gì.
2. **Dòng cuối luôn là điểm verify**: nhìn thấy gì thì coi là xong (trạng thái chuyển sang `available`, step xanh, giá trị trả về đúng, không có 5xx…).
3. Dùng **tên thật**: cluster/service/workflow/file/URL/lệnh. Không biết → để placeholder rõ ràng rồi hỏi, **không viết mơ hồ cho xong**.
4. **Song ngữ**: khối EN đánh số → `ーーーー` → khối JA đánh số **tương ứng 1-1** (cùng số dòng, cùng thứ tự).
5. Độ dài 2–5 dòng/step. Dài hơn → tách thành step riêng.

**Đạt chuẩn** ✅
```
1. Open the ElastiCache Console and select the cluster prodkaigoshoku-cachevalkey.
2. Choose Backup and create a manual snapshot.
3. Check the snapshot list and confirm the snapshot status becomes available.
ーーーー
1. ElastiCache Console を開き、prodkaigoshoku-cachevalkey クラスターを選択します。
2. Backup を実行し、手動スナップショットを作成します。
3. スナップショット一覧を確認し、ステータスが available になっていることを確認します。
```

**Không đạt** ❌ — `Verify the deployment` · `Check the service is working` · `Deploy to staging` (không nói mở gì, chọn gì, nhìn gì để biết xong).

### Smoke step đo metric — 5 bẫy, mỗi cái từng làm smoke test thành vô nghĩa

Áp khi smoke step đọc metric (5xx, error rate) sau deploy. Bốn cái đầu là **sai chỗ đo / sai cách đọc**, cái cuối là **sai thứ tự**:

1. **Service dùng chung load balancer → đo ở mức LB là sai.** Định tuyến theo path/host khiến metric mức LB gộp lỗi của service khác. Phải đo ở **nhóm backend của đúng service** (AWS: target group). Nhận biết bằng IaC: nhiều service khai cùng một LB với `path`/`host` khác nhau = dùng chung.
2. **Có HAI loại 5xx khác nghĩa, phải đo cả hai.** (a) **backend tự trả lỗi** — app fatal, DB không nối được (AWS: `HTTPCode_Target_5XX_Count`). (b) **LB tự sinh lỗi** vì không có backend khoẻ nào để chuyển tới — 502/503 (AWS: `HTTPCode_ELB_5XX_Count`). **Rollover thất bại hiện ở loại (b)** — chỉ đo loại (a) sẽ bỏ sót đúng sự cố mà smoke test sinh ra để bắt.
3. **Phép tổng hợp phải là `Sum`.** Dashboard thường mặc định `Average`, mà trung bình của một metric đếm thì vô nghĩa.
4. **Metric vắng mặt KHÔNG đủ để kết luận pass.** Nhiều hệ chỉ phát datapoint khi có lỗi, nên "no data" thường là tin tốt — **nhưng chỉ khi có traffic**. Bắt buộc đối chiếu số lượng request cùng khoảng thời gian:

   | Số request | 5xx | Kết luận |
   |---|---|---|
   | > 0 | không có metric | ✓ pass thật |
   | = 0 / không có | không có metric | ✘ **vô nghĩa** — chưa ai gọi vào |
   | > 0 | > 0 | ✘ có lỗi, phải điều tra |

5. **Step đo metric phải xếp SAU step sinh traffic.** Môi trường non-prod gần như không có traffic tự nhiên. Ghi ràng buộc thứ tự này vào chính `作業詳細` — đừng để người thực thi tự suy, họ sẽ làm theo số thứ tự.

**Nhãn trên dashboard ≠ tên metric.** Console thường hiển thị nhãn thân thiện (AWS: `Target 5XXs` / `ELB 5XXs`) chứ không phải tên thật (`HTTPCode_Target_5XX_Count`). Viết **cả hai** vào step, nếu không người thực thi tìm không ra rồi báo "không thấy metric".

## Bước 6 — Hỏi phần code không trả lời được (gộp 1 lượt)

**Ba câu BẮT BUỘC hỏi** (không được đoán — chúng đổi cả nội dung runbook):

1. **日時 (JST) / Date & Time** — thời điểm release theo giờ Nhật.
2. **環境 / Environment** — **STG hay PRODUCTION**. Quyết định URL, mức thận trọng, có cần backup/maintenance không.
3. **デプロイ方法 / Deploy method** — CI/CD (GitHub Actions…) · AWS CLI / CDK deploy · FTP · thao tác tay trên Console · khác. **Đây là thứ định hình toàn bộ bảng deployment steps** (xem Bước 5).

Hỏi thêm trong cùng lượt (nếu adapter chưa có): バージョン · URL môi trường · 担当者 PIC · ステータス · UAT (テクタス側 / 顧客様側) · known issues mang tính phán đoán · bước vận hành đặc thù (thao tác AWS Console…).

Hỏi **một lần duy nhất**, gộp tất cả — không hỏi nhỏ giọt.

## Content model (1 nguồn — 4 renderer dùng chung)

```
delivery      : datetime_jst · environment(STG|PRODUCTION) · deploy_method · version · env_url
known_issues  : [ no, detail, note ]
target        : number_of_changes
items         : [ no, function, ticket, note, known_issue,
                  matrix{ fe, be, aws, email, sms, migration, batch, cache },
                  uat{ result, techtus, client, note },
                  evidence: artifact | inferred-from-PR ]
steps         : prep[] · deployment[] · smoke[] · rollback[]
                  → mỗi bước [ no, name, detail, pic, status, note ]
```

## Bước 7 — Render (nội dung như nhau, layout khác nhau)

| Format | Layout | Cách |
|---|---|---|
| **md** | **Nguồn chân lý** — heading mỗi khối, matrix là bảng tick ✓, steps là bảng | viết trực tiếp; lưu `tasks/release-<yyyymmdd>.md` hoặc chỗ user chỉ định |
| **xlsx** | Đúng template công ty | **copy `TEMPLATE_XLSX` rồi ghi theo dòng** — KHÔNG dựng lại layout (template có merged cell) |
| **pdf** | Landscape (matrix rộng) hoặc tách matrix ra bảng riêng | `pandoc release.md -o release.pdf --pdf-engine=typst -V mainfont=... ` (JA → thêm font CJK) |
| **docx** | Dọc; matrix tách bảng riêng nếu tràn | `pandoc release.md -o release.docx` |

Mặc định xuất **md**; format khác chỉ khi user yêu cầu. Nhãn khối giữ song ngữ JA/EN như template.

## Guardrails

- **[HARD]** Không viết release note khi chưa chốt phạm vi (Bước 2). Sai phạm vi = sai toàn bộ.
- **[HARD]** Không viết `"từ X sang Y"` khi chưa đọc X **từ hệ thống** (Bước 2.5.1). Ghi chú, PR, ký ức đều không phải bằng chứng.
- **[HARD]** Release có deploy phải có bước prep **ghi lại revision đang chạy** (Bước 2.5.3) — thông tin này biến mất sau khi deploy.
- **[HARD]** Không kết luận "không có downtime" nếu chưa kiểm cơ chế deploy + migration thật. Chưa kiểm được → `[Giả định — cách verify]`.
- Mục suy từ PR/diff (không có artifact) phải **đánh dấu**, không trộn với mục đã verify.
- Không bịa bước vận hành (thao tác console, tên resource) — không biết thì để trống + hỏi.
- Cột matrix không có path khớp → để trống, không tick cho "đủ bảng".
- Không tự điền PIC / UAT / ステータス — đó là cam kết của người, không phải suy luận.
- Giữ nguyên chuỗi UI / tên resource gốc (tiếng Nhật, tên cluster…) ở mọi locale.
- **[HARD]** Smoke step đọc metric lỗi phải: đo ở **target group** (không phải load balancer) nếu service dùng chung LB · đo **cả** Target 5xx **và** ELB 5xx · statistic **Sum** · đối chiếu `RequestCount > 0` · xếp **sau** step sinh traffic. Thiếu bất kỳ điều nào thì step đó không chứng minh được gì — xem mục "Smoke step đo metric".

## Help

```
release-note <from-ref>..<to-ref> | "release lần này"  [format=md|xlsx|pdf|docx]
  Release note + deployment runbook cho MỘT LẦN RELEASE (N ticket). Output SONG NGỮ EN/JA.
  - Phạm vi: git log/PR range (BẮT BUỘC chốt trước).
  - Enrich từ tasks/{ID}/ (backlog.md, impact.md, report) — không có thì fallback PR/diff + đánh dấu.
  - Auto: 影響箇所マトリックス từ path diff + đánh giá downtime/điều phối + nháp steps.
  - Hỏi 1 lượt, BẮT BUỘC 3 câu: 日時 JST · 環境 (STG/PROD) · デプロイ方法 (CI/CD | CDK | FTP | tay).
    Kèm: version, PIC, UAT, ステータス.
  - Output: md (chuẩn) · xlsx (điền template công ty) · pdf/docx (pandoc).
  KHÔNG phải stage của pipeline per-task — gọi riêng lúc chuẩn bị deploy.
```
