# Discovery Method — reverse-engineer hệ thống

Phương pháp điều tra hệ thống **mình chưa nắm kiến trúc** (lạ/legacy/multi-repo) dùng cho STAGE 3 của `/task-toolkit:report` — hiểu đúng hệ thống trước, kết luận sau. Khác `task-survey`: task-survey giả định đã hiểu repo và chỉ khảo path quanh 1 task; discovery bắt đầu từ chỗ **chưa** có bản đồ, phải dựng project context + kiến trúc trước.

> **Kỹ thuật đào code** (evidence-first, chứng-minh-đừng-khẳng-định, từ vựng grep, đọc consumer-side, đối chiếu khai báo trùng lặp, uncertainty markers, multi-repo): xem [`../_shared/code-evidence-method.md`](../_shared/code-evidence-method.md). File này chỉ giữ phần **đặc thù discovery**: project context, chọn hướng đào, quy trình xác nhận từng phần, output vào report.

## Vai trò: Technical Archaeologist

- **Đọc code, suy luận kiến trúc** — phát hiện patterns, relationships từ source.
- **KHÔNG tự khẳng định** — mọi phát hiện từ code là *suy luận* cho đến khi user/Tech Lead xác nhận.
- Nguyên tắc riêng của discovery (bổ sung cho 4 nguyên tắc lõi ở file chung): **Uncertainty-first** (đánh dấu độ tin cậy từng phát hiện) · **Incremental verification** (xác nhận từng phần nhỏ, không đợi hoàn chỉnh).

## Step 0 — Project Context (BẮT BUỘC, không tự giả định)

Thu thập trước khi phân tích (từ CLAUDE.md/memory nếu có, thiếu thì hỏi user 1 lượt):

1. Hệ thống làm gì, tồn tại bao lâu, tech stack chính?
2. **Project Model**: A. Standalone · B. Ecosystem (nhiều sub-project liên kết — hỏi thêm: sub nào chia sẻ DB/API/auth? cái nào là core?) · C. Multi-tenant.
3. **Danh sách TẤT CẢ repo liên quan** + repo nào là chính. Nhận diện pattern tổ chức:

| Pattern | Ví dụ | Cách xử lý |
|---|---|---|
| Clean multi-repo | mỗi sub = 1 repo | map 1:1 |
| Clean monorepo | `/apps/a`, `/libs/shared` | phân tích folder boundaries (tìm workspace config: workspaces/nx/turbo/lerna/pnpm) |
| **Hybrid** | BE tách repo, FE nhiều app gộp 1 repo | ⚠ PHẢI lập **Repo-to-SubProject Mapping Table** (repo \| loại \| sub-projects bên trong \| cách phân chia); scope đọc đúng folder, KHÔNG trộn findings giữa các app |
| Shared/cross-cutting repo | `shared-libs`, `common-utils` | ghi là shared, map consumers |

4. Tài liệu hiện có ở đâu (wiki/md/Confluence/notes) — cái nào có thể `[OUTDATED?]`.

## Chọn hướng đào theo câu hỏi điều tra (5 loại)

| Câu hỏi report thuộc loại | Hướng đào | Nguồn chính |
|---|---|---|
| Kiến trúc/service/deploy ("cái gì nói chuyện với cái gì") | **Architecture** | entrypoints, infra config, docker/CI, service boundaries |
| Data ("dữ liệu này từ đâu, đi đâu, format gì") | **Database** | schema/migrations, models, producer & consumer code |
| Contract ("API này nhận/trả gì, auth thế nào") | **API** | routes, controllers, middleware, error handling |
| Tổ chức code ("logic X nằm đâu, test thế nào") | **Codebase** | folder structure, conventions, test setup |
| Nghiệp vụ ("flow Y chạy thế nào, rule gì") | **Feature** | use-case code path, business rules, sequence flow |

## Quy trình 6 bước (mỗi lần đào)

```
1. Information Source Catalog  → liệt kê nguồn cần: 🔴 REQUIRED / 🟡 RECOMMENDED / 🟢 OPTIONAL
                                  (REQUIRED phải có hoặc user xác nhận NOT AVAILABLE mới đi tiếp)
2. Phân tích tự động           → Glob/Grep/Read theo catalog; mỗi phát hiện kèm marker
3. Trình bày phát hiện         → format: Nguồn + Mức tin cậy 🟢/🟡/🔴 + câu hỏi xác nhận
4. Xác nhận với user/Tech Lead → hỏi TỪNG PHẦN, không dồn; cập nhật marker theo feedback
5. Soạn (đổ vào report)        → chỉ dùng phần đã xác nhận hoặc còn marker rõ ràng
6. Review                      → user soát, lặp đến khi OK
```

## Trace đặc thù discovery

- **Entrypoints trước**: routes / cron / queue / CLI — hệ thống bị kích hoạt từ đâu, rồi mới lần call chain xuống data store. (Từ vựng grep, đọc consumer-side, cross-check 2 đầu ranh giới, config runtime `[MISSING-SOURCE]`, Repo Map → xem file chung.)
- Ghi communication pattern (REST/queue/shared DB) tại **mỗi integration point** — đây là thứ report cần vẽ thành flow, không chỉ liệt kê file.

## Output đổ vào report

- `Căn cứ (evidence)`: phát hiện `[CONFIRMED]` → ✅; còn lại → ⚠ kèm cách verify.
- Sơ đồ flow (chữ hoặc mermaid) + Repo Map → `🔧 Technical Detail`.
- Bảng suy luận chờ xác nhận (`suy luận | căn cứ | độ tin`) → trình user TRƯỚC khi viết kết luận.
- Nguồn tra cứu → `Refs`.

> **Điều tra dài nhiều phiên** → lập `discovery-tracker.md` trong workspace làm single source of truth giữa các phiên. 7 phần: Project Context · Discovery Progress · Findings Summary · Sources Status · Open Questions · Output Files · Session Log. Đọc đầu phiên để biết đang ở đâu; cập nhật sau mỗi bước; thêm Session Log khi kết thúc phiên.

> **Tài liệu vượt 300 dòng** → tách file: file chính giữ overview + bảng tổng hợp + **bảng link** sang các file chi tiết; file chi tiết có link ngược về file chính. Điều tra multi-repo rất dễ sinh file khổng lồ không ai đọc.
