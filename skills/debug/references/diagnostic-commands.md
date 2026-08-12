# Diagnostic Commands — thư viện lệnh chẩn đoán

> Dùng cho **Bước 1 (định vị)** và **Bước 3 (verify giả thuyết)** của `SKILL.md`. Điều chỉnh theo stack thật của repo — bảng dưới là khung, không phải lệnh copy-paste mù.

## Luật an toàn (đọc trước khi chạy bất cứ thứ gì)

- **Mặc định chỉ read-only.** Lệnh có thể đổi trạng thái (restart, flush, migrate, DELETE/UPDATE, scale) → **hỏi user trước**, nêu rõ lệnh và hệ quả.
- Trên **production**: thu evidence trước khi trạng thái biến mất (log, snapshot, `describe`), vì restart/deploy sẽ xoá dấu vết.
- Không đọc/echo credential, token, giá trị secret. Chỉ kiểm tra **có được set hay không**, không in giá trị.
- Không truy cập được (thiếu quyền/không có env) → **không đoán**: ghi `[MISSING-SOURCE]` + đưa yêu cầu cụ thể vào "Việc khách/team cần làm".

## Bước 1 — Instrument ranh giới component

Nguyên tắc: mỗi ranh giới in **vào / ra / config có tới được không**, chạy MỘT lượt, rồi đọc.

```bash
echo "=== [L1] entry: request/trigger nhận gì ==="
# id request, tham số, user/tenant, thời điểm

echo "=== [L2] biên service: env/config có truyền qua không ==="
env | grep -E '^(APP_|DB_|CACHE_|API_)' | sed 's/=.*/=<set>/'   # CHỈ xem có set, không in giá trị

echo "=== [L3] biên data: query gì / trả về gì ==="
# câu query thật + số dòng trả về (không phải kỳ vọng)

echo "=== [L4] output: cái gì thật sự đi ra ==="
# status code, payload shape, thứ được ghi xuống
```

Đọc kết quả theo hướng: **ranh giới đầu tiên mà "ra" khác "vào" chính là nơi cần đào**. Các layer sau đó chỉ là hệ quả.

## Theo loại hệ thống

### Database / query

```sql
-- Trạng thái dữ liệu thật của case lỗi (KHÔNG suy từ code)
SELECT <cột liên quan> FROM <bảng> WHERE <điều kiện case lỗi> LIMIT 20;

-- NULL / giá trị ngoài dự kiến — nguồn bug kinh điển
SELECT COUNT(*) AS total, COUNT(<cột>) AS non_null FROM <bảng>;

-- Có thay đổi gần thời điểm lỗi không
SELECT * FROM <bảng> WHERE updated_at > NOW() - INTERVAL '1 hour' ORDER BY updated_at DESC;

-- Chậm: xem kế hoạch thật, đừng đoán index
EXPLAIN ANALYZE <query>;
```

Đối chiếu **schema thật** với model/migration trong code — lệch schema↔code là ca "đối chiếu khai báo trùng lặp" điển hình.

### Service / process

```bash
systemctl status <service>            # hoặc: docker ps / kubectl get pods
journalctl -u <service> -n 200 --no-pager --since "1 hour ago"
docker logs --tail 200 --since 1h <container>
kubectl logs <pod> --tail=200 --previous   # --previous: log của lần crash trước

df -h                                 # đầy disk gây lỗi cực kỳ khó đoán
free -h
ss -tulpn | grep <port>
```

### Ứng dụng / runtime

```bash
ps aux | grep <process>
printenv | grep <PREFIX> | sed 's/=.*/=<set>/'

git log --oneline -15
git log -S '<chuỗi/hàm nghi>' --oneline      # lần đầu chuỗi này xuất hiện/biến mất
git blame -L <from>,<to> <file>
git diff <tag-hoạt-động>..<tag-lỗi> -- <path>
```

`git log -S` là cách nhanh nhất trả lời "lỗi bắt đầu từ thay đổi nào" khi đã khoanh được vùng code.

### Network / API

```bash
curl -sS -o /dev/null -w 'code=%{http_code} dns=%{time_namelookup} conn=%{time_connect} ttfb=%{time_starttransfer} total=%{time_total}\n' \
  "https://<host>/<path>"

curl -i -X <METHOD> "https://<host>/<path>" -H 'Content-Type: application/json' -d '<payload>'
dig +short <host>          # hoặc nslookup
openssl s_client -connect <host>:443 -servername <host> </dev/null 2>/dev/null | openssl x509 -noout -dates
```

Bảng `-w` tách được **chậm ở đâu**: DNS / bắt tay / server nghĩ lâu / truyền dữ liệu.

### Dependency / build

```bash
# Đọc version ĐÃ RESOLVE (lock file), không đọc khai báo trong manifest
npm ls <package>            # package-lock.json
pip show <package>          # pip freeze
composer show <vendor/pkg>  # composer.lock
```

Khai báo `^1.2.0` và cái thật sự cài có thể khác nhau — đây là nguồn của phần lớn ca "máy tôi chạy được".

### Container / CI-CD

```bash
docker image inspect <image> --format '{{.Created}} {{.Id}}'
docker run --rm <image> <lệnh in version của runtime>      # version THẬT trong image

gh run list --workflow=<file> --limit 20
gh run view <run-id> --log-failed
```

Đối chiếu version pin ở CI ↔ Dockerfile ↔ image đang chạy thật. Ba chỗ, dễ lệch, lệch im lặng.

## "Máy tôi chạy được" — chụp trạng thái hai bên rồi diff

Chạy trên **cả hai** máy, xuất ra file, rồi `diff`:

```bash
{
  echo "== os ==";      uname -a
  echo "== runtime ==";  node -v 2>/dev/null; python3 -V 2>/dev/null; php -v 2>/dev/null | head -1
  echo "== pkg mgr ==";  npm -v 2>/dev/null; pip -V 2>/dev/null
  echo "== env ==";      printenv | grep -E '^(APP_|DB_|CACHE_|API_|NODE_|PYTHON)' | sed 's/=.*/=<set>/' | sort
  echo "== deps ==";     ( [ -f package-lock.json ] && md5 -q package-lock.json ) 2>/dev/null
  echo "== git ==";      git rev-parse HEAD; git status --porcelain
  echo "== tz/locale =="; date; echo "$LANG"
} > snapshot-$(hostname).txt
```

Múi giờ và locale là hai thứ hay bị bỏ qua nhất trong nhóm bug "chỉ sai ở một môi trường".

## Lỗi chập chờn — dựng bẫy thay vì đoán

Chưa bắt được thì đừng lập giả thuyết bừa. Thêm quan sát rồi chờ lần sau:

- Log kèm **correlation ID** xuyên suốt các layer để nối được một request qua nhiều service.
- Ghi lại **thời điểm + tải + version** ở mỗi lần lỗi → tìm tương quan (giờ cao điểm? sau deploy? khi cache hết hạn?).
- Đo tần suất trước và sau khi đổi một biến — không đổi hai biến cùng lúc.

Ghi rõ trong report: đang ở trạng thái **chờ tái hiện với instrument đã thêm**, kèm `[Giả định — cách verify]`. Đó là kết luận trung thực, không phải thất bại.
