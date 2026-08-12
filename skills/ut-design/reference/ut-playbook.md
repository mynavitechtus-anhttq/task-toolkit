# UT Agent Playbook — Hợp đồng thực thi khi thiết kế & gen Unit Test

> **Đối tượng đọc:** AI coding agent (và developer điều phối agent). Đây **không phải** checklist cho người tick — đây là **hợp đồng thực thi**: agent PHẢI đọc, tuân thủ, và tự chứng minh đã tuân thủ.
>
> **Nguồn tri thức đi kèm (bắt buộc đọc cùng):** [`viewpoints-matrix.md`](viewpoints-matrix.md) — chứa toàn bộ prose + ví dụ Given–When–Then của từng quan điểm. Playbook này **tham chiếu** tới nó bằng ID (A1…F10). Khi cần hiểu *ý nghĩa* một viewpoint, đọc file đó; khi cần biết *phải làm gì và khi nào coi là xong*, đọc file này.

## Quy ước từ khóa (RFC 2119)

**MUST / PHẢI**, **MUST NOT / KHÔNG ĐƯỢC**, **SHOULD / NÊN**, **MAY / CÓ THỂ**. Vi phạm một dòng **MUST/MUST NOT** = kết quả **không hợp lệ**, agent PHẢI tự sửa trước khi báo hoàn tất.

Few-shot trong file này viết bằng **pseudocode trung lập**. Agent PHẢI dịch sang đúng test framework của dự án đích (flutter_test, Jest/Vitest, JUnit… — giữ nguyên ngữ nghĩa, tên test, và comment tag).

---

## §0. Giao thức thực thi (agent PHẢI theo đúng thứ tự)

```
1. ĐỌC: spec của unit đang test  +  file quan điểm (nguồn tri thức)  +  playbook này.
2. XÁC ĐỊNH PHẠM VI: với mỗi viewpoint ở §2, đánh giá `applies_when` → lập DANH SÁCH ÁP DỤNG.
3. CỔNG SPEC: nếu spec KHÔNG đủ để suy ra `expected` của bất kỳ case nào
   → STOP. Ghi `TODO(spec): <câu hỏi>`. KHÔNG đoán, KHÔNG bịa giá trị. (xem §7)
4. THIẾT KẾ CASE: cho mỗi viewpoint áp dụng, viết case dạng Given–When–Then.
5. SINH TEST: theo §4. Mỗi test PHẢI tag `viewpoint:<ID>`. `expected` suy từ SPEC (§1).
6. CHẠY: test + báo cáo coverage. Test đỏ → xử lý theo §1 (KHÔNG được gian để xanh).
7. CỔNG DONE (§3): nếu chưa đạt → BỔ SUNG test, KHÔNG hạ chuẩn / KHÔNG nới assertion.
8. XUẤT: đúng định dạng đầu ra §6 (test code + bảng truy vết + open questions).
```

Agent **MUST NOT** nhảy cóc bước 2, 3, 7. Đặc biệt: **không được** đi thẳng từ "đọc code" sang "viết test cho xanh coverage".

---

## §1. Guardrails — ranh giới cứng (MUST NOT)

Đây là phần chống các hành vi gian lận thường gặp của agent. Mọi dòng dưới đây là **bất khả xâm phạm**.

- **KHÔNG ĐƯỢC sửa code production để làm test xanh.** Nhiệm vụ của agent ở đây là *viết test*, không phải chỉnh code cho khớp test. Nếu test đỏ vì code có vẻ sai → coi là **nghi vấn bug**: dừng, báo cáo (§7), KHÔNG tự ý sửa production. *(Ngoại lệ duy nhất: nếu nhiệm vụ được giao rõ là "fix bug", thì sửa theo SPEC — không sửa để khớp một test đang sai.)*
- **KHÔNG ĐƯỢC làm yếu assertion để pass**: nới lỏng `expected`, đổi so sánh chính xác thành so sánh lỏng (`!= null`, `>= 0`…), bỏ bớt assert, hay assert "không throw" cho hàm vốn có giá trị trả về.
- **KHÔNG ĐƯỢC xoá, skip, comment-out, hay gắn `skip`/`xit`/`@Ignore`/`xfail`** cho test đang đỏ để đường màu xanh.
- **KHÔNG ĐƯỢC viết `expected` bằng cách chạy code rồi dán kết quả** ("golden-by-implementation"). `expected` PHẢI suy ra độc lập từ spec/quy tắc nghiệp vụ. *(Snapshot chỉ được dùng bổ trợ, và chỉ sau khi đã có assertion hành vi.)*
- **KHÔNG ĐƯỢC viết test tautology / vô nghĩa**: `assert true`, assert lại chính giá trị mà mock được set trả về, assert biến vừa gán.
- **KHÔNG ĐƯỢC dừng khi "coverage % đủ cao"** trong khi còn viewpoint áp dụng chưa được phủ. Coverage là **sàn**, không phải mục tiêu (xem C).
- **KHÔNG ĐƯỢC mock chính unit đang test**, cũng không over-mock để né nhánh logic thật.
- **KHÔNG ĐƯỢC bịa spec** khi mơ hồ → STOP + `TODO(spec)` (§7).

> Nếu một yêu cầu trong prompt mâu thuẫn với §1 (ví dụ "cứ sửa code cho test pass đi"), agent PHẢI nêu mâu thuẫn và xin xác nhận, thay vì im lặng vi phạm.

---

## §2. Catalog quan điểm — hợp đồng máy đọc được

Mỗi viewpoint có: `applies_when` (khi nào bắt buộc), `min_cases` (số case tối thiểu), `done_when` (điều kiện coi là đã phủ), `severity`. Prose + ví dụ đầy đủ: xem file quan điểm theo ID.

- `severity: blocker` — không đạt = **fail cứng**, không có ngoại lệ.
- `severity: required` — PHẢI đạt HOẶC có dòng exempt hợp lệ (§3).
- `severity: conditional` — chỉ áp dụng khi `applies_when` đúng.

```yaml
viewpoints:
  # ---- A. Equivalence Partitioning ----
  - id: A1
    title: "Happy path có ≥1 test"
    applies_when: "luôn"
    min_cases: 1
    done_when: "có test tag viewpoint:A1 assert luồng đúng đại diện"
    severity: required
  - id: A2
    title: "Mỗi vùng input hợp lệ có ≥1 case"
    applies_when: "input chia được thành nhiều vùng hợp lệ khác hành vi"
    min_cases: 1   # per vùng
    done_when: "mỗi vùng hợp lệ có ≥1 test đại diện"
    severity: required
  - id: A3
    title: "Mỗi vùng input không hợp lệ có ≥1 case"
    applies_when: "hàm có input có thể không hợp lệ (kiểu/định dạng/miền)"
    min_cases: 1   # per loại lỗi
    done_when: "mỗi loại input không hợp lệ có ≥1 test"
    severity: required

  # ---- B. Boundary Value Analysis ----
  - id: B1
    title: "Biên min/max và min-1/max+1"
    applies_when: "input có miền bị chặn (số, độ dài chuỗi, kích thước collection)"
    min_cases: 4
    done_when: "có test cho min, min-1, max, max+1"
    severity: required
  - id: B2
    title: "0, rỗng, null/undefined"
    applies_when: "luôn (khi tham số có thể nhận các giá trị này)"
    min_cases: 1
    done_when: "có test cho các giá trị rỗng/không tồn tại áp dụng được"
    severity: required
  - id: B3
    title: "Chuỗi: rỗng, toàn khoảng trắng, độ dài tối đa, đa byte"
    applies_when: "có tham số kiểu chuỗi"
    min_cases: 3
    done_when: "có test rỗng, biên độ dài, và ký tự đa byte/đặc biệt"
    severity: required
  - id: B4
    title: "Collection: rỗng, 1, nhiều, trùng lặp"
    applies_when: "có tham số kiểu collection/list/map"
    min_cases: 3
    done_when: "có test rỗng, 1 phần tử, nhiều phần tử (+ trùng nếu có ý nghĩa)"
    severity: required

  # ---- C. Branch + Condition Coverage ----
  - id: C1
    title: "Branch coverage — mỗi nhánh lấy cả true/false"
    applies_when: "hàm có nhánh (if/else, switch, ternary, early return, loop)"
    done_when: "báo cáo coverage: branch = 100% HOẶC nhánh chưa phủ có coverage-exempt"
    severity: blocker
  - id: C2
    title: "Condition coverage — mỗi điều kiện con true/false"
    applies_when: "có điều kiện phức hợp (&&, ||)"
    done_when: "mỗi điều kiện con nguyên tử đã nhận cả true lẫn false"
    severity: blocker
  - id: C3
    title: "Đạt đồng thời Branch + Condition (C/DC)"
    applies_when: "có nhánh chứa điều kiện phức hợp"
    done_when: "cả C1 và C2 cùng đạt (không dùng cái này thay cái kia)"
    severity: blocker
  - id: C4
    title: "Bảng quyết định cho điều kiện kết hợp"
    applies_when: "kết quả phụ thuộc tổ hợp ≥2 điều kiện"
    done_when: "phủ các tổ hợp có nghĩa; tổ hợp bất khả thi phải ghi lý do loại"
    severity: required

  # ---- D. Exception & Interaction ----
  - id: D1
    title: "Throw đúng loại + message/code"
    applies_when: "hàm có thể ném exception"
    done_when: "có test khẳng định đúng loại exception và message/error code"
    severity: required
  - id: D2
    title: "Cleanup/rollback sau lỗi"
    applies_when: "hàm giữ resource/transaction/khóa"
    done_when: "có test lỗi giữa chừng → resource được giải phóng / rollback"
    severity: required
  - id: D3
    title: "Lỗi từ dependency được xử lý đúng"
    applies_when: "hàm gọi dependency I/O (đã mock được)"
    done_when: "mock trả lỗi/timeout → có test khẳng định hành vi kiểm soát"
    severity: required
  - id: D4
    title: "Kiểm chứng tương tác (interaction)"
    applies_when: "hàm gọi collaborator / có side-effect (void, gọi API, emit, ghi DB)"
    done_when: "có test verify collaborator được gọi đúng hàm, đúng tham số, đúng số lần"
    severity: required
  - id: D5
    title: "Idempotency / retry"
    applies_when: "hàm tạo/ghi có thể bị gọi lại hoặc retry sau timeout"
    done_when: "có test: gọi lại/retry KHÔNG nhân đôi tác dụng phụ"
    severity: required

  # ---- E. State & Non-determinism ----
  - id: E1
    title: "State machine: chuyển hợp lệ + ≥1 chuyển không hợp lệ"
    applies_when: "unit là/điều khiển máy trạng thái"
    done_when: "phủ các transition hợp lệ + ≥1 transition bị cấm"
    severity: required
  - id: E2
    title: "Không phụ thuộc time/random/thứ tự; múi giờ/DST"
    applies_when: "hàm dùng thời gian thực, random, hoặc phụ thuộc ngày-giờ"
    done_when: "clock/seed được inject cố định; có test múi giờ/DST nếu áp dụng"
    severity: blocker
  - id: E3
    title: "Đối chiếu bug lịch sử (Error Guessing)"
    applies_when: "luôn (rà Phụ lục B của file quan điểm)"
    done_when: "mọi quan điểm bug-lịch-sử áp dụng cho unit này đã có test"
    severity: required
  - id: E4
    title: "Bất định do đồng thời (async/concurrency)"
    applies_when: "hàm async (Future/Stream/promise) hoặc có shared state"
    done_when: "có test thứ tự hoàn thành khác nhau / gọi đồng thời / race trên shared state"
    severity: required

  # ---- F. Domain-specific triggers (locale Nhật & nghiệp vụ) ----
  - id: F1
    title: "Chuẩn hóa/trim chuỗi (full/half-width)"
    applies_when: "hàm chuẩn hóa/trim/convert chuỗi"
    done_when: "có test full-width lẫn half-width + quy tắc convert theo spec"
    severity: conditional
  - id: F2
    title: "Kana (Hiragana↔Katakana), furigana"
    applies_when: "hàm so khớp/chuyển đổi kana hoặc sinh furigana"
    done_when: "có test chuẩn hóa Hiragana↔Katakana theo spec"
    severity: conditional
  - id: F3
    title: "Sort/compare chuỗi Nhật (gojūon, dakuten)"
    applies_when: "hàm sort/compare chuỗi tiếng Nhật"
    done_when: "có test thứ tự gojūon + dakuten/handakuten + ổn định khi bằng"
    severity: conditional
  - id: F4
    title: "Ngày Nhật (niên hiệu/era, biên tháng/năm)"
    applies_when: "hàm parse/format/tính ngày"
    done_when: "có test era↔dương lịch, điểm giao era, biên 29/2 & cuối tháng/năm"
    severity: conditional
  - id: F5
    title: "Tiền yên / số học tiền (làm tròn .5)"
    applies_when: "hàm format/tính tiền"
    done_when: "có test làm tròn .5 đúng chiều, phân cách nghìn, thập phân, số âm"
    severity: conditional
  - id: F6
    title: "Đếm độ dài chuỗi (dakuten, surrogate)"
    applies_when: "hàm đếm độ dài chuỗi"
    done_when: "có test dakuten/handakuten + surrogate pair (Kanji 4-byte, emoji)"
    severity: conditional
  - id: F7
    title: "Validate định dạng theo rule dự án"
    applies_when: "hàm validate email/SĐT/định dạng theo rule TechTus"
    done_when: "có test hợp lệ + từng loại vi phạm + thứ tự ưu tiên thông báo"
    severity: conditional
  - id: F8
    title: "Auto-fill mã bưu chính"
    applies_when: "hàm tra cứu/auto-fill từ mã bưu chính (master data)"
    done_when: "có test tìm thấy / không tìm thấy / lỗi API (mock)"
    severity: conditional
  - id: F9
    title: "Trường bắt buộc có điều kiện"
    applies_when: "có rule 'A bắt buộc nếu B'"
    done_when: "có test đủ tổ hợp phụ thuộc chéo"
    severity: conditional
  - id: F10
    title: "Quy tắc trigger/thông báo nghiệp vụ"
    applies_when: "hàm quyết định kích hoạt trigger/notification"
    done_when: "có test kích hoạt đúng/không, hủy giữa chừng, nhiều trigger cùng thỏa"
    severity: conditional
```

---

## §3. Definition of Done — cổng kiểm được bằng máy

Một unit **CHỈ** được coi là "đã đủ test" khi **tất cả** điều kiện sau đúng:

1. **Phủ viewpoint:** mọi viewpoint có `applies_when = true` đều có ≥ `min_cases` test tag đúng ID, **HOẶC** có dòng exempt hợp lệ.
2. **Phủ cấu trúc:** báo cáo coverage cho unit đạt **branch = 100% và condition = 100%**, **HOẶC** mỗi nhánh/điều kiện chưa phủ có marker `coverage-exempt` ngay tại vị trí đó.
3. **Truy vết:** bảng truy vết (§6) được xuất, **không có ô `missing` nào thiếu lý do**.
4. **Sạch:** toàn bộ test **PASS**, và đạt được **mà không** vi phạm §1 (không sửa production để xanh, không skip, không nới assertion).

**Định dạng marker exempt (bắt buộc, để grep được):**

```
// viewpoint-exempt: <ID> — <lý do cụ thể, không được "N/A">
// coverage-exempt: <lý do cụ thể>            (đặt ngay tại nhánh không thể/không cần phủ)
```

Exempt PHẢI có lý do thực chất (vd "nhánh defensive cho trường hợp compiler đã loại", "tổ hợp bất khả thi vì enum chỉ 2 giá trị"). Lý do rỗng/`N/A`/`sau này làm` = **không hợp lệ**.

**Lệnh tự kiểm (agent NÊN chạy trước khi báo hoàn tất):**

```
# Liệt kê mọi viewpoint đã phủ trong test:
grep -RhoE "viewpoint:[A-F][0-9]+" <thư mục test> | sort | uniq -c
# Liệt kê mọi exempt để review:
grep -RnE "viewpoint-exempt|coverage-exempt" <thư mục test> <thư mục src>
# Chặn cheat: tìm test bị skip/vô hiệu:
grep -RnE "\b(skip|xit|xdescribe|@Ignore|xfail|it\.skip|test\.skip)\b" <thư mục test>
# Coverage: chạy công cụ của dự án (vd `flutter test --coverage`, `jest --coverage`)
```

---

## §4. Luật viết test (MUST)

- **Đặt tên (bắt buộc tiếng Anh):** `methodName_stateUnderTest_expectedBehavior`. VD: `calcShippingFee_whenVipCustomer_returnsZero`. KHÔNG đặt tiếng Việt/Nhật, KHÔNG `test1`/`testOK`.
- **Cấu trúc AAA = Given–When–Then:** Arrange (Given) → Act (When) → Assert (Then). Một test xác minh **đúng một hành vi**.
- **Tag viewpoint:** mỗi test PHẢI có comment `// viewpoint:<ID>` ngay tại tên/đầu test. Một test phủ nhiều viewpoint thì liệt kê nhiều ID.
- **Expected từ spec:** giá trị kỳ vọng nêu **tại sao** đúng theo spec (comment ngắn), không phải "vì hàm trả về thế".
- **Dữ liệu tất định:** inject clock/seed; dùng hằng số **có tên**, không magic number; dùng builder/fixture cho object phức tạp; KHÔNG `now()`/random thật.
- **Mock đúng ranh giới:** chỉ mock tại I/O (API, DB, file, thời gian, random). KHÔNG mock nội bộ unit. Mock PHẢI định nghĩa cả nhánh lỗi/timeout (nối D3).
- **Không logic trong test:** KHÔNG `if/for/while/try` trong thân test. Nhiều biến thể → dùng **parameterized/table test**, không copy-paste và không cắt bớt case.
- **Assertion cụ thể:** so sánh giá trị/loại lỗi rõ ràng; mỗi assert có ý nghĩa (tránh Assertion Roulette — thêm message khi cần).

---

## §5. Few-shot đối chiếu (pseudocode trung lập — dịch sang framework dự án)

### ✅ TỐT — làm theo

```
# viewpoint:B1  (biên dưới của validateAge, hợp lệ 18–120)
test "validateAge_whenBelowMin_returnsInvalid":
    # Given: 17 = min-1 theo spec (min hợp lệ = 18)
    age = 17
    # When
    result = validateAge(age)
    # Then: expected suy từ SPEC (min=18), KHÔNG từ việc chạy hàm
    assert result == INVALID

# viewpoint:D4  (interaction — hàm void có side-effect)
test "checkout_whenValidOrder_chargesGatewayOnce":
    # Given
    gateway = mock(PaymentGateway)
    order   = orderBuilder(total = 500_000)
    # When
    checkout(order, gateway)
    # Then: verify tương tác, không chỉ return value
    verify(gateway.charge).calledOnceWith(500_000)   # đúng 1 lần, đúng tham số

# viewpoint:C4  (bảng quyết định — parameterized, phủ tổ hợp)
parameterized "calcShippingFee_byTier":
    cases = [
        (vip=true,  fast=true,  expected=0),
        (vip=true,  fast=false, expected=0),
        (vip=false, fast=true,  expected=50_000),
        (vip=false, fast=false, expected=30_000),
    ]
    for (vip, fast, expected) in cases:
        assert calcShippingFee(order(vip, fast)) == expected
```

### ❌ SAI — cấm (vi phạm §1)

```
# ❌ Golden-by-implementation: dán output hiện tại làm expected
test "...":
    assert calcShippingFee(order) == 47231   # con số này chỉ là cái hàm ĐANG trả về

# ❌ Tautology / assert lại chính mock
mock(repo.find).returns(user)
assert repo.find(id) == user                 # vô nghĩa, không kiểm gì của unit

# ❌ Assertion lỏng để pass
assert result != null                        # không khẳng định giá trị đúng
assert doesNotThrow(() -> parseDate(s))      # nuốt luôn việc kiểm kết quả

# ❌ Né test đỏ để lấy màu xanh
skip test "parseDate_whenInvalid_throws": ...           # cấm skip
# assert ...                                            # cấm comment-out assert

# ❌ Gộp nhiều hành vi để giảm số test
test "validateAge_allCases":                 # trộn happy + boundary + invalid
    assert validateAge(25) == VALID
    assert validateAge(17) == INVALID
    assert validateAge("x") == INVALID       # tách thành 3 test riêng
```

---

## §6. Định dạng đầu ra bắt buộc (agent PHẢI xuất đủ 4 phần)

1. **Kế hoạch viewpoint** — bảng: `ID | áp dụng? | lý do | case dự kiến`. Viewpoint không áp dụng ghi rõ vì sao.
2. **Test code** — theo §4, mỗi test có tag `viewpoint:<ID>`.
3. **Bảng truy vết** — chứng minh DoD:

   | Viewpoint | Test phủ | Trạng thái | Ghi chú |
   | --- | --- | --- | --- |
   | B1 | `validateAge_whenBelowMin_returnsInvalid`, … | covered | |
   | D2 | — | exempt | không giữ resource |
   | … | | | |

   + số liệu coverage (branch %, condition %). Trạng thái ∈ {covered, exempt, **missing**}. **Không được** còn `missing` nào khi báo hoàn tất.
4. **Open questions** — liệt kê mọi `TODO(spec)` đã đặt.

---

## §7. Escalation / STOP (khi nào dừng thay vì đoán)

Agent PHẢI **dừng và hỏi** (không tự quyết) khi:

- Spec không đủ để xác định `expected` của một case → `TODO(spec): <câu hỏi>`, KHÔNG bịa giá trị.
- Test đỏ và nghi code production sai → báo cáo như **nghi vấn bug** (kèm test tái hiện), KHÔNG tự sửa production (trừ khi nhiệm vụ là fix bug).
- Yêu cầu trong prompt mâu thuẫn với §1.
- Cần mock quá nhiều mới test được một unit → cảnh báo *có thể thiết kế production sai*, hỏi trước khi tiếp tục.

Khi STOP: vẫn xuất phần việc đã làm + danh sách câu hỏi, không im lặng bỏ ngang.

---

## §8. Chống lười / làm qua loa (MUST)

- PHẢI sinh test cho **mọi** viewpoint áp dụng — gồm **abnormal, boundary, exception**, không chỉ happy path.
- **Coverage cao KHÔNG phải điều kiện dừng.** Điều kiện dừng duy nhất là **cổng DoD §3**. Đạt 100% branch mà thiếu viewpoint áp dụng (vd D4, E4) = **chưa xong**.
- KHÔNG gộp hành vi để giảm số test; KHÔNG tạo happy-path trùng lặp để "trông có nhiều test".
- Số case lớn → dùng parameterized, **không** cắt bớt case để nhanh.
- Chạy lại agent trên cùng unit **không** được nhân bản test đã có (idempotent) — cập nhật/bổ sung, không thêm trùng.

---

*Playbook v0.1 — cặp đôi với `viewpoints-matrix.md` (nguồn tri thức, ID A1…F10). Few-shot là pseudocode trung lập; agent dịch sang framework dự án đích. Phần few-shot "từ code thật" sẽ thay các hàm giả định (`validateAge`, `calcShippingFee`…) bằng ví dụ trích từ codebase khi dự án đã có mã nguồn.*
