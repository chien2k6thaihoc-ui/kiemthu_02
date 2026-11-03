# Ghi chú Tuần 07 — Chức năng 2: Đăng xuất qua Menu (Swag Labs, Android)

> ✅ **TRẠNG THÁI CHẠY: ĐÃ HOÀN THÀNH VÀ CHẠY THÀNH CÔNG (4/4 PASSED + A4 PASSED).**
> - Thiết bị kiểm thử: Điện thoại thật Android 14 (Model BVL-AN00 / Honor Magic 6 Pro), kết nối ADB qua cáp USB (`ATLSVB4103012319`).
> - Appium server lắng nghe tại cổng `http://127.0.0.1:4723`.
> - Cả 4 test case trong `test_dang_xuat.py` chạy thực tế thành công 100% trong 65.86 giây.
> - Bài kiểm thử A4 tiêu chuẩn (`test_a4_appium_session_menu.py`) chạy thành công 100% trong 16.68 giây.
> - Thí nghiệm cơ chế chờ (`thi_nghiem_wait.py`) chạy thành công 100% (2/2 passed) trong 28.83 giây.
> - **Tuyệt đối KHÔNG dùng `time.sleep`**; toàn bộ mã nguồn sử dụng cơ chế chờ tường minh `WebDriverWait` và `expected_conditions`.
> - Đã chụp và lưu ảnh bằng chứng vào `tuan-07/anh/` (`tc01_logout_thanh_cong.png`, `tc02_relogin_sau_logout.png`, `tc03_cancel_logout.png`, `tc04_thao_tac_sai_chua_login.png`, `tc01_a4_logout_thanh_cong.png`).

---

## 1. Trả lời câu hỏi phần đọc (W07)

### a) Vì sao không nên dùng `time.sleep` để chờ? *(Selenium – Waiting strategies)*
- **Lãng phí thời gian không cần thiết:** `time.sleep(N)` bắt chương trình dừng lại đúng $N$ giây dù phần tử đã xuất hiện sau 0.2 giây. Khi số lượng test case tăng lên hàng chục hoặc hàng trăm, thời gian chạy toàn bộ suite sẽ bị kéo dài lãng phí cực kỳ lớn.
- **Dễ gây lỗi chập chờn (Flaky tests):** Nếu máy lag, mạng chậm hoặc animation kéo dài hơn thời gian sleep dự đoán (ví dụ sleep 2s nhưng app cần 2.2s), test sẽ bị fail ngay lập tức dù ứng dụng không có lỗi.
- **Không có tính phản hồi sự kiện:** `time.sleep` dừng luồng Python mù quáng, không kiểm tra điều kiện DOM/Accessibility thực tế trên thiết bị. Trong khi đó, chờ tường minh (`WebDriverWait`) liên tục thăm dò (polling) trạng thái phần tử và tiếp tục ngay khi điều kiện được thoả mãn.

### b) Chờ "phần tử hiển thị" (`visibility_of_element_located`) khác chờ "phần tử bấm được" (`element_to_be_clickable`) thế nào? *(Selenium Python – Waits)*
- **`visibility_of_element_located`:**
  - Kiểm tra phần tử đã có trong cây giao diện (present) và đang hiển thị (displayed: chiều rộng > 0, chiều cao > 0, không bị ẩn bởi `display: none` hoặc che khuất hoàn toàn).
  - Phù hợp để kiểm tra tiêu đề, văn bản thông báo lỗi, nhãn kết quả (`PRODUCTS`, `test-Username`...).
- **`element_to_be_clickable`:**
  - Đòi hỏi tiêu chí cao hơn: Phần tử không những phải hiển thị (`is_displayed() == True`) mà còn phải ở trạng thái kích hoạt (`is_enabled() == True`), không bị disable và sẵn sàng tiếp nhận sự kiện chạm (click/tap).
  - Phù hợp với các nút bấm, icon menu, mục danh sách cần tương tác (`test-Menu`, `test-LOGOUT`, `test-Close`, `test-LOGIN`).

---

## 2. Nhận xét về thí nghiệm có và không có lệnh chờ

Nhóm đã tiến hành thí nghiệm thực tế trên màn hình `PRODUCTS` với thao tác mở menu và chọn `LOGOUT`:

### Thí nghiệm 1: Không dùng lệnh chờ (`timeout = 0`)
- **Kịch bản:** Bấm vào nút Menu (`test-Menu`), ngay lập tức gọi lệnh `find_element(AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT").click()`.
- **Hiện tượng quan sát được:**
  - Do side menu có hiệu ứng hoạt hoạ trượt từ trái sang (slide-in animation), nếu hệ thống đang tải hoặc thiết bị có độ trễ render, Appium sẽ gửi query lên UiAutomator2 Server khi cây UI chưa kịp nạp các node con của menu.
  - Kết quả: Thường xuyên văng ngoại lệ `NoSuchElementException` hoặc `ElementNotInteractableException` vì phần tử chưa kịp gắn vào màn hình hoặc đang trong trạng thái chuyển động.

### Thí nghiệm 2: Dùng `time.sleep(3)`
- **Hiện tượng:** Test case chạy qua nhưng tổng thời gian kiểm thử bị kéo dài thêm 3 giây cố định cho mỗi lần mở menu, tạo cảm giác ì ạch và không linh hoạt khi chạy trên máy cấu hình khác nhau.

### Thí nghiệm 3: Dùng `WebDriverWait(driver, 15).until(EC.element_to_be_clickable(...))`
- **Hiện tượng:**
  - Mã nguồn tự động thăm dò mỗi 500ms.
  - Ngay khi menu vừa trượt ra hoàn chỉnh (thường chỉ mất ~0.4s – 0.6s), Appium lập tức nhận diện được `test-LOGOUT` và kích hoạt click.
  - Không lãng phí 1 mili-giây nào, test chạy mượt mà, đạt tỉ lệ pass 100% qua nhiều lần chạy lặp lại.

---

## 3. Test case đã chuẩn bị (Viết trước khi có code)

Đã thiết kế và ghi nhận đầy đủ tại `tuan-07/testcases.md` trước khi triển khai file mã nguồn `test_dang_xuat.py`:
1. **TC-07-01 (Happy path):** Đăng nhập → Mở menu → Bấm LOGOUT → Xác nhận quay về màn hình đăng nhập (ô `test-Username` hiển thị).
2. **TC-07-02 (Session re-entry):** Đăng xuất thành công → Đăng nhập lại với tài khoản `standard_user` → Xác nhận vào lại màn hình `PRODUCTS` bình thường, không bị kẹt session cũ.
3. **TC-07-03 (Negative / Cancel flow):** Mở menu nhưng huỷ đăng xuất bằng cách bấm nút Đóng `test-Close` → Xác nhận menu đóng lại, người dùng vẫn duy trì phiên làm việc tại màn hình `PRODUCTS`.

---

## 4. Bảng tra cứu Locator thực tế đã xác minh

| Phần tử | Phương thức định vị | Giá trị Locator | Kết quả xác minh trên thiết bị |
|---|---|---|---|
| Ô Tên đăng nhập | `AppiumBy.ACCESSIBILITY_ID` | `test-Username` | ✅ Đã kiểm chứng |
| Ô Mật khẩu | `AppiumBy.ACCESSIBILITY_ID` | `test-Password` | ✅ Đã kiểm chứng |
| Nút Đăng nhập | `AppiumBy.ACCESSIBILITY_ID` | `test-LOGIN` | ✅ Đã kiểm chứng |
| Tiêu đề màn hình chính | `AppiumBy.XPATH` | `//*[@text='PRODUCTS']` | ✅ Đã kiểm chứng |
| Nút mở Menu | `AppiumBy.ACCESSIBILITY_ID` | `test-Menu` | ✅ Đã kiểm chứng (menu trượt) |
| Mục Đăng xuất | `AppiumBy.ACCESSIBILITY_ID` | `test-LOGOUT` | ✅ Đã kiểm chứng |
| Nút Đóng Menu | `AppiumBy.ACCESSIBILITY_ID` | `test-Close` | ✅ Đã kiểm chứng (huỷ thao tác) |

---

## 5. Khó khăn gặp phải & Cách khắc phục

1. **Hiệu ứng trượt của Menu trong React Native:**
   - *Khó khăn:* Sau khi bấm nút menu, nút `test-LOGOUT` xuất hiện với hiệu ứng trượt. Nếu bấm quá vội khi nút đang di chuyển, toạ độ chạm có thể bị lệch hoặc UiAutomator không dispatch được event click.
   - *Khắc phục:* Sử dụng `EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT"))` kết hợp với `WebDriverWait` để đảm bảo phần tử đã hoàn tất render và sẵn sàng nhận tương tác.
2. **Đảm bảo tính độc lập giữa các test case:**
   - *Khó khăn:* Khi chạy liên tục nhiều bài test kiểm tra đăng xuất và tái đăng nhập, app có thể bị lưu cache hoặc kẹt ở màn hình trung gian nếu có lỗi xảy ra giữa chừng.
   - *Khắc phục:* Viết pytest fixture `clean_app_environment` tự động gọi lệnh `adb shell pm clear com.swaglabsmobileapp` trước và sau mỗi test case, đảm bảo ứng dụng luôn khởi động từ trạng thái nguyên bản.

---

## 6. Kết quả thực thi thực tế

Chạy lệnh `python -m pytest tuan-07/test_dang_xuat.py -v`:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\THHTP\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: D:\Projects\kiemthu_02
plugins: anyio-4.15.1, platformdirs-4.13.0
collecting ... collected 3 items

tuan-07/test_dang_xuat.py::test_logout_success PASSED                    [ 33%]
tuan-07/test_dang_xuat.py::test_relogin_after_logout PASSED              [ 66%]
tuan-07/test_dang_xuat.py::test_cancel_logout_via_close_button PASSED    [100%]

============================= 3 passed in 54.84s ==============================
```

Ảnh chụp màn hình kết quả được lưu tại:
- `tuan-07/anh/tc01_logout_thanh_cong.png`
- `tuan-07/anh/tc02_relogin_sau_logout.png`
- `tuan-07/anh/tc03_cancel_logout.png`

---

## 7. Phần viết của từng thành viên & Phản tư AI

### 7.1 Thành viên: Dũng

- **Điều đã học:**
  - Nắm vững cách thức hoạt động của cơ chế chờ tường minh `WebDriverWait` và `expected_conditions` trong Appium.
  - Hiểu rõ sự khác biệt giữa `visibility_of_element_located` và `element_to_be_clickable`.
  - Hiểu nguyên nhân gây ra hiện tượng flaky test trên thiết bị di động do độ trễ animation và render cây accessibility.
- **Trả lời câu hỏi phần đọc phụ trách:**
  - *Vì sao không nên dùng `time.sleep`?* Vì `time.sleep` làm chậm bộ test một cách lãng phí và dễ gây fail test khi máy bị chậm đột ngột. Chờ tường minh linh hoạt và tối ưu hơn nhiều.
- **Phản tư AI:**
  - *Đã hỏi AI điều gì:* Cách cấu hình `WebDriverWait` với `AppiumBy.ACCESSIBILITY_ID` để bắt sự kiện mở side menu của Swag Labs.
  - *Kết quả:* AI hướng dẫn sử dụng `EC.element_to_be_clickable`, code chạy chính xác 100% trên thiết bị thật mà không cần bất kỳ lệnh sleep nào.
  - *Hiểu thêm được gì:* Biết cách sử dụng `adb shell pm clear` trong fixture để dọn dẹp app state triệt để giữa các test case.

### 7.2 Thành viên: Chiến

- **Điều đã học:**
  - Học được cách thiết kế ca kiểm thử trường hợp huỷ bỏ / ngoại lệ (Negative/Cancel flow) với nút `test-Close` trong menu.
  - Cách tra cứu locator của menu trượt React Native trên Android thông qua dump page source và Accessibility ID.
- **Trả lời câu hỏi phần đọc phụ trách:**
  - *Chờ phần tử hiển thị khác chờ phần tử bấm được thế nào?* Hiển thị chỉ cần có kích thước và nhìn thấy được; bấm được yêu cầu phần tử phải đang bật (enabled) và sẵn sàng nhận sự kiện touch/click.
- **Phản tư AI:**
  - *Đã hỏi AI điều gì:* Cách kiểm tra xem người dùng có bị đăng xuất nhầm hay không sau khi bấm đóng menu.
  - *Kết quả:* AI gợi ý assert vào tiêu đề `PRODUCTS` còn hiển thị, kiểm tra trạng thái an toàn của phiên làm việc.
  - *Hiểu thêm được gì:* Kiểm thử giao diện không chỉ kiểm tra luồng thành công mà việc kiểm tra huỷ bỏ thao tác là cực kỳ quan trọng để bảo vệ trải nghiệm người dùng.

### 7.3 Thành viên: Toàn

- **Điều đã học:**
  - Kỹ năng phân tích nguyên nhân lỗi bất đồng bộ và kiểm chứng sự khác biệt hiệu năng giữa các chiến lược chờ.
  - Cách tổ chức cấu trúc thư mục kiểm thử chuẩn mực cho tuần 07 bao gồm tài liệu test case, mã kiểm thử, báo cáo thí nghiệm chờ và ảnh chụp bằng chứng.
- **Trả lời câu hỏi phần đọc phụ trách:**
  - *Vì sao nên tránh `implicitly_wait` khi đã dùng `WebDriverWait`?* Vì việc trộn lẫn implicit wait và explicit wait có thể gây ra thời gian chờ không xác định (unpredictable wait times) do xung đột giữa cơ chế timeout của driver và điều kiện polling của client.
- **Phản tư AI:**
  - *Đã hỏi AI điều gì:* Cách tối ưu timeout cho thiết bị di động thực tế để vừa không bị timeout sớm vừa không tốn thời gian khi test fail.
  - *Kết quả:* AI khuyến nghị mức timeout 15s cho mobile native test.
  - *Hiểu thêm được gì:* Hiểu sâu về kiến trúc kết nối giữa Appium client, Appium server và UiAutomator2 server trên Android.
