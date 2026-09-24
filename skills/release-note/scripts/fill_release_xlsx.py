#!/usr/bin/env python3
"""Điền release note vào template xlsx của công ty (giữ nguyên merge / style / độ rộng cột).

    python3 fill_release_xlsx.py --data release.json --out "[Proj][PROD] Release notes.xlsx" \
        [--template /path/to/template.xlsx] [--sheet-title 20260930-TICKET]

Vào: JSON đúng content model của SKILL.md. Ra: bản sao template đã điền.
Script KHÔNG dựng lại layout — nó copy template rồi ghi theo dòng, vì template có
merged cell; dựng lại là mất định dạng công ty đã duyệt.

Neo theo CHỮ trong cột A (`DEPLOYMENT PREPARATION`, `ENGINEER DEPLOYMENT STEPS`,
`SMOKE TEST`, `ROLLBACK`), không hardcode số dòng — template đổi bố cục vẫn chạy.

JSON tối thiểu:
{
  "sheet_title": "20260930-MAG_UNEI-14532",
  "delivery": {"datetime_jst": "15:30 – 18:30 JST 2026/09/30",
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
from copy import copy
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


def shift_merges(ws, at_row, count):
    """openpyxl không tự dời merged cell khi insert_rows — dời tay.

    Không dùng unmerge_cells(): nó xoá thẳng trong ws._cells và ném KeyError khi
    ô đã bị insert_rows dịch đi. Cách chắc hơn: gỡ toàn bộ metadata merge, dọn
    các MergedCell mồ côi, rồi merge lại ở vị trí mới.
    """
    old = [(rng.min_row, rng.min_col, rng.max_row, rng.max_col) for rng in ws.merged_cells.ranges]
    ws.merged_cells.ranges = []
    for r0, c0, r1, c1 in old:  # MergedCell là read-only, phải dọn khỏi _cells
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if (r, c) != (r0, c0):
                    ws._cells.pop((r, c), None)
    for r0, c0, r1, c1 in old:
        shift = count if r0 >= at_row else 0
        ws.merge_cells(start_row=r0 + shift, start_column=c0,
                       end_row=r1 + shift, end_column=c1)


def fit_rows(ws, first, last, needed):
    """Khớp số dòng của khối với số bước: thiếu thì chèn, thừa thì xoá.

    Trả về độ lệch dòng (dương = đã chèn, âm = đã xoá) để khối bên dưới dời theo.
    Xoá dòng thừa là cần thiết: dòng rỗng vẫn mang viền của bảng, để lại thì
    bảng trông như còn kéo dài xuống dưới.
    """
    have = last - first + 1
    if needed == have:
        return 0

    if needed > have:
        extra = needed - have
        at = last + 1
        ws.insert_rows(at, extra)
        shift_merges(ws, at, extra)
        for r in range(at, at + extra):
            ws.row_dimensions[r].height = ws.row_dimensions[first].height
            for col in "ABCDEF":
                ws[f"{col}{r}"]._style = copy(ws[f"{col}{first}"]._style)
        return extra

    gone = have - needed
    at = first + needed
    ws.delete_rows(at, gone)
    shift_merges(ws, at, -gone)
    return -gone


def write_steps(ws, key, rows, first, last):
    if not rows:  # khối không có bước nào -> giữ nguyên, để người điền tay
        return 0
    shift = fit_rows(ws, first, last, len(rows))
    for i, step in enumerate(rows):
        r = first + i
        ws[f"A{r}"] = step.get("no", i + 1)
        for field, col in STEP_COLS.items():
            if field in step:
                ws[f"{col}{r}"] = step[field]
    return shift


def trim_trailing(ws):
    """Xoá các dòng cuối không có dữ liệu. Chúng vẫn mang viền nên trông như bảng còn tiếp."""
    last = max((c.row for row in ws.iter_rows() for c in row if c.value not in (None, "")), default=0)
    if last and ws.max_row > last:
        ws.delete_rows(last + 1, ws.max_row - last)


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

    title = args.sheet_title or data.get("sheet_title")
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
        ws["A4"] = (f"{'本番' if env.startswith('PROD') else env}環境の情報：\n"
                    f"{env} Environment Information:")

    # --- KNOWN ISSUES -----------------------------------------------------
    ki_header = find_row(ws, "KNOWN ISSUES AND LIMITATIONS")
    if ki_header:
        first = ki_header + 2  # tiêu đề khối + dòng tiêu đề cột
        for i, issue in enumerate(data.get("known_issues", [])):
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

    trim_trailing(ws)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.out)
    counts = " · ".join(f"{k}:{len(steps.get(k, []))}" for k, _ in SECTIONS)
    print(f"xong — {args.out}\nitems:{len(data.get('items', []))} · {counts}")


if __name__ == "__main__":
    main()
