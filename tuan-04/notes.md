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