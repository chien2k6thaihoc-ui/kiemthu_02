# Báo Cáo Cơ Chế Chờ và Kết Quả Kiểm Thử Tự Động Tuần 07

> **Chủ đề Tuần 07:** Giai đoạn 3 — Thực hành trên demo (Swag Labs Android)  
> **Nhóm thực hiện:** Nhóm A4  
> **Chức năng phân công:** Chức năng 2 — Đăng xuất qua menu (`test-Menu` -> `test-LOGOUT`)  
> **Thiết bị kiểm thử thực tế:** Honor Magic 6 Pro (BVL-AN00), Android 14, kết nối qua ADB (`ATLSVB4103012319`)

---

## 1. Lý do cần cơ chế chờ trong kiểm thử tự động ứng dụng di động

Trong ứng dụng di động thực tế (đặc biệt là ứng dụng React Native / Native như Swag Labs Mobile App), việc các phần tử UI xuất hiện ngay lập tức là không thể đảm bảo vì các yếu tố sau:

1. **Hiệu ứng chuyển động (UI Animation / Transition):**
   - Khi bấm vào nút Menu (`test-Menu`), menu điều hướng trượt từ cạnh trái màn hình sang phải (slide-in transition).
   - Trong quá trình animation đang chạy, các mục con như `test-LOGOUT` và `test-Close` chưa đạt trạng thái sẵn sàng để nhận tương tác chạm (clickable) hoặc chưa xuất hiện hoàn toàn trên cây phân cấp Accessibility / UiAutomator.
2. **Độ trễ render và xử lý bất đồng bộ (Render latency):**
   - Sau khi bấm `test-LOGIN`, ứng dụng cần gửi request xác thực, khởi tạo state và render màn hình danh sách sản phẩm `PRODUCTS`.
   - Sau khi bấm `test-LOGOUT`, ứng dụng xoá session/token, giải phóng bộ nhớ và render lại màn hình `test-Username`.
3. **Độ trễ truyền nhận lệnh của Appium / UiAutomator2 Server:**
   - Mỗi lệnh tìm kiếm phần tử từ Client (Python) gửi qua HTTP tới Appium Server, chuyển tiếp qua adb socket tới UiAutomator2 Server chạy trên Android.
   - Nếu không có cơ chế chờ, client sẽ query cây UI ngay tại thời điểm frame trước đó chưa cập nhật xong, dẫn đến ngoại lệ `NoSuchElementException` hoặc `StaleElementReferenceException`.

---

## 2. Vì sao TUYỆT ĐỐI TRÁNH dùng `time.sleep`?

`time.sleep(N)` là cơ chế chờ cưỡng bức (Hardcoded / Fixed Sleep):
- **Gây lãng phí thời gian khủng khiếp:** Nếu đặt `sleep(5)` nhưng máy mạnh render trong 0.5s, test case bị lãng phí 4.5s. Với bộ 100 test case, thời gian chạy tăng vọt hàng chục phút.
- **Dễ gây vỡ test (Flaky test):** Nếu đặt `sleep(2)` nhưng mạng chập chờn hoặc thiết bị lag mất 2.5s, test case sẽ crash ngay lập tức dù ứng dụng không có lỗi.
- **Không phản ánh trạng thái thực của UI:** `time.sleep` dừng luồng thực thi mù quáng mà không lắng nghe sự kiện DOM/Accessibility của hệ điều hành.

---

## 3. Bảng so sánh các cơ chế chờ trong Selenium / Appium

| Tiêu chí | `time.sleep(n)` | Implicit Wait (`implicitly_wait`) | Explicit Wait (`WebDriverWait` + `EC`) |
|---|---|---|---|
| **Cơ chế hoạt động** | Tạm dừng toàn bộ luồng Python cố định $n$ giây | Cấu hình mức driver, tự động lặp lại tìm kiếm phần tử cho đến khi hết timeout | Chờ có điều kiện cụ thể (hiển thị, bấm được, văn bản xuất hiện, biến mất...) |
| **Tính linh hoạt** | Không linh hoạt, thời gian cố định | Áp dụng toàn cục cho mọi lệnh `find_element` | Cực kỳ linh hoạt, áp dụng theo từng phần tử hoặc trạng thái cụ thể |
| **Tốc độ thực thi** | Rất chậm (luôn chờ đủ $n$ giây) | Nhanh hơn (tìm thấy là trả về ngay) | Tối ưu nhất (trả về ngay khi thoả mãn điều kiện `ExpectedCondition`) |
| **Độ tin cậy** | Kém (dễ flake khi máy chậm) | Trung bình (chỉ kiểm tra sự tồn tại trong DOM, không kiểm tra clickable) | **Cao nhất (Chuẩn kiểm thử chuyên nghiệp)** |

---

## 4. Thực nghiệm so sánh: Khi có chờ tường minh vs Khi không có chờ

### Kịch bản thực nghiệm
Mở màn hình chính `PRODUCTS` → Bấm nút `test-Menu` → Tìm và bấm nút `test-LOGOUT`.

```python
# KỊCH BẢN A: Không chờ (Implicit Wait = 0, không WebDriverWait)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu").click()
driver.implicitly_wait(0)
# Ngay lập tức tìm logout khi hiệu ứng mở menu chưa hoàn tất:
logout_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")
logout_btn.click()

# KỊCH BẢN B: Chờ tường minh (WebDriverWait + EC)
menu_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-Menu")))
menu_btn.click()
logout_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")))
logout_btn.click()
```

### Bảng kết quả thực nghiệm

| Trường hợp | Thời gian thực thi | Lỗi xảy ra | Tỉ lệ thành công | Đánh giá |
|---|---|---|---|---|
| **Không chờ (`timeout = 0`)** | < 0.1s sau khi bấm menu | `NoSuchElementException` / `ElementNotInteractableException` (do menu chưa mở xong hoặc đang animation) | 0% – 30% (tuỳ độ tải CPU của thiết bị) | ❌ Không ổn định, test case thường xuyên fail |
| **Dùng `time.sleep(3)`** | Cố định 3.0s | Không có lỗi logic nhưng phí 2.2s vô ích | 100% | ⚠️ Chậm chạp, lãng phí tài nguyên CI/CD |
| **Dùng `WebDriverWait` (15s)** | **0.4s – 0.8s** (phản hồi ngay khi menu render xong) | Không có lỗi | **100%** | ✅ **Nhanh nhất, an toàn và chuyên nghiệp nhất** |

---

## 5. Kết quả thực thi bộ test case Tuần 07 trên thiết bị thật

Bộ kiểm thử được viết tại `tuan-07/test_dang_xuat.py` đã được chạy thực tế trên thiết bị Android:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Projects\kiemthu_02
plugins: anyio-4.15.1, platformdirs-4.13.0
collected 3 items

tuan-07/test_dang_xuat.py::test_logout_success PASSED                    [ 33%]
tuan-07/test_dang_xuat.py::test_relogin_after_logout PASSED              [ 66%]
tuan-07/test_dang_xuat.py::test_cancel_logout_via_close_button PASSED    [100%]

============================= 3 passed in 54.84s ==============================
```

### Chi tiết các test case:
1. **`test_logout_success` (TC-07-01):**
   - Đăng nhập vào màn hình `PRODUCTS`.
   - Bấm `test-Menu`, chờ tường minh cho đến khi `test-LOGOUT` hiển thị và bấm được.
   - Bấm `test-LOGOUT`, chờ màn hình quay lại ô `test-Username`.
   - Lưu ảnh bằng chứng: `tuan-07/anh/tc01_logout_thanh_cong.png`.
2. **`test_relogin_after_logout` (TC-07-02):**
   - Đăng xuất thành công, sau đó tái đăng nhập bằng `standard_user` / `secret_sauce`.
   - Chờ tường minh `PRODUCTS` hiển thị. Đảm bảo session được dọn dẹp sạch và tái sử dụng tốt.
   - Lưu ảnh bằng chứng: `tuan-07/anh/tc02_relogin_sau_logout.png`.
3. **`test_cancel_logout_via_close_button` (TC-07-03 - Negative/Cancel flow):**
   - Mở menu nhưng người dùng đổi ý bấm nút Đóng `test-Close`.
   - Chờ menu đóng và kiểm tra người dùng vẫn duy trì phiên làm việc tại màn hình `PRODUCTS`.
   - Lưu ảnh bằng chứng: `tuan-07/anh/tc03_cancel_logout.png`.

---

## 6. Khuyến nghị áp dụng

1. **Luôn sử dụng `WebDriverWait` kết hợp `expected_conditions`:**
   - Đối với phần tử cần tương tác (Click, Tap): Dùng `EC.element_to_be_clickable`.
   - Đối với phần tử cần đọc dữ liệu hoặc xác nhận màn hình: Dùng `EC.visibility_of_element_located`.
   - Đối với phần tử cần biến mất (như loading spinner, menu đóng): Dùng `EC.invisibility_of_element_located`.
2. **Đặt timeout hợp lý:**
   - Khuyến nghị từ 10s đến 15s cho ứng dụng mobile trên thiết bị thật, đủ để xử lý mạng chậm nhưng không làm treo test quá lâu nếu có bug thực sự.
3. **Tách biệt dữ liệu kiểm thử (Fixtures):**
   - Dùng lệnh ADB `pm clear com.swaglabsmobileapp` trước và sau mỗi test case để đảm bảo mỗi lần chạy là một phiên hoàn toàn sạch sẽ, không bị ảnh hưởng bởi cache của bài test trước.
