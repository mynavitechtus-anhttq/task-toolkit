#!/usr/bin/env bash
# task-toolkit — cài đặt cho Claude Code / Codex / Cursor
#
#   bash install.sh              chọn agent qua menu
#   bash install.sh --codex      cài thẳng cho Codex
#   bash install.sh --cursor     cài rule cho Cursor (thư mục hiện tại)
#   bash install.sh --claude     in lệnh cài cho Claude Code
#   bash install.sh --verify     chỉ kiểm tra bản đã cài
#   bash install.sh --uninstall  gỡ những gì script này đã tạo
#
# Chỉ tạo symlink và file rule. Không sửa gì trong package.

set -uo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$ROOT/skills"
CODEX_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
MANIFEST="$CODEX_DIR/.task-toolkit-installed"

# Tên lệnh trong Codex = tên symlink. Đặt cùng dạng với Claude Code (task-toolkit:<skill>)
# để gõ ở đâu cũng như nhau. Đổi PREFIX/SEP nếu Codex của bạn không nhận dấu ':'.
PREFIX="${TASK_TOOLKIT_PREFIX:-task-toolkit}"
SEP="${TASK_TOOLKIT_SEP:-:}"

SKILLS_LIST=(report task-init task-survey analyze-spec debug planning backlog-ticket release-note)

# _shared KHÔNG được đặt tiền tố. Mọi SKILL.md trỏ tới nó bằng '../_shared/...',
# tức là ngang cấp trong ~/.codex/skills/ — đổi tên là gãy hết.
SHARED_NAME="_shared"

link_name_for() { printf '%s%s%s' "$PREFIX" "$SEP" "$1"; }

# tên cũ từ các bản trước, dùng để dọn khi cài lại
LEGACY_NAMES=(report task-init-generic task-survey-generic analyze-spec-toolkit debug planning backlog-ticket release-note)

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  B=$'\033[1m'; G=$'\033[32m'; Y=$'\033[33m'; R=$'\033[31m'; D=$'\033[2m'; N=$'\033[0m'
else
  B=""; G=""; Y=""; R=""; D=""; N=""
fi
ok()   { printf "  %s✅%s %s\n" "$G" "$N" "$1"; }
warn() { printf "  %s⚠%s  %s\n" "$Y" "$N" "$1"; }
err()  { printf "  %s✖%s  %s\n" "$R" "$N" "$1"; }
info() { printf "  %s\n" "$1"; }
head2(){ printf "\n%s%s%s\n" "$B" "$1" "$N"; }

ask() {   # ask "câu hỏi" "mặc-định"  → stdout
  local q="$1" def="${2:-}" a
  if [ -n "$def" ]; then read -rp "  $q [$def]: " a; else read -rp "  $q: " a; fi
  printf '%s' "${a:-$def}"
}

# ─────────────────────────────────────────────────────────── sanity

precheck() {
  local bad=0
  [ -d "$SKILLS" ] || { err "không thấy $SKILLS — chạy script từ trong package"; bad=1; }
  [ -d "$SKILLS/_shared" ] || { err "thiếu skills/_shared — package không đầy đủ"; bad=1; }
  for s in "${SKILLS_LIST[@]}"; do
    [ -d "$SKILLS/$s" ] || { err "thiếu skills/$s"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo; err "package không hợp lệ, dừng."; exit 1; }
}

# ─────────────────────────────────────────────────────────── dọn tên cũ

cleanup_legacy() {
  local found=()
  for old in "${LEGACY_NAMES[@]}"; do
    local link="$CODEX_DIR/$old"
    [ -L "$link" ] || continue
    [[ "$(readlink "$link")" == "$SKILLS"/* ]] || continue   # chỉ đụng symlink của package này
    found+=("$old")
  done
  [ "${#found[@]}" -gt 0 ] || return 0

  warn "Tìm thấy ${#found[@]} lối tắt theo tên cũ của package này:"
  printf '        %s\n' "${found[@]}"
  info "      Bản mới dùng tên thống nhất ${B}${PREFIX}${SEP}<skill>${N} cho khớp Claude Code."
  local c; c="$(ask "  Gỡ tên cũ? [Y/n]" "Y")"
  case "$c" in
    n|N) info "      giữ lại — sẽ có hai bộ tên song song" ;;
    *)   for old in "${found[@]}"; do rm -f "$CODEX_DIR/$old" && ok "gỡ $old"; done ;;
  esac
  echo
}

# ─────────────────────────────────────────────────────────── Codex

install_codex() {
  head2 "Codex — symlink vào $CODEX_DIR"
  mkdir -p "$CODEX_DIR" || { err "không tạo được $CODEX_DIR"; return 1; }

  cleanup_legacy

  local created=() skipped=0
  for src_name in "${SKILLS_LIST[@]}" "$SHARED_NAME"; do
    local link_name
    if [ "$src_name" = "$SHARED_NAME" ]; then link_name="$SHARED_NAME"; else link_name="$(link_name_for "$src_name")"; fi
    local src="$SKILLS/$src_name" link="$CODEX_DIR/$link_name"

    if [ -L "$link" ]; then
      local cur; cur="$(readlink "$link")"
      if [ "$cur" = "$src" ]; then
        ok "$link_name — đã trỏ đúng, bỏ qua"; created+=("$link_name"); continue
      fi
      warn "$link_name đang trỏ tới:"
      info "      ${D}$cur${N}"
      local c; c="$(ask "  [o] ghi đè · [r] đổi tên thành ${link_name}-2 · [s] bỏ qua" "r")"
      case "$c" in
        o|O) ln -sfn "$src" "$link"; ok "$link_name — đã ghi đè"; created+=("$link_name") ;;
        s|S) skipped=$((skipped+1)); info "      bỏ qua $link_name" ;;
        *)   link_name="${link_name}-2"; link="$CODEX_DIR/$link_name"
             ln -sfn "$src" "$link"; ok "$link_name — tạo tên mới"; created+=("$link_name") ;;
      esac
      continue
    fi

    if [ -e "$link" ]; then
      err "$link_name đã tồn tại và KHÔNG phải symlink — không đụng vào"
      info "      ${D}$link${N}"
      skipped=$((skipped+1)); continue
    fi

    ln -sfn "$src" "$link" && { ok "$link_name"; created+=("$link_name"); } || err "$link_name — tạo symlink thất bại"
  done

  printf '%s\n' "${created[@]}" > "$MANIFEST" 2>/dev/null
  echo
  if [ "$skipped" -gt 0 ]; then
    info "Đã tạo/xác nhận ${#created[@]} symlink, bỏ qua $skipped."
    warn "Có mục bị bỏ qua — chạy lại nếu muốn xử lý."
  else
    info "Đã tạo/xác nhận ${#created[@]} symlink."
  fi

  # _shared là bắt buộc: mọi SKILL.md trỏ tới nó bằng ../_shared/...
  if [ ! -e "$CODEX_DIR/_shared" ]; then
    echo
    err "THIẾU _shared — các skill trỏ '../_shared/...' sẽ không resolve được."
    info "     Đây là lỗi hay gặp nhất khi cài tay. Tạo bằng:"
    info "     ${D}ln -sfn \"$SKILLS/_shared\" \"$CODEX_DIR/_shared\"${N}"
  fi
}

# ─────────────────────────────────────────────────────────── Cursor

install_cursor() {
  head2 "Cursor — ghi file hướng dẫn trỏ về package"
  local scope target
  scope="$(ask "Cài cho [p] project hiện tại hay [g] global (~/.cursor)" "p")"
  case "$scope" in g|G) target="$HOME/.cursor/rules" ;; *) target="$PWD/.cursor/rules" ;; esac
  mkdir -p "$target" || { err "không tạo được $target"; return 1; }

  local f="$target/task-toolkit.mdc"
  if [ -e "$f" ]; then
    local c; c="$(ask "$f đã tồn tại — ghi đè? [y/N]" "N")"
    case "$c" in y|Y) ;; *) info "bỏ qua"; return 0 ;; esac
  fi

  cat > "$f" <<RULE
---
description: Khi user yêu cầu viết report / báo cáo bug / điều tra issue ("viết report", "báo cáo bug", "root cause", "/task-toolkit:report"), đọc và làm theo $SKILLS/report/SKILL.md (kèm templates.md, checklists.md, rca-method.md, discovery-method.md cùng thư mục; discovery-method trỏ tiếp tới ../_shared/code-evidence-method.md cho kỹ thuật đào code).
alwaysApply: false
---
RULE
  ok "đã ghi $f"
}

# ─────────────────────────────────────────────────────────── Claude Code

install_claude() {
  head2 "Claude Code"
  info "Claude cài qua marketplace, script không chạy hộ được vì cần biết nguồn."
  info "Package đã có sẵn ${B}.claude-plugin/marketplace.json${N} nên repo này tự làm marketplace."
  echo
  info "  ${D}# từ thư mục local${N}"
  info "  claude plugin marketplace add $ROOT"
  info "  claude plugin install task-toolkit@task-toolkit"
  echo
  info "  ${D}# hoặc từ git remote sau khi push${N}"
  info "  claude plugin marketplace add <git-url>"
  info "  claude plugin install task-toolkit@task-toolkit"
  echo
  warn "Sau khi sửa nội dung package: bump version trong .claude-plugin/plugin.json,"
  info "     chạy 'claude plugin update task-toolkit', rồi mở session mới."
}

# ─────────────────────────────────────────────────────────── verify

verify() {
  head2 "Kiểm tra"
  local bad=0

  # 1. symlink Codex resolve được không
  if [ -d "$CODEX_DIR" ]; then
    local n=0
    for src_name in "${SKILLS_LIST[@]}" "$SHARED_NAME"; do
      local link_name
      if [ "$src_name" = "$SHARED_NAME" ]; then link_name="$SHARED_NAME"; else link_name="$(link_name_for "$src_name")"; fi
      for cand in "$CODEX_DIR/$link_name" "$CODEX_DIR/${link_name}-2"; do
        [ -L "$cand" ] || continue
        n=$((n+1))
        if [ -e "$cand" ]; then :; else
          err "symlink gãy: $(basename "$cand") → $(readlink "$cand")"; bad=1
        fi
      done
    done
    [ "$bad" = 0 ] && ok "Codex: $n symlink, tất cả resolve được"
    if [ ! -e "$CODEX_DIR/_shared" ]; then
      err "Codex: THIẾU _shared — tham chiếu '../_shared/...' sẽ gãy"; bad=1
    fi
  else
    info "Codex: chưa cài (không có $CODEX_DIR)"
  fi

  # 2. mọi tham chiếu ../_shared/... trong package có trỏ tới file thật không
  local miss=0 total=0
  while IFS= read -r f; do
    while IFS= read -r ref; do
      total=$((total+1))
      local resolved; resolved="$(cd "$(dirname "$f")" && cd "$(dirname "$ref")" 2>/dev/null && pwd)/$(basename "$ref")"
      [ -f "$resolved" ] || { err "tham chiếu gãy trong $(basename "$(dirname "$f")")/$(basename "$f"): $ref"; miss=$((miss+1)); bad=1; }
    done < <(grep -ohE '\.\./_shared/[A-Za-z0-9._/-]+\.md' "$f" 2>/dev/null | sort -u)
  done < <(find "$SKILLS" -name "*.md" -type f)
  [ "$miss" = 0 ] && ok "Nội bộ package: $total tham chiếu ../_shared/ đều hợp lệ"

  # 3. frontmatter từng skill
  local nodesc=0
  for s in "${SKILLS_LIST[@]}"; do
    local f="$SKILLS/$s/SKILL.md"
    [ -f "$f" ] || { err "thiếu $s/SKILL.md"; bad=1; continue; }
    head -1 "$f" | grep -q '^---$' || { err "$s/SKILL.md không mở đầu bằng ---"; bad=1; }
    grep -q '^name:' "$f"        || { err "$s/SKILL.md thiếu 'name:'"; bad=1; }
    grep -q '^description:' "$f" || { err "$s/SKILL.md thiếu 'description:'"; nodesc=$((nodesc+1)); bad=1; }
  done
  [ "$nodesc" = 0 ] && ok "Frontmatter: 8 skill đều có name + description"

  echo
  [ "$bad" = 0 ] && printf "  %s✅ Không phát hiện vấn đề.%s\n" "$G" "$N" \
                 || printf "  %s✖ Có vấn đề ở trên — xem lại trước khi dùng.%s\n" "$R" "$N"
  return "$bad"
}

# ─────────────────────────────────────────────────────────── uninstall

uninstall() {
  head2 "Gỡ cài đặt"
  if [ ! -f "$MANIFEST" ]; then
    warn "Không có $MANIFEST — script chỉ gỡ được thứ chính nó tạo."
    info "     Gỡ tay: xoá các symlink trong $CODEX_DIR trỏ về $SKILLS"
    return 0
  fi
  local n=0
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    local link="$CODEX_DIR/$name"
    if [ -L "$link" ] && [[ "$(readlink "$link")" == "$SKILLS"/* ]]; then
      rm -f "$link" && { ok "đã gỡ $name"; n=$((n+1)); }
    else
      warn "$name — không phải symlink của package, giữ nguyên"
    fi
  done < "$MANIFEST"
  rm -f "$MANIFEST"
  echo; info "Đã gỡ $n symlink."
  info "Rule Cursor và plugin Claude Code phải gỡ riêng:"
  info "  ${D}rm .cursor/rules/task-toolkit.mdc${N}"
  info "  ${D}claude plugin uninstall task-toolkit${N}"
}

# ─────────────────────────────────────────────────────────── main

menu() {
  head2 "task-toolkit — cài đặt"
  info "Package: ${D}$ROOT${N}"
  echo
  info "  ${B}1) Claude Code${N}   ${D}(mặc định)${N}"
  info "     Claude cài plugin bằng lệnh riêng của nó, script không chạy hộ được."
  info "     Script chỉ IN RA hai lệnh, đã điền sẵn đường dẫn đúng, để bạn dán vào."
  info "     ${D}Cài xong dùng được đủ, kể cả agent thẩm định chạy trong context riêng.${N}"
  echo
  info "  ${B}2) Codex CLI${N}"
  info "     Tạo lối tắt trong ~/.codex/skills/ trỏ ngược về package này."
  info "     Xong là gõ /task-toolkit:report trong Codex chạy được ngay."
  info "     ${D}Hạn chế: Codex không có hệ agent riêng, nên bước thẩm định report${N}"
  info "     ${D}chạy như một lượt tự soát thay vì một agent độc lập.${N}"
  echo
  info "  ${B}3) Cursor${N}"
  info "     Cursor không có hệ skill. Script ghi một file hướng dẫn"
  info "     (.cursor/rules/task-toolkit.mdc) chỉ cho Cursor biết:"
  info "     \"khi user đòi viết report thì đọc SKILL.md ở đường dẫn này\"."
  info "     ${D}Chỉ trỏ đường, không copy nội dung — sửa package là Cursor ăn ngay.${N}"
  echo
  info "  ${B}4) Codex + Cursor${N}   — làm cả 2 và 3"
  info "  ${B}5) Kiểm tra${N}         — soát bản đã cài, không thay đổi gì"
  echo
  local c; c="$(ask "Chọn" "1")"
  case "$c" in
    1) install_claude ;;
    2) install_codex; verify ;;
    3) install_cursor ;;
    4) install_codex; install_cursor; verify ;;
    5) verify ;;
    *) err "lựa chọn không hợp lệ"; exit 1 ;;
  esac
}

precheck
case "${1:-}" in
  --codex)     install_codex; verify ;;
  --cursor)    install_cursor ;;
  --claude)    install_claude ;;
  --verify)    verify ;;
  --uninstall) uninstall ;;
  -h|--help)   sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  "")          menu ;;
  *)           err "tham số không nhận: $1 — dùng --help"; exit 1 ;;
esac
