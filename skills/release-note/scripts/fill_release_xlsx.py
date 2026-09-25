#!/usr/bin/env python3
"""Điền release note vào template xlsx của công ty (giữ nguyên merge / style / độ rộng cột).

    python3 fill_release_xlsx.py --data release.json --out "[Proj][PROD] Release notes.xlsx" \
        [--template /path/to/template.xlsx] [--sheet-title 20260930-TICKET]

Vào: JSON đúng content model của SKILL.md. Ra: bản sao template đã điền.
Script KHÔNG dựng lại layout và KHÔNG chèn/xoá dòng — nó copy template rồi ghi vào
đúng số slot có sẵn, vì template có merged cell, border và dropdown theo vùng cố định;
chèn/xoá dòng là lệch cả ba. Nội dung nhiều hơn slot → script báo, người gom lại.

Neo theo CHỮ trong cột A (`DEPLOYMENT PREPARATION`, `ENGINEER DEPLOYMENT STEPS`,
`SMOKE TEST`, `ROLLBACK`), không hardcode số dòng — template đổi bố cục vẫn chạy.

JSON tối thiểu:
{
  "sheet_title": "(tuỳ chọn — mặc định tự dựng: Ymd-デジ戦's PROD-x.y.z từ delivery)",
  "delivery": {"datetime_jst": "15:30 – 18:30 JST 2026-09-30",
               "version": "WEB: v1.0.0",
               "environment": "PRODUCTION",
               "env_url": "https://example.jp/"},
  "known_issues": [{"detail": "EN\nーーーー\nJA", "note": ""}],
  "target": {"number_of_changes": 1},
  "items": [{"function": "EN\nーーーー\nJA", "ticket": "TICKET-1 タイトル", "note": "",
             "known_issue": "", "matrix": {"aws": true}, "matrix_note": "",
             "test_result": "", "uat": {"techtus": "", "client": "", "note": ""}}],
  "steps": {"prep": [{"name": "EN\nーーーー\nJA", "detail": "1. …\nーーーー\n1. …",
                      "pic": "anhttq", "status": "Open", "note": "cmd"}],
            "deployment": [], "smoke": [], "rollback": []}
}

Khoá matrix: fe, be, aws, email, sms, migration, batch, cache.
"""
from __future__ import annotations

import argparse
import json
import sys
from copy import copy  # autofit_rows
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("thiếu openpyxl: pip3 install openpyxl")

DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "release-note-template.xlsx"

# nhãn cột A của từng khối steps -> khoá trong JSON
SECTIONS = [
    ("prep", ("DEPLOYMENT PREPARATION",)),
    ("deployment", ("ENGINEER DEPLOYMENT STEPS",)),
    ("smoke", ("SMOKE TEST",)),
    ("rollback", ("ROLLBACK",)),
]
MATRIX_COLS = {"fe": "G", "be": "H", "aws": "I", "email": "J", "sms": "K",
               "migration": "L", "batch": "M", "cache": "N"}
STEP_COLS = {"name": "B", "detail": "C", "pic": "D", "status": "E", "note": "F"}


SHEET_TEAM = "デジ戦"  # quy ước công ty: Ymd-デジ戦's STAGING-x.y.z / Ymd-デジ戦's PROD-x.y.z


def default_sheet_title(d):
    """Dựng tên sheet theo quy ước từ delivery: ngày (YYYY/MM/DD trong datetime_jst),
    môi trường (STG*/STAGING -> STAGING, còn lại -> PROD), version (bỏ tiền tố 'WEB: v').
    Ngày trong datetime_jst viết Y-m-d (vd '12:00 – 14:00 JST 2026-09-25')."""
    import re
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", d.get("datetime_jst", ""))
    env = (d.get("environment") or "").upper()
    ver = re.sub(r"^[A-Za-z]+:\s*v?", "", d.get("version", "")).strip()
    if not (m and env and ver):
        return None  # thiếu dữ kiện thì giữ tên sheet của template
    env_label = "STAGING" if env.startswith("ST") else "PROD"
    return f"{''.join(m.groups())}-{d.get('sheet_team', SHEET_TEAM)}'s {env_label}-{ver}"


def find_row(ws, *needles, start=1):
    """Dòng đầu tiên có cột A chứa một trong các chuỗi (không phân biệt hoa thường)."""
    for r in range(start, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if isinstance(v, str) and any(n.lower() in v.lower() for n in needles):
            return r
    return None


def section_bounds(ws):
    """[(key, first_data_row, last_usable_row)] — chặn dưới là tiêu đề khối kế tiếp."""
    titles = []
    for key, needles in SECTIONS:
        r = find_row(ws, *needles)
        if r is None:
            sys.exit(f"template thiếu khối '{needles[0]}'")
        titles.append((key, r))
    titles.sort(key=lambda t: t[1])

    out = []
    for i, (key, title_row) in enumerate(titles):
        nxt = ws.cell(row=title_row + 1, column=1).value
        # khối có dòng tiêu đề cột ("NO.") thì dữ liệu bắt đầu sau nó
        first = title_row + (2 if isinstance(nxt, str) and nxt.strip().upper().startswith("NO.") else 1)
        last = (titles[i + 1][1] - 1) if i + 1 < len(titles) else ws.max_row
        out.append((key, first, last))
    return out


def check_fits(key, needed, first, last):
    """Template là bố cục khách đã duyệt: KHÔNG chèn/xoá dòng (border, merge, dropdown
    sẽ lệch). Nội dung vượt số slot thì gom lại cho vừa, script chỉ báo."""
    have = last - first + 1
    if needed > have:
        sys.exit(f"khối '{key}' có {needed} mục nhưng template chỉ có {have} dòng "
                 f"(dòng {first}-{last}) — gom nội dung lại cho vừa, không chèn dòng")


def write_steps(ws, key, rows, first, last):
    if not rows:  # khối không có bước nào -> giữ nguyên, để người điền tay
        return 0
    check_fits(key, len(rows), first, last)
    shift = 0
    for i, step in enumerate(rows):
        r = first + i
        ws[f"A{r}"] = step.get("no", i + 1)
        for field, col in STEP_COLS.items():
            if field in step:
                ws[f"{col}{r}"] = step[field]
    return shift


LINE_PT = 15  # chiều cao ước lượng của một dòng chữ (pt)
MAX_ROW_PT = 409  # giới hạn của Excel


def autofit_rows(ws, rows):
    """Bật wrap và ước lượng chiều cao theo số dòng chữ. Template khoá customHeight
    nên Excel không tự giãn; không làm bước này thì ô dài bị cắt."""
    import math
    from openpyxl.styles import Alignment
    widths = {}
    for rng in ws.merged_cells.ranges:  # ô merge dùng tổng độ rộng các cột gộp
        widths[(rng.min_row, rng.min_col)] = sum(
            ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width or 8
            for c in range(rng.min_col, rng.max_col + 1))
    for r in rows:
        lines = 1
        for c in ws[r]:
            if c.column == 1 or c.value in (None, "") or not isinstance(c.value, str):
                continue  # cột A là nhãn/số thứ tự, chữ tràn sang phải — không wrap
            al = copy(c.alignment); al.wrap_text = True; al.vertical = al.vertical or "top"
            c.alignment = al
            w = widths.get((r, c.column)) or ws.column_dimensions[c.column_letter].width or 8
            n = 0
            for line in c.value.split("\n"):
                units = sum(1.8 if ord(ch) > 0x2E7F else 1 for ch in line)  # CJK rộng gần gấp đôi
                n += max(1, math.ceil(units / max(w - 1, 1)))
            lines = max(lines, n)
        ws.row_dimensions[r].height = min(MAX_ROW_PT, max(ws.row_dimensions[r].height or 0, lines * LINE_PT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="JSON content model")
    ap.add_argument("--out", required=True, help="file xlsx xuất ra")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--sheet-title", default=None)
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    wb = openpyxl.load_workbook(args.template)
    ws = wb.active

    title = args.sheet_title or data.get("sheet_title") or default_sheet_title(data.get("delivery", {}))
    if title:
        ws.title = title[:31]

    # --- DELIVERY ---------------------------------------------------------
    d = data.get("delivery", {})
    if d.get("datetime_jst"):
        ws["C2"] = d["datetime_jst"]
    if d.get("version"):
        ws["C3"] = d["version"]
    if d.get("env_url"):
        ws["C4"] = d["env_url"]
    env = (d.get("environment") or "").upper()
    if env:
        ws["A4"] = (f"{env}環境の情報：\n"
                    f"{env} Environment Information:")

    # --- KNOWN ISSUES -----------------------------------------------------
    ki_header = find_row(ws, "KNOWN ISSUES AND LIMITATIONS")
    issues = data.get("known_issues", [])
    if ki_header and issues:
        first = ki_header + 2  # tiêu đề khối + dòng tiêu đề cột
        last = find_row(ws, "RELEASE TARGET", start=first) - 1
        check_fits("known_issues", len(issues), first, last)
        for i, issue in enumerate(issues):
            r = first + i
            ws[f"A{r}"] = issue.get("no", i + 1)
            ws[f"B{r}"] = issue.get("detail", "")
            ws[f"F{r}"] = issue.get("note", "")

    # --- RELEASE TARGET / NOTES ------------------------------------------
    if "target" in data and data["target"].get("number_of_changes") is not None:
        tr = find_row(ws, "完成したタスク数", "Number of changes")
        if tr:
            ws[f"C{tr}"] = data["target"]["number_of_changes"]

    rn = find_row(ws, "リリースノート", "RELEASE NOTES")
    if rn:
        first = rn + 2  # dòng tiêu đề cột nằm ngay dưới
        for i, item in enumerate(data.get("items", [])):
            r = first + i
            ws[f"A{r}"] = item.get("no", i + 1)
            ws[f"B{r}"] = item.get("function", "")
            ws[f"C{r}"] = item.get("ticket", "")
            ws[f"D{r}"] = item.get("note", "")
            ws[f"E{r}"] = item.get("known_issue", "")
            for k, col in MATRIX_COLS.items():
                if item.get("matrix", {}).get(k):
                    ws[f"{col}{r}"] = "✓"
            ws[f"O{r}"] = item.get("matrix_note", "")
            ws[f"P{r}"] = item.get("test_result", "")
            uat = item.get("uat", {})
            ws[f"Q{r}"] = uat.get("techtus", "")
            ws[f"R{r}"] = uat.get("client", "")
            ws[f"S{r}"] = uat.get("note", "")

    # --- STEPS ------------------------------------------------------------
    steps = data.get("steps", {})
    shift = 0
    for key, first, last in section_bounds(ws):
        first += shift
        last += shift
        shift += write_steps(ws, key, steps.get(key, []), first, last)

    # bỏ qua dòng tiêu đề khối (chỉ có cột A, chữ tràn sang phải) và dòng tiêu đề cột "NO."
    def is_data_row(r):
        a = ws.cell(r, 1).value
        if isinstance(a, str) and a.strip().upper() == "NO.":
            return False
        return any(ws.cell(r, c).value not in (None, "") for c in range(2, ws.max_column + 1))
    autofit_rows(ws, [r for r in range(1, ws.max_row + 1) if is_data_row(r)])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.out)
    counts = " · ".join(f"{k}:{len(steps.get(k, []))}" for k, _ in SECTIONS)
    print(f"xong — {args.out}\nitems:{len(data.get('items', []))} · {counts}")


if __name__ == "__main__":
    main()
