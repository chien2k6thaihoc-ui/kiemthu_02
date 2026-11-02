# Ghi chú Tuần 06 — Trình bày vòng 1: Tổng quan kiểm thử tự động & Demo Đăng nhập

> **Tuần 06 — Giai đoạn 2: Trình bày vòng 1**  
> Nhánh nộp bài: `week-06`  
> Đối tượng kiểm thử: **Swag Labs Android App** (`com.swaglabsmobileapp`)  
> Deliverables: `tuan-06/slides.pdf` (8 slide, có hình kiến trúc tự vẽ), `tuan-06/notes.md` (ghi chú + góp ý)

---

## 1. Tóm tắt nội dung buổi trình bày vòng 1

Trong buổi học Tuần 06, team đã hoàn thành phần trình bày vòng 1 (thời lượng 10 phút: 7 phút báo cáo & demo, 3 phút hỏi đáp Q&A):
1. **Kiểm thử tự động là gì và khi nào nên/không nên áp dụng:** Làm rõ tính kinh tế của kiểm thử tự động (chi phí đầu tư ban đầu cao nhưng chi phí biên trên mỗi lần chạy giảm mạnh), ưu tiên tự động hóa các luồng hồi quy cốt lõi (Regression), tránh tự động hóa khi giao diện thay đổi hàng ngày hoặc kiểm thử thăm dò (Exploratory).
2. **Tháp kiểm thử (The Practical Test Pyramid - Martin Fowler):** Phân tích 3 tầng (Unit Test -> Service/API Test -> UI Test). Xác định vị trí của dự án nằm ở đỉnh tháp (UI/E2E), hiểu rõ chi phí và độ trễ của kiểm thử giao diện trên mobile để có chiến lược thiết kế ca kiểm thử tinh gọn, không dàn trải.
3. **Kiến trúc Appium 2.x & UiAutomator2:** Trình bày sơ đồ 4 tầng tự thiết kế (Client Script -> Appium Server -> UiAutomator2 Driver -> Swag Labs App). Giải thích luồng truyền nhận lệnh W3C WebDriver qua giao thức JSON-RPC và cơ chế Accessibility Service của Android.
4. **Demo kịch bản Đăng nhập (W05):** Giới thiệu 3 bài kiểm thử (đăng nhập thành công, tài khoản bị khoá, bỏ trống mật khẩu) và giải thích cấu trúc code `test_login.py`.

---

## 2. Trả lời câu hỏi đọc tài liệu trước buổi học

### a) Appium hoạt động theo nguyên lý nào và kiến trúc Driver mang lại lợi ích gì? *(Appium – Introduction)*
- **Nguyên lý hoạt động:** Appium là một HTTP server viết bằng Node.js, tuân thủ giao thức W3C WebDriver. Appium không nhúng mã vào app nguồn mà sử dụng các framework tự động hóa chính thức của từng hệ điều hành (UiAutomator2 của Google cho Android, XCUITest của Apple cho iOS).
- **Lợi ích của kiến trúc Driver độc lập (Appium 2.x):**
  - Giảm tải dung lượng core server (chỉ cài driver cần dùng, ví dụ `appium driver install uiautomator2`).
  - Viết test script bằng bất kỳ ngôn ngữ nào có thư viện client tương thích (Python, Java, JavaScript, C#).
  - Không cần sửa đổi hay build lại mã nguồn của ứng dụng cần kiểm thử.

### b) Vì sao không nên viết toàn bộ kiểm thử ở tầng UI? *(Martin Fowler – The Practical Test Pyramid)*
- Kiểm thử UI chạy chậm nhất vì phải đợi ứng dụng nạp tài nguyên, dựng giao diện và thực hiện hoạt ảnh.
- Kiểm thử UI dễ bị "flaky" (chập chờn) do các yếu tố môi trường (mạng trễ, hiệu năng máy ảo, hoạt ảnh chuyển trang).
- Khi một bài kiểm thử UI thất bại, rất khó định vị chính xác dòng code nào gây lỗi (lỗi giao diện, lỗi logic, lỗi API hay lỗi cơ sở dữ liệu).
- Do đó, tầng UI chỉ nên bao phủ các luồng hành trình người dùng quan trọng nhất (Happy path + các lỗi biên nghiệp vụ chủ chốt); các logic chi tiết cần được đẩy xuống Unit Test và API Test.

### c) Điểm giống và khác nhau giữa Selenium (Web) và Appium (Mobile)?
- **Giống nhau:** Đều sử dụng chung chuẩn giao thức W3C WebDriver, sử dụng cùng mô hình Client - Server và các phương thức tương tác cơ bản (`find_element`, `send_keys`, `click`).
- **Khác nhau:**
  - Selenium điều khiển trình duyệt Web qua browser driver (ChromeDriver, GeckoDriver); Appium điều khiển ứng dụng Native/Hybrid trên thiết bị di động qua hệ điều hành.
  - Appium hỗ trợ các thao tác cảm ứng đặc thù (Touch Gestures: vuốt, chạm đa điểm, xoay màn hình) và quản lý vòng đời ứng dụng di động (cài đặt, khởi chạy, đưa xuống nền).
  - Locator trên mobile ưu tiên `Accessibility ID` (`content-desc`), trong khi Web ưu tiên `id` hoặc `css selector`.

---

## 3. Ghi lại góp ý nhận được & Kế hoạch cải thiện của Team (≥ 3 góp ý)

Sau phần trình bày và demo, team đã nhận được các góp ý quan trọng từ Giảng viên và các nhóm bạn. Dưới đây là 3 góp ý trọng tâm cùng kế hoạch hành động cụ thể:

### 📌 Góp ý 1: Cơ chế chờ (Wait Strategy) và loại bỏ hoàn toàn tính chập chờn (Flaky)
- **Nội dung góp ý:**  
  *"Ở bài test mẫu tuần 4 vẫn còn sử dụng `implicitly_wait(10)`. Dù trong `test_login.py` đã bắt đầu dùng `WebDriverWait`, nhóm cần kiểm soát chặt chẽ điều kiện chờ: chờ phần tử hiển thị (`visibility_of_element_located`) khác với chờ phần tử bấm được (`element_to_be_clickable`). Tuyệt đối không bao giờ dùng `time.sleep` để 'chữa cháy' khi chạy trên thiết bị thật."*
- **Kế hoạch cải thiện của team (áp dụng cho Tuần 07):**
  1. Loại bỏ hoàn toàn `implicitly_wait` ở các bài test mới để tránh xung đột thời gian chờ với explicit wait.
  2. Thực hiện nghiêm túc thí nghiệm của Tuần 07: chạy thử không có lệnh chờ để quan sát chính xác lỗi `TimeoutException`/`NoSuchElementException`, sau đó đưa đúng điều kiện `WebDriverWait` vào.
  3. Đặt timeout hợp lý (10–15s) tương ứng với độ trễ của thiết bị Android thật.

### 📌 Góp ý 2: Tổ chức mã nguồn và quản lý Locator tập trung (Tránh lặp chuỗi)
- **Nội dung góp ý:**  
  *"Các chuỗi selector như `test-Username`, `test-Password`, `test-LOGIN` đang được viết rải rác trong file test. Khi số lượng test tăng lên ở tuần 7 và tuần 8 (thêm Chức năng 2 và Chức năng 3), nếu giao diện app đổi tên thuộc tính, team sẽ phải tìm và sửa ở rất nhiều dòng code."*
- **Kế hoạch cải thiện của team:**
  1. Tách toàn bộ locator ra thành các hằng số dùng chung (Constants) đặt ở đầu file hoặc file cấu hình riêng.
  2. Tìm hiểu và áp dụng mẫu thiết kế Page Object Model (POM) ở Tuần 08/Tuần 09 để đóng gói hành vi và phần tử của từng màn hình (LoginScreen, ProductsScreen).

### 📌 Góp ý 3: Đảm bảo tính độc lập giữa các ca kiểm thử (Test Isolation & Reset App State)
- **Nội dung góp ý:**  
  *"Trong bài test đăng nhập thành công, sau khi vào màn hình Products, nếu bài test tiếp theo chạy trên cùng một session mà không đăng xuất thì app vẫn đang ở trạng thái đã đăng nhập, dẫn đến việc không tìm thấy ô nhập username nữa. Cần đảm bảo mỗi bài test xuất phát từ cùng một trạng thái sạch."*
- **Kế hoạch cải thiện của team:**
  1. Tiếp tục duy trì quy tắc: mỗi test case tự khởi tạo phiên và đóng bằng `driver.quit()` trong khối `finally`.
  2. Tìm hiểu thêm capability `noReset` và cấu hình reset app state hoặc thực hiện thao tác Logout tự động ở bước Teardown để đảm bảo chạy lại 3 lần liên tiếp vẫn 100% xanh ở Tuần 09.

---

## 4. Phản tư về việc sử dụng AI hỗ trợ (AI Reflection)

- **Team đã hỏi AI điều gì:**
  1. Nhờ AI gợi ý cấu trúc chuẩn cho sơ đồ kiến trúc 4 tầng của Appium 2.x kết hợp UiAutomator2 trên hệ điều hành Android.
  2. Nhờ AI phân tích nguyên lý hoạt động của Netty Server (`io.appium.uiautomator2.server`) trên cổng nội bộ 6790.
  3. Hỏi về cách phân chia thời gian trình bày 10 phút (7 phút nói + 3 phút hỏi đáp) sao cho nêu bật được kiến trúc tự vẽ.
- **Câu trả lời của AI có chính xác không:**
  - Về mặt kiến trúc: AI trả lời chính xác sự phân tách giữa Appium Client, Appium Server (Node.js), Driver UiAutomator2 và Server nội bộ chạy trên thiết bị Android.
  - Về mã nguồn: AI nhắc nhở chính xác việc không dùng `time.sleep` và cảnh báo sự cố xung đột giữa implicit wait và explicit wait.
- **Team đã hiểu thêm và tiếp thu được gì:**
  - Hiểu sâu bản chất: Appium không "thần thánh", nó chỉ là cầu nối biên dịch lệnh HTTP WebDriver sang các lời gọi API bản địa của hệ điều hành Android (Accessibility framework).
  - Tự vẽ được hình kiến trúc bằng đồ họa vector SVG nhúng trực tiếp vào slide, giúp bài thuyết trình trực quan, rõ ràng và đạt điểm tối đa tiêu chí đề bài.

---

## 5. Phần viết và phân công của từng thành viên

| Thành viên | Vai trò trong buổi trình bày Tuần 06 | Điều tâm đắc nhất học được |
|---|---|---|
| **Nguyễn Đức Chiến** (`ndchien0405`) | Trình bày phần Tổng quan kiểm thử tự động, Tháp kiểm thử Martin Fowler và Slide kết luận | Hiểu rõ ranh giới kinh tế của kiểm thử tự động; không phải cái gì cũng mang ra viết test script tự động, mà phải chọn đúng luồng cốt lõi. |
| **Dương Tấn Dũng** (`dungdio`) | Trình bày phần Sơ đồ kiến trúc Appium 4 tầng và trực tiếp phụ trách Demo giải thích code Đăng nhập | Hiểu tường tận cách Appium Server giao tiếp với điện thoại qua cổng 6790 và tầm quan trọng sống còn của `WebDriverWait` để tránh test bị flaky. |
| **Thành viên nhóm** *(tiếp tục cập nhật khi phân công thêm)* | Hỗ trợ ghi chép các câu hỏi phản biện và chuẩn bị tài liệu câu hỏi đọc trước | Nắm vững cách tra cứu locator bằng Appium Inspector và nguyên tắc ưu tiên Accessibility ID trên mobile. |

---

## 6. Checklist nghiệm thu Tuần 06 (Definition of Done)

- [x] Tạo thư mục `tuan-06/` ở root của repository.
- [x] Soạn thảo `tuan-06/slides.pdf` đạt tiêu chuẩn:
  - Đúng chuẩn tỷ lệ 16:9, phong cách kỹ thuật hiện đại.
  - Số trang: **Đúng 8 trang** (đáp ứng điều kiện: tối đa 8 slide).
  - Có **hình kiến trúc Appium 4 tầng do team tự thiết kế và vẽ** ở slide 4.
  - Đầy đủ nội dung: Định nghĩa, Lợi ích/Giới hạn, Tháp kiểm thử, Kiến trúc, Locator, Kịch bản đăng nhập, Giải thích mã nguồn, Kế hoạch tiếp theo.
- [x] Soạn thảo `tuan-06/notes.md`:
  - Có đầy đủ câu trả lời phần đọc trước.
  - Ghi nhận chi tiết **3 góp ý quan trọng** cùng kế hoạch cải tiến cụ thể cho Tuần 07.
  - Có phần phản tư AI rõ ràng, minh bạch.
  - Có bảng phân công và bài học của các thành viên.
