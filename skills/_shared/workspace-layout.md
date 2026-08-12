# Workspace layout — nguồn duy nhất

> **Mọi skill trỏ vào file này, không chép lại đường dẫn.** Đổi layout → sửa đúng một chỗ.
> Skill nào ghi file mà không khớp bảng dưới là lỗi — `scripts/selftest.mjs` bắt được.

## Cây thư mục

```
tasks/{TICKET-ID}/
├── README.md                    cổng vào: task là gì · đang ở stage nào · đọc gì trước
├── notes.md                     nhật ký chạy suốt task
│
├── 01-discovery/                HIỂU
│   ├── README.md
│   ├── current-state.md
│   ├── impact.md
│   ├── spec-analysis.md
│   ├── technical-approach.md
│   ├── security.md
│   ├── performance.md
│   └── diagnosis-<yyyymmdd>.md          (task BUG)
│
├── 02-plan/                     CHIA
│   ├── README.md
│   ├── plan.md
│   └── wbs-schedule.md
│
├── 03-backlog/                  GIAO VIỆC
│   ├── README.md                        index gom theo hạng mục WBS
│   └── ticket-NN-slug.md
│
├── 04-quality/                  KIỂM
│   ├── README.md
│   ├── test-checklist.md
│   ├── ut-design.md
│   ├── testcases/
│   └── test-report.md
│
└── 05-delivery/                 GIAO RA NGOÀI
    ├── README.md
    ├── report-<type>-<yyyymmdd>.md
    ├── release-note.md
    ├── security-checklist-<yyyymmdd>.md (AUDIT mode)
    └── evidence/
```

## Skill nào ghi vào đâu

| Skill | Ghi ra |
|---|---|
| `task-init` | `README.md` · `notes.md` · khung thư mục + README từng stage + file placeholder |
| `task-survey` | `01-discovery/current-state.md` · `01-discovery/impact.md` |
| `analyze-spec` | `01-discovery/spec-analysis.md` · `01-discovery/technical-approach.md` |
| `security-check` (task) | `01-discovery/security.md` |
| `security-check` (audit) | `05-delivery/security-checklist-<yyyymmdd>.md` |
| `perf-check` | `01-discovery/performance.md` |
| `debug` | `01-discovery/diagnosis-<yyyymmdd>.md` |
| `planning` | `02-plan/plan.md` · `02-plan/wbs-schedule.md` |
| `backlog-ticket` | `03-backlog/ticket-NN-slug.md` · `03-backlog/README.md` · cập nhật `04-quality/test-checklist.md` |
| `ut-design` | `04-quality/ut-design.md` |
| `report` | `05-delivery/report-<type>-<yyyymmdd>.md` · ảnh/log vào `05-delivery/evidence/` |
| `release-note` | `05-delivery/release-note.md` (tầng task) · `tasks/release-<yyyymmdd>.md` (tầng release) |

## Ba luật

1. **Tạo sẵn đủ thư mục và file placeholder**, kể cả phần chưa làm — placeholder ghi rõ *skill nào sẽ điền*. Người mở workspace phải thấy hình dạng đầy đủ của công việc ngay. Thư mục rỗng **kèm README** là chỗ đã dành sẵn; thư mục rỗng **không README** mới là rác.
2. **Mỗi thư mục stage có `README.md` riêng** — chứa gì · ai ghi · đọc theo thứ tự nào. Không quá một màn hình.
3. **Không ghi đè file đã có.** Chạy lại skill trên workspace cũ phải an toàn.

## Dòng chảy giữa các stage

```
01-discovery ──► 02-plan ──► 03-backlog ──┬─► 04-quality  (impact → lưới kiểm)
     │              │            │        └─► 05-delivery (report cite evidence 01)
     └──────────────┴────────────┴──► không stage nào điều tra lại từ đầu
```

Ràng buộc chéo cần giữ:

- `02-plan` Σ est **phải khớp** giữa `plan.md` và `wbs-schedule.md`; lệch thì ghi mục lệch số liệu.
- `01-discovery/impact.md` mỗi dòng **phải trỏ được** sang một lưới ở `04-quality/`.
- `01-discovery/security.md` mỗi dòng `⚠ Cần làm` **phải thành checkbox** trong ticket ở `03-backlog/`.
- `05-delivery/report-*.md` mọi claim **phải cite** file trong `01-discovery/`.
