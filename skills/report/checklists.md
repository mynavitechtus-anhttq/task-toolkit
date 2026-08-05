# Report Gates — 3 checklist bắt buộc trước khi giao

## 1. Investigation checklist (điều tra đủ chưa)

- [ ] Repro được hiện tượng (hoặc bác bỏ được) — chạy thật, không suy diễn
- [ ] Timeline: từ commit / release / config change nào (`git log -S`, `git blame`, deploy history)
- [ ] Phạm vi 2 CHIỀU: cái bị ảnh hưởng VÀ cái không bị (env, user, data, màn hình)
- [ ] Dependency walk: component/service/CSS/DB/cache/URL dùng chung — kể cả repo anh em; mỗi cái liên quan có mặt trong Impact hoặc có dòng "không ảnh hưởng vì..."
- [ ] Cross-repo: nếu data chảy qua hệ thống khác → đã đọc code phía consumer (không đoán từ producer)
- [ ] Config/env diff giữa môi trường hoạt động đúng vs sai
- [ ] Trạng thái ĐANG CHẠY (version/config mỗi env, PR đã merge chưa) đọc **từ hệ thống** (git theo branch, container, console) — KHÔNG từ memory/ghi chú/PR title. Một PR có thể vẫn OPEN dù mọi người tưởng đã merge; memory phản ánh thời điểm ghi, không phải hiện tại
- [ ] Official docs đối chiếu cho behavior framework/library then chốt → link vào Refs
- [ ] Issue ngoài repo (infra/process/requirement/vendor notice): đã thu evidence theo bảng routing STAGE 2 — CLI/IaC/workflow/run history/spec tham chiếu; nguồn không truy cập được → [Giả định] + action cụ thể trong "Việc khách/team cần làm"
- [ ] Vendor notice: deadline + phạm vi resource bị ảnh hưởng đã đối chiếu với inventory THẬT của hệ thống mình (không chỉ chép lại notice)
- [ ] Yêu cầu mới từ khách: tách 3 nhóm — yêu cầu rõ / suy ra / open questions cần khách confirm; tham chiếu (PR/spec) đã đọc thật
- [ ] Bug cũ tình cờ phát hiện → đã ghi repro + evidence vào "Phát hiện ngoài phạm vi" (không lờ, không âm thầm fix)

## 2. Conclusion-quality checklist (kết luận đạt chưa)

- [ ] Root cause là "why" (lỗ hổng khiến nó xảy ra ĐƯỢC) chứ không phải "what" (dòng code hỏng)
- [ ] Fix root cause thì hết tái diễn? Nếu không → chưa phải root cause, đào tiếp
- [ ] Trigger và cause tách bạch
- [ ] Không dừng ở lỗi cá nhân — "đổi người khác vẫn xảy ra?" → phải xuống tầng quy trình/hệ thống
- [ ] Claim chưa verify đã đánh dấu [Giả định — cách verify: …]; claim còn lại đều có nguồn khi then chốt — không có claim trần
- [ ] Có cân nhắc ít nhất 1 giả thuyết cạnh tranh và loại nó bằng facts (chống anchoring)
- [ ] Số liệu cụ thể thay cho "nhanh hơn / nhiều hơn / ổn định hơn"

## 3. Writing-quality checklist (văn bản đạt chưa)

- [ ] TL;DR đứng ĐẦU và ≤ 5 dòng — người đọc dừng ở đó vẫn hiểu đúng
- [ ] Icon tối thiểu: không emoji heading, không icon từng dòng; chỉ có dấu [Giả định] khi cần
- [ ] Không ví von phi kỹ thuật; thuật ngữ IT giữ nguyên + giải thích ngắn trong ngoặc khi cần
- [ ] Nguyên nhân gốc/Kết luận trình bày gạch đầu dòng, không phải đoạn văn
- [ ] Chuỗi 5 Whys dạng bảng (Tầng | Nguyên nhân | Evidence), không phải chuỗi hỏi-đáp
- [ ] Tầng 1 (trên vạch `---`) không còn jargon chưa giải thích; ≤ ~1 trang
- [ ] Chi tiết kỹ thuật nằm DƯỚI vạch, có file:line
- [ ] Không kể chuyện điều tra theo thời gian
- [ ] Mỗi next action có chủ ngữ + thời hạn
- [ ] Bảng cho facts đếm được; không có đoạn văn khổng lồ
- [ ] Chuỗi UI sản phẩm (tiếng Nhật) giữ nguyên, không dịch
- [ ] Đúng locale + tone (JA khách = keigo); audience customer → đã qua agent `report-reviewer` + rà redact (tên người, credential, URL nội bộ → vai trò/`***`)
- [ ] Không câu nào "cho có" — xoá được mà nghĩa không đổi thì xoá
