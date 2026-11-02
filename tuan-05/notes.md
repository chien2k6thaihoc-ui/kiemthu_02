# Ghi chú Tuần 05 — Bài kiểm thử chức năng Đăng nhập (Swag Labs, Android)

> ✅ **TRẠNG THÁI CHẠY: ĐÃ HOÀN THÀNH VÀ CHẠY THÀNH CÔNG (3/3 PASSED).**
> - Thiết bị đã kết nối qua ADB không dây (`adb connect 192.168.1.18:41785`).
> - Appium server v2.16.2 đã khởi chạy ở cổng 4723.
> - Cả 3 test case trong `test_login.py` đã chạy thực tế và đều PASS.
> - Đã chụp và lưu ảnh bằng chứng vào `tuan-05/anh/` (`tc01_login_success.png`, `tc02_locked_out_user.png`, `tc03_empty_password.png`).

---

## 1. Đã học được gì trong tuần này

- **3 việc cốt lõi của một bài kiểm thử giao diện:** (1) *tìm đúng phần tử* trên màn hình, (2) *thao tác* với nó (nhập chữ, bấm nút), (3) *kiểm tra kết quả* bằng `assert`. Ba bài trong `test_login.py` được chia theo đúng 3 bước này.
- **Cách ly từng test case:** mỗi bài tự mở một phiên Appium riêng và `driver.quit()` trong `finally`. Sử dụng fixture `reset_app_state` gọi `adb shell pm clear com.swaglabsmobileapp` để làm sạch dữ liệu ứng dụng trước mỗi bài test, đảm bảo trạng thái xuất phát luôn là màn hình đăng nhập sạch sẽ.
- **Chờ tường minh thay vì chờ ngầm định:** dùng `WebDriverWait` + `expected_conditions.visibility_of_element_located` để chờ đúng phần tử cần dùng, thay vì `implicitly_wait` chờ mọi phần tử một khoảng cố định. Việc này chuẩn bị cho tuần 07 (yêu cầu **không dùng `time.sleep`**).
- **Truyền thông điệp lỗi vào `assert`:** `assert x in y, f"..."` giúp khi bài kiểm thử fail thì biết ngay giá trị thực tế nhận được là gì, thay vì chỉ thấy "AssertionError".
- **Kiểm thử trường hợp sai (negative) cũng phải kiểm tra đúng nội dung thông báo**, không chỉ kiểm tra "không vào được màn chính". Ví dụ với tài khoản bị khoá, phải `assert` thấy thông báo *"Sorry, this user has been locked out."*.
- **Cấu trúc cây UI của React Native trên Android:** phần tử có accessibility id `test-Error message` là một `ViewGroup`, nội dung chữ thực sự nằm trong thẻ con `android.widget.TextView`. Khi lấy text cần đọc từ `TextView` con.

## 2. Trả lời câu hỏi phần đọc (W05)

**a) Với ô tên đăng nhập ở trang `/login`, nên xác định bằng cách nào là ổn định nhất, vì sao?** *(Selenium – Locator strategies)*
Nên ưu tiên `id` (hoặc accessibility id trên mobile), vì nó gắn với bản thân phần tử chứ không phụ thuộc vị trí trong cây giao diện hay nội dung hiển thị. XPath kiểu đường dẫn tuyệt đối (`/html/body/div[2]/...`) sẽ hỏng ngay khi trang đổi bố cục, còn CSS selector theo class cũng dễ hỏng khi giao diện đổi style.

**b) Muốn nhập chữ vào một ô thì dùng lệnh gì?** *(Selenium – Interacting with elements)*
Dùng `element.send_keys("nội dung")`. Trước khi nhập nên `clear()` để xoá nội dung cũ (đã áp dụng trong `login()`), tránh trường hợp nối thêm chữ vào giá trị có sẵn.

**c) Làm thế nào để biết id của một ô nhập trên trang?** *(Chrome DevTools – View & change the DOM)*
Mở DevTools → tab Elements → dùng công cụ chọn phần tử (Ctrl+Shift+C) bấm vào ô nhập, rồi đọc thuộc tính `id` trong panel bên phải.

**d) Làm thế nào để tìm accessibility id của một nút trong ứng dụng?** *(Appium Inspector – Docs)*
Mở Appium Inspector (hoặc `adb shell uiautomator dump`), kết nối tới Appium server, khởi tạo phiên với app cần kiểm tra, bấm vào nút trên cây giao diện; giá trị `accessibility id` (trên Android hiển thị ở thuộc tính `content-desc`) sẽ nằm trong panel thuộc tính của phần tử.

**e) Vì sao trên điện thoại nên ưu tiên accessibility id?** *(UiAutomator2 driver – README, Element Location)*
Vì accessibility id do lập trình viên đặt và gắn với **mục đích** của phần tử, nên ổn định hơn XPath — vốn phụ thuộc vào cấu trúc cây giao diện và sẽ hỏng khi app đổi bố cục hoặc thêm/bớt phần tử. Nó cũng hoạt động được trên cả iOS lẫn Android, giúp bài kiểm thử dễ bảo trì.

**f) Nếu kết quả thực tế khác mong đợi thì pytest báo gì?** *(pytest – Assertions)*
pytest báo `AssertionError` và in ra biểu thức bị sai. Với `assert a == b`, pytest còn hiển thị giá trị thực tế và giá trị mong đợi để dễ so sánh. Nếu tự truyền thông điệp (như trong `test_login.py`), thông điệp đó được in kèm.

## 3. Test case đã viết (trước khi viết code)

Đã viết `tuan-05/testcases.md` **trước** khi viết `test_login.py`, gồm 3 test case:
TC-05-01 (đăng nhập thành công), TC-05-02 (`locked_out_user`), TC-05-03 (bỏ trống mật khẩu) — mỗi case có bước làm, dữ liệu nhập, kết quả mong đợi.

## 4. Locator — kết quả xác minh thực tế

| Phần tử | Locator | Trạng thái | Ghi chú kỹ thuật |
|---|---|---|---|
| Ô Username | `test-Username` | ✅ **Đã xác minh** | `accessibility id` (content-desc: `test-Username`) |
| Ô Password | `test-Password` | ✅ **Đã xác minh** | `accessibility id` (content-desc: `test-Password`) |
| Nút LOGIN | `test-LOGIN` | ✅ **Đã xác minh** | `accessibility id` (content-desc: `test-LOGIN`) |
| Thông báo lỗi | `test-Error message` + `TextView` | ✅ **Đã xác minh** | ViewGroup chứa con `android.widget.TextView` |
| Màn Products | text `PRODUCTS` | ✅ **Đã xác minh** | `//*[@text='PRODUCTS']` |

## 5. Khó khăn gặp phải & cách giải quyết

- **Vấn đề kết nối thiết bị:** Cổng kết nối USB của thiết bị không ổn định ở chế độ gỡ lỗi có dây. Đã giải quyết triệt để bằng cách kích hoạt gỡ lỗi không dây (Wireless Debugging) thông qua lệnh `adb pair` và `adb connect 192.168.1.18:41785`.
- **Trạng thái session giữa các test case:** Khi đăng nhập thành công ở test case 1, app giữ trạng thái đã đăng nhập khiến các test case sau không tìm thấy ô đăng nhập. Đã xử lý bằng pytest fixture `reset_app_state` tự động gọi `adb shell pm clear com.swaglabsmobileapp`.
- **Đọc thông báo lỗi:** `test-Error message` là thẻ `ViewGroup`, thuộc tính `.text` trả về rỗng. Đã truy vấn phần tử con `TextView` bên trong để đọc được text chính xác.

## 6. Kết quả thực thi

Toàn bộ 3 bài kiểm thử đã chạy thành công trong 39.29 giây:
```text
tuan-05/test_login.py::test_login_success PASSED                         [ 33%]
tuan-05/test_login.py::test_login_locked_out_user PASSED                 [ 66%]
tuan-05/test_login.py::test_login_empty_password PASSED                  [100%]
```
Đã lưu ảnh màn hình vào `tuan-05/anh/`:
- `tc01_login_success.png`
- `tc02_locked_out_user.png`
- `tc03_empty_password.png`

## 7. Phần viết của từng thành viên & Phản tư AI

### 7.1 Thành viên: Dũng

- **Điều tôi học được:**
  - Nắm vững 3 bước cốt lõi của một bài kiểm thử giao diện: tìm phần tử, tương tác và kiểm tra bằng `assert`.
  - Hiểu cách hoạt động của `adb shell pm clear com.swaglabsmobileapp` để cô lập dữ liệu bài test, đảm bảo mỗi ca kiểm thử bắt đầu từ trạng thái sạch.
- **Câu hỏi phần đọc phụ trách + câu trả lời:**
  - *Vì sao trên điện thoại nên ưu tiên accessibility id?* Vì accessibility id gắn liền với mục đích của phần tử thay vì vị trí hay style, không bị gãy khi ứng dụng thay đổi layout, hoạt động đồng nhất trên cả Android và iOS.
- **Tôi đã hỏi AI điều gì / câu trả lời có đúng không / tôi hiểu thêm được gì:**
  - *Đã hỏi AI:* Cách xử lý lỗi `NoSuchElementException` khi tìm ô `test-Username` sau khi test case 1 vừa chạy xong.
  - *Câu trả lời của AI:* AI đề xuất dùng `adb shell pm clear` trong fixture để dọn dẹp phiên đăng nhập cũ, câu trả lời hoàn toàn chính xác.
  - *Hiểu thêm được gì:* Kiểm thử tự động trên mobile đòi hỏi phải quản lý kỹ lưỡng trạng thái ứng dụng giữa các lần chạy liên tiếp.

### 7.2 Thành viên: Chiến

- **Điều tôi học được:**
  - Nắm bắt cấu trúc phân cấp UI của ứng dụng React Native trên Android thông qua công cụ dump UI của Appium và UiAutomator2.
  - Cách định vị phần tử con `TextView` bên trong một `ViewGroup` (`test-Error message`) để lấy chính xác chuỗi thông báo lỗi.
- **Câu hỏi phần đọc phụ trách + câu trả lời:**
  - *Muốn nhập chữ vào một ô thì dùng lệnh gì?* Dùng `element.send_keys("nội dung")`, và nên gọi `clear()` trước để làm sạch dữ liệu cũ.
- **Tôi đã hỏi AI điều gì / câu trả lời có đúng không / tôi hiểu thêm được gì:**
  - *Đã hỏi AI:* Tại sao thuộc tính `.text` của phần tử `test-Error message` lại trả về chuỗi rỗng.
  - *Câu trả lời của AI:* AI chỉ ra rằng trên React Native, `test-Error message` là ViewGroup container, còn chuỗi ký tự nằm ở thẻ con `android.widget.TextView`.
  - *Hiểu thêm được gì:* Hiểu sâu về cách React Native render các component giao diện xuống các widget bản địa của Android.

### 7.3 Thành viên: Toàn

- **Điều tôi học được:**
  - Biết cách thiết kế test case có cấu trúc rõ ràng với đầy đủ thông tin: ID, mục đích, tiền điều kiện, các bước thực hiện và kết quả mong đợi.
  - Viết thông điệp lỗi chi tiết trong câu lệnh `assert` để chẩn đoán nhanh khi test case thất bại.
- **Câu hỏi phần đọc phụ trách + câu trả lời:**
  - *Nếu kết quả thực tế khác mong đợi thì pytest báo gì?* pytest sẽ ném ra `AssertionError`, đồng thời in chi tiết biểu thức so sánh và thông điệp lỗi tự định nghĩa.
- **Tôi đã hỏi AI điều gì / câu trả lời có đúng không / tôi hiểu thêm được gì:**
  - *Đã hỏi AI:* Cú pháp viết pytest fixture autouse để dọn dẹp ứng dụng trước mỗi bài kiểm thử.
  - *Câu trả lời của AI:* Hướng dẫn dùng `@pytest.fixture(autouse=True)` kết hợp `subprocess.run(["adb", "shell", "pm", "clear", ...])`.
  - *Hiểu thêm được gì:* Tận dụng tối đa sức mạnh của pytest fixtures để tối ưu mã nguồn kiểm thử.

