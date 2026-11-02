# Test Cases — Tuần 05: Chức năng Đăng nhập (Swag Labs, Android)

> **Quy trình bắt buộc của đề bài:** file này được viết **TRƯỚC khi viết code** (`tuan-05/test_login.py`).
> Nguồn yêu cầu: sheet *Timeline* hàng 26 (W05) và sheet *Phân công team* (mục Tuần 5, nhóm App).
> Đối tượng kiểm thử: ứng dụng **Swag Labs** (Android) — package `com.swaglabsmobileapp`.

---

## Thông tin chung

| Mục | Giá trị | Nguồn |
|---|---|---|
| Ứng dụng | Swag Labs (Android) | sheet Timeline hàng 2 |
| Package | `com.swaglabsmobileapp` | `tuan-04/test_smoke.py` |
| Activity | `com.swaglabsmobileapp.MainActivity` | `tuan-04/test_smoke.py` |
| Thiết bị | Điện thoại Android thật, serial `ATLSVB4103012319` (model BVL-AN00) | `tuan-04/test_smoke.py`, `tuan-04/notes.md`, Windows USB `VID_339B&PID_107D` |
| Công cụ | Appium 2 + UiAutomator2 driver + pytest | sheet Phân công team |
| Locator dùng chung | Ô Username: accessibility id `test-Username`; ô Password/nút LOGIN/thông báo lỗi: tìm bằng Appium Inspector, ghi ở cuối file | `tuan-04/test_smoke.py` |

**Tài khoản dùng để kiểm thử** (nguồn: sheet Phân công team, mục Tuần 5 – nhóm App):

| Tài khoản | Mật khẩu | Kết quả mong đợi |
|---|---|---|
| `standard_user` | `secret_sauce` | Vào được màn **Products** |
| `locked_out_user` | `secret_sauce` | Báo tài khoản bị khoá |
| `standard_user` | *(bỏ trống)* | Báo `Password is required` |

---

## TC-05-01 — Đăng nhập thành công với tài khoản hợp lệ

| Trường | Nội dung |
|---|---|
| **Mã test case** | TC-05-01 |
| **Tên** | Đăng nhập thành công bằng `standard_user` |
| **Mục đích** | Kiểm tra người dùng hợp lệ đăng nhập được và vào đúng màn hình chính |
| **Điều kiện trước** | App Swag Labs đã cài trên thiết bị; app đang ở màn hình đăng nhập; Appium server chạy ở `127.0.0.1:4723` |

**Các bước thực hiện**

1. Mở ứng dụng Swag Labs (khởi tạo phiên Appium với `appPackage`/`appActivity` như `test_smoke.py`).
2. Chờ ô nhập **Username** hiển thị.
3. Nhập vào ô Username: `standard_user`.
4. Nhập vào ô **Password**: `secret_sauce`.
5. Bấm nút **LOGIN**.
6. Chờ màn hình **Products** xuất hiện.

**Dữ liệu nhập:** Username = `standard_user`; Password = `secret_sauce`

**Kết quả mong đợi:** Màn hình **Products** hiển thị (có tiêu đề "PRODUCTS" / danh sách sản phẩm); không có thông báo lỗi.

**Kết quả thực tế:** Màn hình Products hiển thị thành công với tiêu đề "PRODUCTS". Đã chụp ảnh `anh/tc01_login_success.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

## TC-05-02 — Đăng nhập thất bại với tài khoản bị khoá

| Trường | Nội dung |
|---|---|
| **Mã test case** | TC-05-02 |
| **Tên** | Đăng nhập thất bại bằng `locked_out_user` |
| **Mục đích** | Kiểm tra hệ thống chặn tài khoản bị khoá và hiển thị thông báo phù hợp |
| **Điều kiện trước** | App đang ở màn hình đăng nhập |

**Các bước thực hiện**

1. Mở ứng dụng Swag Labs (phiên Appium mới).
2. Chờ ô nhập **Username** hiển thị.
3. Nhập vào ô Username: `locked_out_user`.
4. Nhập vào ô **Password**: `secret_sauce`.
5. Bấm nút **LOGIN**.
6. Chờ thông báo lỗi xuất hiện.
7. Đọc nội dung thông báo lỗi.

**Dữ liệu nhập:** Username = `locked_out_user`; Password = `secret_sauce`

**Kết quả mong đợi:** Hiển thị thông báo tài khoản bị khoá (nội dung tiếng Anh, Swag Labs hiển thị: *"Sorry, this user has been locked out."*), **không** vào được màn Products.

**Kết quả thực tế:** Ứng dụng không chuyển màn hình, hiển thị thông báo chính xác: "Sorry, this user has been locked out.". Đã chụp ảnh `anh/tc02_locked_out_user.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

## TC-05-03 — Đăng nhập thất bại khi bỏ trống mật khẩu

| Trường | Nội dung |
|---|---|
| **Mã test case** | TC-05-03 |
| **Tên** | Đăng nhập thất bại khi bỏ trống mật khẩu |
| **Mục đích** | Kiểm tra hệ thống bắt lỗi bắt buộc nhập mật khẩu |
| **Điều kiện trước** | App đang ở màn hình đăng nhập |

**Các bước thực hiện**

1. Mở ứng dụng Swag Labs (phiên Appium mới).
2. Chờ ô nhập **Username** hiển thị.
3. Nhập vào ô Username: `standard_user`.
4. **Bỏ trống** ô Password (không nhập gì).
5. Bấm nút **LOGIN**.
6. Chờ thông báo lỗi xuất hiện.
7. Đọc nội dung thông báo lỗi.

**Dữ liệu nhập:** Username = `standard_user`; Password = *(bỏ trống)*

**Kết quả mong đợi:** Hiển thị thông báo `Password is required`; **không** vào được màn Products.

**Kết quả thực tế:** Ứng dụng hiển thị thông báo chính xác: "Password is required". Đã chụp ảnh `anh/tc03_empty_password.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

## Bảng locator (xác minh bằng Appium Inspector / UI Hierarchy Dump)

Theo yêu cầu W05, locator phải được tìm bằng **Appium Inspector** (hoặc DevTools cho Web), không được đoán.

| Phần tử | Locator | Chiến lược | Đã xác minh? |
|---|---|---|---|
| Ô Username | `test-Username` (accessibility id) | `AppiumBy.ACCESSIBILITY_ID` | ✅ Đã xác minh |
| Ô Password | `test-Password` (accessibility id) | `AppiumBy.ACCESSIBILITY_ID` | ✅ Đã xác minh |
| Nút LOGIN | `test-LOGIN` (accessibility id) | `AppiumBy.ACCESSIBILITY_ID` | ✅ Đã xác minh |
| Thông báo lỗi | `test-Error message` (ViewGroup chứa `android.widget.TextView`) | `AppiumBy.ACCESSIBILITY_ID` + `TextView` | ✅ Đã xác minh |
| Màn Products (xác nhận đăng nhập thành công) | `//*[@text='PRODUCTS']` | `AppiumBy.XPATH` | ✅ Đã xác minh |

**Lý do ưu tiên accessibility id trên Android** (câu hỏi phần đọc W05 – UiAutomator2 driver README): accessibility id do nhà phát triển đặt và gắn với mục đích của phần tử, **ổn định hơn** so với XPath theo vị trí trong cây giao diện — XPath kiểu `/hierarchy/android.widget.FrameLayout/...` sẽ vỡ ngay khi app đổi bố cục hoặc thêm/bớt phần tử.
