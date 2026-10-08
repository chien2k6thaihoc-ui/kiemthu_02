# Ghi chú Tuần 04 - Smoke Test Mobile App

## 1. Trả lời câu hỏi đọc trước buổi học
- **Quy tắc tìm bài kiểm thử của pytest**: [Inference] pytest tự động tìm các file có tiền tố `test_*.py` hoặc hậu tố `*_test.py`, chứa các hàm có tiền tố `test_*`.
- **Mô hình hoạt động Appium**: 
  - Appium Client (code Python): Chạy trên máy tính gửi lệnh WebDriver.
  - Appium Server: Lắng nghe tại cổng 4723, chuyển đổi lệnh tới driver.
  - UiAutomator2 Driver: Chạy trên thiết bị Android, thao tác trực tiếp với giao diện.
- **Cấu hình thiết bị**: Sử dụng điện thoại Android thật (Model: BVL-AN00) qua USB Debugging.
- **Cách cài đặt APK**: Sử dụng lệnh `adb install <duong_dan_apk>`.

## 2. Các lỗi cài đặt đã gặp và cách xử lý
- **Lỗi 1**: `adb` không được nhận diện trong PowerShell (`The term 'adb' is not recognized`).
  - *Cách xử lý*: Thêm đường dẫn `platform-tools` vào biến môi trường `Path`.
- **Lỗi 2**: Appium Server báo thiếu `ANDROID_HOME` (`Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported`).
  - *Cách xử lý*: Khai báo biến môi trường `ANDROID_HOME` trỏ tới Android SDK và khởi động lại Appium server.

## 3. Thử nghiệm cố tình gây lỗi (Intentional Failure)
- **Thao tác**: Đổi locator của trường nhập liệu từ `test-Username` thành `test-Username-sai`.
- **Hiện tượng**: Báo lỗi `NoSuchElementException`.
- **Khôi phục**: Đổi lại `test-Username`, kết quả kiểm thử trở lại trạng thái `PASSED`.

---

## 4. Phần viết của thành viên

> **Khung do agent soạn ngày 2026-10-08 — chưa phải nội dung hoàn chỉnh.**
> **Phạm vi:** theo yêu cầu của Dũng ngày 2026-10-08, bài nộp W04 này **chỉ cần phần viết của Dũng**.
> (Yêu cầu gốc của môn là "phần viết của *mọi* thành viên"; phần của Chiến và Toàn nếu cần bổ sung thì lấy lại khung từ lịch sử commit.)
> **Dũng tự thay các dòng `_(...)_` bằng lời của mình** — agent không được viết thay.

### 4.1 Dũng

- **Điều đã học:** _(Dũng tự viết 2–3 dòng)_
- **Trả lời 1–2 câu hỏi phần đọc** *(nhóm App)*:
  - Vì sao trên điện thoại nên ưu tiên **accessibility id**? → _(tự trả lời)_
  - pytest tự tìm bài kiểm thử dựa vào quy tắc đặt tên nào? → _(tự trả lời)_
- **Lỗi đã gặp khi cài đặt + cách sửa:** _(tự ghi; có thể bổ sung cho mục 2 ở trên)_
- **Phản tư AI** *(nếu có dùng AI)*:
  - Đã hỏi AI điều gì: _(...)_
  - Câu trả lời của AI có đúng không: _(...)_
  - Mình hiểu thêm được gì: _(...)_

---

## 5. Việc còn lại để W04 đủ điều kiện đạt

- [x] `tuan-04/test_smoke.py` — có, chú thích tiếng Việt, đã chạy PASS (xem ảnh `anh/passed.jpg`).
- [x] **`tuan-04/anh/`** — `passed.jpg` + `fail.jpg` **là ảnh chụp trên máy của Dũng** (Dũng xác nhận 2026-10-08); giữ nguyên, không xoá/ghi đè.
- [x] `README.md` — hướng dẫn cài đặt + câu lệnh chạy (đã viết ngày 2026-10-08).
- [ ] **Mục 4.1 ở trên: Dũng tự điền phần viết + phản tư AI** (hiện còn là khung `_(...)_`).
- [ ] Commit phần bổ sung lên nhánh `week-04` rồi gộp `main`.
