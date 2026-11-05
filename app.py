from flask import Flask, request, jsonify, render_template
from urllib.parse import urlparse, urljoin
import requests

app = Flask(__name__)

ALLOWED_START_HOSTS = {"gtraffic.io", "www.gtraffic.io"}
TIMEOUT = 12
MAX_HOPS = 8

@app.get("/")
def home():
    return render_template("index.html")

def valid_http_url(value):
    try:
        p = urlparse(value.strip())
        return p.scheme in ("http", "https") and bool(p.hostname)
    except Exception:
        return False

@app.post("/resolve")
def resolve():
    data = request.get_json(silent=True) or {}
    original = (data.get("url") or "").strip()
    if not valid_http_url(original):
        return jsonify(ok=False, error="URL không hợp lệ."), 400

    parsed = urlparse(original)
    if parsed.hostname.lower() not in ALLOWED_START_HOSTS:
        return jsonify(ok=False, error="Chỉ hỗ trợ link bắt đầu từ gtraffic.io."), 400

    current = original
    chain = [current]
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GTrafficLinkChecker/4.0)"}

    try:
        for _ in range(MAX_HOPS):
            # Chỉ đọc redirect HTTP thông thường. Không chạy JavaScript,
            # không gửi CAPTCHA, không giả lập phiên đăng nhập hay né chống bot.
            response = requests.get(
                current, headers=headers, allow_redirects=False,
                timeout=TIMEOUT, stream=True
            )
            status = response.status_code
            location = response.headers.get("Location")
            response.close()

            if status not in (301, 302, 303, 307, 308) or not location:
                return jsonify(
                    ok=True, original=original, current=current,
                    chain=chain, status=status,
                    note="Đây là điểm dừng của redirect HTTP. Nếu trang yêu cầu CAPTCHA hoặc chuyển hướng bằng JavaScript, hãy mở bằng Safari và hoàn tất xác minh."
                )

            next_url = urljoin(current, location)
            if not valid_http_url(next_url):
                return jsonify(ok=True, original=original, current=current,
                                chain=chain, status=status,
                                note="Redirect trả về URL không hợp lệ.")
            chain.append(next_url)
            current = next_url

            # Không tiếp tục truy cập máy chủ bên ngoài GTraffic.
            # Chỉ hiển thị URL đích được trả về trong header Location.
            next_host = (urlparse(current).hostname or "").lower()
            if next_host not in ALLOWED_START_HOSTS:
                return jsonify(
                    ok=True, original=original, current=current,
                    chain=chain, status=status,
                    note="Đã tìm thấy URL chuyển hướng ra ngoài GTraffic. Mở URL này trong Safari để tiếp tục nếu trang đích còn bước xác minh."
                )

        return jsonify(ok=True, original=original, current=current,
                       chain=chain, status=None,
                       note=f"Đã dừng ở giới hạn {MAX_HOPS} bước redirect.")
    except requests.RequestException as exc:
        return jsonify(
            ok=False,
            error="Không đọc được redirect HTTP. Link có thể cần JavaScript, CAPTCHA hoặc chặn truy cập tự động.",
            detail=str(exc)[:220]
        ), 200

@app.get("/health")
def health():
    return {"ok": True, "version": "4.0"}

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
