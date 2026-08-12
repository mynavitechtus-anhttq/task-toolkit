#!/usr/bin/env node
/**
 * selftest — kiểm tính nhất quán nội bộ của plugin task-toolkit.
 * KHÔNG kiểm code dự án. Chạy: node scripts/selftest.mjs [--verbose]
 */
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const VERBOSE = process.argv.includes('--verbose');
const pass = [];
const fail = [];
const ok = (m) => pass.push(m);
const no = (m) => fail.push(m);

const read = (p) => readFileSync(join(ROOT, p), 'utf8');
const dirs = (p) =>
  existsSync(join(ROOT, p))
    ? readdirSync(join(ROOT, p)).filter((d) => statSync(join(ROOT, p, d)).isDirectory())
    : [];

/** Thư mục skill = có SKILL.md; `_shared` là thư viện dùng chung, không phải skill. */
const skillDirs = dirs('skills').filter(
  (d) => d !== '_shared' && existsSync(join(ROOT, 'skills', d, 'SKILL.md')),
);

/* ── 1 · Frontmatter hợp lệ và `name` khớp tên thư mục ───────────────── */
for (const d of skillDirs) {
  const src = read(`skills/${d}/SKILL.md`);
  const fm = src.match(/^---\n([\s\S]*?)\n---\n/);
  if (!fm) {
    no(`${d}: thiếu frontmatter — skill sẽ không load`);
    continue;
  }
  const name = fm[1].match(/^name:\s*(\S+)/m)?.[1];
  const desc = fm[1].match(/^description:\s*/m);
  if (!name) no(`${d}: frontmatter thiếu 'name'`);
  else if (name !== d) no(`${d}: name='${name}' không khớp tên thư mục`);
  else ok(`${d}: frontmatter + name`);
  if (!desc) no(`${d}: frontmatter thiếu 'description' — skill sẽ không được trigger đúng`);
}

/* ── 2 · Mọi link markdown nội bộ đều tồn tại ────────────────────────── */
const mdFiles = [];
const walk = (rel) => {
  for (const e of readdirSync(join(ROOT, rel))) {
    if (e === 'node_modules' || e === '.git') continue;
    const p = join(rel, e);
    if (statSync(join(ROOT, p)).isDirectory()) walk(p);
    else if (e.endsWith('.md')) mdFiles.push(p);
  }
};
['skills', 'agents', 'commands'].filter((d) => existsSync(join(ROOT, d))).forEach(walk);

let linkBad = 0;
for (const f of mdFiles) {
  const src = read(f);
  for (const m of src.matchAll(/\]\(([^)\s]+\.md)(#[^)]*)?\)/g)) {
    const target = m[1];
    if (/^https?:/.test(target)) continue;
    if (!existsSync(resolve(ROOT, dirname(f), target))) {
      no(`${f}: link gãy → ${target}`);
      linkBad++;
    }
  }
}
if (!linkBad) ok(`link nội bộ: ${mdFiles.length} file, không gãy`);

/* ── 3 · Đường ghi workspace khớp layout chuẩn ───────────────────────── */
const LAYOUT = 'skills/_shared/workspace-layout.md';
if (!existsSync(join(ROOT, LAYOUT))) {
  no(`thiếu ${LAYOUT} — nguồn duy nhất của cấu trúc workspace`);
} else {
  const layout = read(LAYOUT);
  const STAGES = ['01-discovery', '02-plan', '03-backlog', '04-quality', '05-delivery'];
  const missing = STAGES.filter((s) => !layout.includes(s));
  if (missing.length) no(`workspace-layout.md thiếu stage: ${missing.join(', ')}`);
  else ok('workspace-layout.md: đủ 5 stage');

  // Đường phẳng cũ còn sót: tasks/{ID}/<file>.md không qua thư mục stage
  const FLAT = /tasks\/\{(?:TICKET-)?ID\}\/(current-state|impact|plan|wbs-schedule|spec-analysis|test-checklist|ut-design|technical-approach|security|performance)\.md/g;
  let flatBad = 0;
  for (const f of mdFiles) {
    for (const m of read(f).matchAll(FLAT)) {
      no(`${f}: còn đường phẳng cũ → ${m[0]} (phải nằm trong thư mục stage)`);
      flatBad++;
    }
  }
  if (!flatBad) ok('không skill nào còn trỏ đường phẳng cũ');

  // Mọi đường tasks/{ID}/NN-*/ dùng trong skill phải là stage có thật
  let stageBad = 0;
  for (const f of mdFiles) {
    for (const m of read(f).matchAll(/tasks\/\{(?:TICKET-)?ID\}\/(\d{2}-[a-z]+)/g)) {
      if (!STAGES.includes(m[1])) {
        no(`${f}: stage không tồn tại → ${m[1]}`);
        stageBad++;
      }
    }
  }
  if (!stageBad) ok('mọi tham chiếu stage đều hợp lệ');
}

/* ── 4 · Không tham chiếu skill không tồn tại ────────────────────────── */
let refBad = 0;
for (const f of mdFiles) {
  for (const m of read(f).matchAll(/\/task-toolkit:([a-z-]+)/g)) {
    const s = m[1];
    if (s === 'help' || s === 'report') continue; // report là skill, help là command
    if (!skillDirs.includes(s) && !existsSync(join(ROOT, 'commands', `${s}.md`))) {
      no(`${f}: gọi /task-toolkit:${s} nhưng không có skill/command đó`);
      refBad++;
    }
  }
}
if (!refBad) ok('mọi /task-toolkit:<skill> đều tồn tại');

/* ── 5 · Không phụ thuộc plugin ngoài (mô tả nói "tự chứa đầy đủ") ──── */
const EXTERNAL = ['/rca-5why:', '/unittest-toolkit:', '/e2e-automator:'];
let extBad = 0;
for (const f of mdFiles) {
  const src = read(f);
  for (const e of EXTERNAL) {
    if (!src.includes(e)) continue;
    // ut-design cố ý đề nghị cài unittest-toolkit — hợp lệ, đã nói rõ là tuỳ chọn
    if (f.startsWith('skills/ut-design/') && e === '/unittest-toolkit:') continue;
    no(`${f}: phụ thuộc plugin ngoài ${e} — plugin khai "tự chứa đầy đủ"`);
    extBad++;
  }
}
if (!extBad) ok('không phụ thuộc plugin ngoài ngoài phần đã khai');

/* ── 5b · install.sh không hardcode danh sách skill ──────────────────── */
if (existsSync(join(ROOT, 'install.sh'))) {
  const sh = read('install.sh');
  const hard = sh.match(/^SKILLS_LIST=\((.+)\)/m);
  if (hard) {
    const listed = hard[1].trim().split(/\s+/);
    const drift = skillDirs.filter((s) => !listed.includes(s));
    no(
      `install.sh: SKILLS_LIST hardcode${drift.length ? ` và đã lệch — thiếu ${drift.join(', ')}` : ''}` +
        ' — phải dẫn xuất từ thư mục skills/',
    );
  } else if (/SKILLS_LIST=\(\)/.test(sh) && /SKILL\.md/.test(sh)) {
    ok('install.sh: danh sách skill dẫn xuất từ skills/, không hardcode');
  } else {
    no('install.sh: không tìm thấy cách dựng SKILLS_LIST');
  }
}

/* ── 5c · Quy ước viết skill (theo skill-creator) ─────────────────────── */
// 5c.1 SKILL.md < 500 dòng — vượt thì tách bớt sang reference/
for (const d of skillDirs) {
  const n = read(`skills/${d}/SKILL.md`).split('\n').length;
  if (n > 500) no(`${d}/SKILL.md: ${n} dòng — vượt 500, tách bớt sang reference/`);
}
ok(`SKILL.md: ${skillDirs.length} file đều dưới 500 dòng`);

// 5c.2 reference > 300 dòng phải có mục lục
let tocBad = 0;
for (const f of mdFiles.filter((x) => !x.endsWith('SKILL.md'))) {
  const src = read(f);
  if (src.split('\n').length <= 300) continue;
  if (!/^##\s+(Mục lục|Contents|Table of contents)/im.test(src)) {
    no(`${f}: >300 dòng nhưng thiếu Mục lục`);
    tocBad++;
  }
}
if (!tocBad) ok('reference dài đều có mục lục');

// 5c.3 description phải có cả trigger LẪN ranh giới (khi nào KHÔNG dùng)
for (const d of skillDirs) {
  const fm = read(`skills/${d}/SKILL.md`).match(/^---\n([\s\S]*?)\n---/)[1];
  const m = fm.match(/^description:\s*>-?\n((?:\s{2,}.*\n)+)/m) || fm.match(/^description:\s*(.+)$/m);
  const desc = m[1].replace(/\s+/g, ' ');
  if (!/trigger|dùng khi|when the user/i.test(desc)) no(`${d}: description thiếu trigger phrase`);
  if (!/\bNOT\b|do not use|not for|instead of|KHÔNG /.test(desc))
    no(`${d}: description thiếu ranh giới "khi nào KHÔNG dùng" — 12 skill sát nhau, dễ trigger nhầm`);
}
ok('description: đủ trigger + ranh giới');

// 5c.4 Layout chuẩn: mỗi skill chỉ có SKILL.md ở gốc, tài liệu phụ vào references/
for (const d of skillDirs) {
  for (const e of readdirSync(join(ROOT, 'skills', d))) {
    const full = join(ROOT, 'skills', d, e);
    if (statSync(full).isDirectory()) {
      if (!['references', 'scripts', 'assets'].includes(e))
        no(`skills/${d}/${e}/: thư mục lạ — chuẩn chỉ có references/ scripts/ assets/`);
    } else if (e !== 'SKILL.md') {
      no(`skills/${d}/${e}: tài liệu phụ phải nằm trong references/, không để ở gốc skill`);
    }
  }
}
ok('layout skill: SKILL.md ở gốc, phụ trợ trong references/');

/* ── 6 · plugin.json khớp thư mục skills/ ────────────────────────────── */
const pj = JSON.parse(read('.claude-plugin/plugin.json'));
if (!pj.version) no('plugin.json thiếu version');
else ok(`plugin.json: v${pj.version}, ${skillDirs.length} skill`);

/* ── 7 · Cửa vào (help/README) biết mọi skill ────────────────────────── */
for (const doc of ['commands/help.md', 'README.md']) {
  if (!existsSync(join(ROOT, doc))) {
    no(`thiếu ${doc}`);
    continue;
  }
  const src = read(doc);
  const unknown = skillDirs.filter((s) => !src.includes(s));
  if (unknown.length) no(`${doc}: chưa nhắc tới skill — ${unknown.join(', ')}`);
  else ok(`${doc}: biết đủ ${skillDirs.length} skill`);
}

/* ── kết quả ─────────────────────────────────────────────────────────── */
if (VERBOSE) pass.forEach((m) => console.log(`  ✅ ${m}`));
fail.forEach((m) => console.log(`  ❌ ${m}`));
const total = pass.length + fail.length;
console.log(
  fail.length
    ? `\nselftest: ${pass.length}/${total} — ${fail.length} lỗi`
    : `\nselftest: ${total}/${total} ✅`,
);
process.exit(fail.length ? 1 : 0);
