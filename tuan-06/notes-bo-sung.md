# Ghi chú bổ sung – A1, A2, A3 (dán vào notes.md của nhóm)

## Đã làm được
- **A1:** kiểm tra 4 kiểu sắp xếp (tên A→Z/Z→A, giá tăng/giảm) bằng explicit wait (`WebDriverWait` + `expected_conditions`), có thêm custom wait condition và test ngoại lệ (`NoSuchElementException`, `TimeoutException`).
- **A2:** thêm/xoá sản phẩm trong giỏ, xử lý popup/alert, kéo-thả bằng 3 cách: `drag_and_drop`, chuỗi `click_and_hold → move_to_element → release`, và `mobile: dragGesture`.
- **A3:** cuộn bằng `UiScrollable` và `mobile: scrollGesture`; chụp màn hình bằng `save_screenshot` và ảnh phần tử bằng `element.screenshot`.

## Khác biệt Selenium web và Appium mobile
| Nội dung | Tài liệu Selenium (web) | Appium (app Android) |
|----------|-------------------------|----------------------|
| Locator | `By.ID`, `By.NAME`, CSS, XPath | `AppiumBy.ACCESSIBILITY_ID`, `ANDROID_UIAUTOMATOR`, id |
| Cuộn | `execute_script("window.scrollTo(0, document.body.scrollHeight)")` | `execute_script("mobile: scrollGesture", {...})` hoặc `UiScrollable` |
| Kéo-thả | `ActionChains.drag_and_drop(element, target)` | Dùng được, nhưng `mobile: dragGesture` ổn định hơn |
| Popup | `driver.switch_to.alert` | Alert hệ thống dùng được; dialog của app là phần tử thường (ví dụ nút `android:id/button1`) |
| Screenshot | `driver.save_screenshot(...)` | Giống nhau |

## Khó khăn
- `window.scrollTo` không có trong app native nên phải đổi sang lệnh `mobile:` của Appium.
- Một số locator phải dò lại bằng Appium Inspector.
- Kéo-thả bằng `ActionChains` đôi khi không ăn trên Android; cần thử thêm `dragGesture`.

## Bài học
- Dùng explicit wait thay cho `time.sleep()` để test ổn định hơn.
- Tách locator và hàm dùng chung vào `helpers.py`, fixture vào `conftest.py` để code gọn và dễ bảo trì.
