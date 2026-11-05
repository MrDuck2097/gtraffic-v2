# GTraffic Link Tool V4

## Tính năng
- Kiểm tra redirect HTTP thông thường từ link `gtraffic.io`.
- Hiển thị chuỗi redirect và URL đích nếu được trả về bằng HTTP `Location`.
- Tạo bookmarklet cho Safari để gửi URL hiện tại về app sau khi người dùng tự hoàn tất CAPTCHA.

## Giới hạn
- Không giải CAPTCHA, không tự gửi mã xác minh và không né cơ chế chống bot.
- Không thực thi JavaScript của trang GTraffic trên máy chủ.
- Nếu trang đổi URL bằng JavaScript hoặc giữ đích trong trạng thái nội bộ, bookmarklet chỉ lấy URL đang hiển thị trên thanh địa chỉ.

## Deploy Render
1. Upload toàn bộ nội dung ZIP lên GitHub, giữ đúng cấu trúc:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `static/index.html`
2. Render → New → Web Service → chọn repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy xong, mở URL Render và kiểm tra `/health`.

## Dùng Safari bookmarklet
1. Mở app Render V4.
2. Trong mục “Tạo nút chụp URL cho Safari”, dán URL Render và bấm Tạo bookmarklet.
3. Sao chép đoạn `javascript:...`.
4. Trong Safari, tạo một dấu trang bất kỳ; vào Sửa và thay trường địa chỉ bằng bookmarklet.
5. Mở link GTraffic trong Safari và tự hoàn tất CAPTCHA/bước xác minh hợp lệ.
6. Chạy dấu trang vừa tạo. App sẽ mở lại và hiển thị URL hiện tại của tab.

Lưu ý: bookmarklet là thao tác do người dùng chủ động chạy. iOS/Safari có thể hạn chế một số bookmarklet tùy phiên bản hoặc chính sách trang.
