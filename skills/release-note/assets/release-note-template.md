# リリースノート / RELEASE NOTES — {PROJECT} {ENV}

> Bản md này **mirror 1:1 các khối của template Excel** (`release-note-template.xlsx`): cùng tên khối, cùng cột, cùng thứ tự. Có gì thì điền nấy, không thêm mục Excel không có. Số dòng mỗi khối là số slot của Excel — vượt thì gom bước lại, không thêm dòng.
> Song ngữ: mỗi ô mô tả = khối EN → `ーーーー` → khối JA (đánh số 1-1). Giữ nguyên chuỗi UI / tên resource gốc.

---

## 1. デリバリー・DELIVERY

| 項目 / Item | 内容 / Value |
|---|---|
| 日時（日本時間）/ Date and Time (JST) | `HH:MM – HH:MM JST YYYY/MM/DD` |
| バーション / Version | `WEB: vX.Y.Z` — **hỏi người phụ trách, không suy từ git** |
| {ENV}環境の情報 / {ENV} Environment Information | `https://…/` |

---

## 2. 問題・ペンディングタスク・KNOWN ISSUES AND LIMITATIONS

<!-- Excel: 3 slot. HỎI người phụ trách có known issue không rồi mới điền — không tự rút từ md/PR. Không có thì ghi đúng 1 dòng: 現時点で確認されている問題はありません。/ No known issues at this time. -->

| NO. | 詳細 / DETAIL | 備考 / NOTE |
|---|---|---|
| 1 | EN<br>ーーーー<br>JA | |

---

## 3. リリースタゲット・RELEASE TARGET

| 完成したタスク数 / Number of changes | N |
|---|---|

---

## 4. リリースノート・RELEASE NOTES

| NO. | 機能 / MAIN FUNCTIONS | 内部バックログチケット / INTERNAL BACKLOG TICKET | 備考 / NOTE | 問題 / KNOWN ISSUES |
|---|---|---|---|---|
| 1 | JA<br>ーーーー<br>EN | `TICKET-ID チケット名` | | |

### 影響箇所マトリックス・AFFECTED Matrix

<!-- Tick ✓ theo path trong diff (Bước 4). Cột không có path khớp → để trống, không đoán. -->

| NO. | フロントエンド / Frontend | バックエンド / Backend | AWS設定 / AWS Config | メール / Email | SMS | データマイグレーション / シーダー / Data Migration / Seeder | バッチ / Batch | キャッシュ / Cache | 備考 / NOTE |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |

### UAT ステータス・UAT Status

<!-- Giá trị: Testing · OK · Re-open · Not Test. Không tự điền — đây là cam kết của người. -->

| NO. | テスト結果 / Test Result | テクタス側（テクタス側で実施必要な場合）/ TechTus (If TechTus Need to do) | 顧客様側（顧客様側で実施必要な場合）/ Client (If Client Need to do) | 備考 / NOTE |
|---|---|---|---|---|
| 1 | | | | |

---

## 5. DEPLOYMENT PREPARATION

<!-- Excel: 8 slot. ステータス: Open · In Progress · Done · No Need. 作業詳細 theo quy tắc checklist đánh số (SKILL.md Bước 5). -->

| NO. | 項目 / Name | 作業詳細 / Task Detail | 担当者 / PIC | ステータス / Status | 備考 / Note |
|---|---|---|---|---|---|
| 1 | EN<br>ーーーー<br>JA | 1. …<br>ーーーー<br>1. … | | Open | lệnh / URL |

---

## 6. ENGINEER DEPLOYMENT STEPS

<!-- Excel: 7 slot. -->

| NO. | 項目 / Name | 作業詳細 / Task Detail | 担当者 / PIC | ステータス / Status | 備考 / Note |
|---|---|---|---|---|---|
| 1 | | | | Open | |

---

## 7. エンジニアのスモークテストステップ・ENGINEER SMOKE TEST STEPS

<!-- Excel: 10 slot. Step đo metric phải xếp SAU step sinh traffic (SKILL.md "Smoke step đo metric"). -->

| NO. | 項目 / Name | 作業詳細 / Task Detail | 担当者 / PIC | ステータス / Status | 備考 / Note |
|---|---|---|---|---|---|
| 1 | | | | Open | |

---

## 8. エンジニアのロールバックステップ・ENGINEER ROLLBACK STEPS

<!-- Excel: 8 slot. Mỗi bước nêu hiện vật lùi về (artifact / revision / snapshot) và điểm verify. -->

| NO. | 項目 / Name | 作業詳細 / Task Detail | 担当者 / PIC | ステータス / Status | 備考 / Note |
|---|---|---|---|---|---|
| 1 | | | | Open | |
