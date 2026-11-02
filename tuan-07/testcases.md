# Danh sách Ca kiểm thử Tuần 07 — Chức năng 2: Đăng xuất qua Menu (Swag Labs, Android)

> **Tuần 07 — Giai đoạn 3: Thực hành trên demo**  
> Đối tượng kiểm thử: **Ứng dụng di động Swag Labs (Android Native App)**  
> Gói ứng dụng (Package): `com.swaglabsmobileapp`  
> Activity khởi chạy: `com.swaglabsmobileapp.MainActivity`  
> Phân công chức năng: **Nhóm A4 — Chức năng 2: Đăng xuất qua menu**  
> Yêu cầu kỹ thuật: **KHÔNG dùng `time.sleep`**, sử dụng cơ chế chờ tường minh (`WebDriverWait`), có ít nhất 1 trường hợp sai/ngoại lệ.

---

## 1. Bảng tổng hợp ca kiểm thử

| Mã test case | Tên ca kiểm thử | Loại kiểm thử | Mục đích kiểm tra | Kết quả mong đợi | Trạng thái |
|---|---|---|---|---|---|
| **TC-07-01** | Đăng xuất thành công qua menu | Dương tính (Positive) | Kiểm tra luồng đăng xuất chuẩn qua side menu | Ứng dụng kết thúc phiên làm việc, trở về màn hình Đăng nhập | ✅ Đạt (PASSED) |
| **TC-07-02** | Đăng nhập lại sau khi đăng xuất | Dương tính (Positive) | Kiểm tra tính tái sử dụng và giải phóng session sau đăng xuất | Đăng nhập lại thành công với tài khoản chuẩn, hiển thị màn hình PRODUCTS | ✅ Đạt (PASSED) |
| **TC-07-03** | Mở menu và huỷ đăng xuất (bấm nút Đóng) | Luồng ngoại lệ / Huỷ bỏ (Negative) | Kiểm tra việc người dùng mở menu nhưng huỷ thao tác đăng xuất | Menu đóng lại an toàn, người dùng vẫn ở lại màn hình PRODUCTS, phiên không bị huỷ | ✅ Đạt (PASSED) |

---

## 2. Chi tiết từng ca kiểm thử

### TC-07-01 — Đăng xuất thành công qua side menu

| Trường thông tin | Chi tiết |
|---|---|
| **Mã test case** | TC-07-01 |
| **Tên test case** | Đăng xuất thành công qua side menu |
| **Chức năng** | Chức năng 2 — Đăng xuất qua menu (Team A4) |
| **Mục đích** | Đảm bảo người dùng sau khi đăng nhập có thể mở side menu và chọn mục LOGOUT để kết thúc phiên an toàn |
| **Điều kiện tiên quyết** | App Swag Labs đã khởi chạy, thiết bị đã kết nối ADB, người dùng đã đăng nhập thành công vào màn hình PRODUCTS |

**Các bước thực hiện:**
1. Khởi tạo phiên kết nối Appium với ứng dụng Swag Labs.
2. Đăng nhập với tài khoản hợp lệ (`standard_user` / `secret_sauce`).
3. Chờ tường minh cho tới khi màn hình chính `PRODUCTS` xuất hiện.
4. Bấm vào biểu tượng Menu (`test-Menu` ở góc trên bên trái).
5. Chờ tường minh cho tới khi danh sách menu xuất hiện và mục `LOGOUT` (`test-LOGOUT`) hiển thị trên màn hình.
6. Bấm vào mục `LOGOUT`.
7. Chờ tường minh cho màn hình đăng nhập hiển thị trở lại (kiểm tra ô nhập `test-Username`).
8. Chụp ảnh màn hình làm bằng chứng kiểm thử.

**Dữ liệu đầu vào:**
- Tài khoản: `standard_user` / `secret_sauce`.
- Thao tác: Bấm `test-Menu` → Bấm `test-LOGOUT`.

**Kết quả mong đợi:**
- Ứng dụng chuyển hướng về màn hình đăng nhập ban đầu.
- Ô nhập tên đăng nhập `test-Username` và nút `test-LOGIN` hiển thị rõ ràng.

**Kết quả thực tế:**
- Màn hình đăng nhập hiển thị chính xác sau khi bấm LOGOUT.
- Đã lưu ảnh bằng chứng `tuan-07/anh/tc01_logout_thanh_cong.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

### TC-07-02 — Đăng nhập lại sau khi đã đăng xuất

| Trường thông tin | Chi tiết |
|---|---|
| **Mã test case** | TC-07-02 |
| **Tên test case** | Đăng nhập lại sau khi đã đăng xuất |
| **Chức năng** | Chức năng 2 — Đăng xuất qua menu (Team A4) |
| **Mục đích** | Đảm bảo tính toàn vẹn của ứng dụng: sau khi đăng xuất, hệ thống không bị treo hoặc rò rỉ trạng thái, người dùng có thể tái đăng nhập bình thường |
| **Điều kiện tiên quyết** | Đã thực hiện đăng xuất thành công về màn hình đăng nhập |

**Các bước thực hiện:**
1. Thực hiện luồng đăng nhập và đăng xuất thành công (như TC-07-01).
2. Tại màn hình đăng nhập, nhập lại ô `test-Username`: `standard_user`.
3. Nhập lại ô `test-Password`: `secret_sauce`.
4. Bấm nút `test-LOGIN`.
5. Chờ tường minh cho tiêu đề màn hình `PRODUCTS` xuất hiện.
6. Xác nhận tiêu đề `PRODUCTS` hiển thị.
7. Chụp ảnh màn hình làm bằng chứng kiểm thử.

**Dữ liệu đầu vào:**
- Tài khoản tái đăng nhập: `standard_user` / `secret_sauce`.

**Kết quả mong đợi:**
- Đăng nhập lại thành công, màn hình `PRODUCTS` hiển thị bình thường.

**Kết quả thực tế:**
- Ứng dụng cho phép đăng nhập lại mượt mà, không gặp lỗi phiên cũ hay xung đột token.
- Đã lưu ảnh bằng chứng `tuan-07/anh/tc02_relogin_sau_logout.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

### TC-07-03 — Mở menu và huỷ đăng xuất bằng cách bấm nút Đóng (Cancel/Negative Flow)

| Trường thông tin | Chi tiết |
|---|---|
| **Mã test case** | TC-07-03 |
| **Tên test case** | Mở menu và huỷ đăng xuất bằng cách bấm nút Đóng |
| **Chức năng** | Chức năng 2 — Đăng xuất qua menu (Team A4) |
| **Mục đích** | Kiểm tra trường hợp người dùng mở menu nhưng thay đổi ý định (không muốn đăng xuất), bấm nút Close `test-Close`. Ứng dụng phải đóng menu, giữ nguyên phiên làm việc và không được đăng xuất nhầm người dùng |
| **Điều kiện tiên quyết** | Đang ở màn hình `PRODUCTS` sau khi đăng nhập |

**Các bước thực hiện:**
1. Đăng nhập vào ứng dụng và vào màn hình `PRODUCTS`.
2. Bấm vào nút Menu (`test-Menu`) để mở menu trượt ra.
3. Chờ nút Đóng (`test-Close`) và mục `LOGOUT` hiển thị.
4. Bấm nút Đóng (`test-Close`) để huỷ thao tác trong menu.
5. Chờ tường minh cho menu ẩn đi và danh sách sản phẩm `PRODUCTS` tương tác lại được.
6. Xác nhận người dùng vẫn đang ở màn hình `PRODUCTS`, không bị chuyển về màn hình đăng nhập (ô `test-Username` không tồn tại hoặc không hiển thị).
7. Chụp ảnh màn hình làm bằng chứng kiểm thử.

**Dữ liệu đầu vào:**
- Bấm `test-Menu` → Bấm `test-Close`.

**Kết quả mong đợi:**
- Menu được đóng lại, ứng dụng vẫn giữ nguyên trạng thái đăng nhập, tiêu đề `PRODUCTS` vẫn hiển thị.

**Kết quả thực tế:**
- Menu đóng thành công, ứng dụng giữ nguyên trạng thái làm việc tại màn hình PRODUCTS.
- Đã lưu ảnh bằng chứng `tuan-07/anh/tc03_cancel_logout.png`.

**Trạng thái:** ✅ Đạt (PASSED)

---

## 3. Bảng tra cứu phần tử định vị (Locators đã xác minh)

Tất cả các định vị dưới đây đều đã được xác minh bằng `driver.page_source` và dump UI thực tế từ thiết bị thật qua Appium:

| Tên phần tử | Chiến lược định vị | Giá trị Locator | Mục đích tương tác | Trạng thái xác minh |
|---|---|---|---|---|
| Ô Tên đăng nhập | `AppiumBy.ACCESSIBILITY_ID` | `test-Username` | Nhập tên tài khoản | ✅ Đã xác minh |
| Ô Mật khẩu | `AppiumBy.ACCESSIBILITY_ID` | `test-Password` | Nhập mật khẩu | ✅ Đã xác minh |
| Nút LOGIN | `AppiumBy.ACCESSIBILITY_ID` | `test-LOGIN` | Bấm đăng nhập | ✅ Đã xác minh |
| Tiêu đề PRODUCTS | `AppiumBy.XPATH` | `//*[@text='PRODUCTS']` | Kiểm tra vào màn hình chính | ✅ Đã xác minh |
| Nút Mở Menu | `AppiumBy.ACCESSIBILITY_ID` | `test-Menu` | Bấm để mở menu trượt trái | ✅ Đã xác minh |
| Mục LOGOUT | `AppiumBy.ACCESSIBILITY_ID` | `test-LOGOUT` | Bấm để đăng xuất | ✅ Đã xác minh |
| Nút Đóng Menu | `AppiumBy.ACCESSIBILITY_ID` | `test-Close` | Bấm để đóng menu | ✅ Đã xác minh |
