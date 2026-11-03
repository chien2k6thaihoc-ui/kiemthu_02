# Tuần 06 – Appium trên Swag Labs (Android)

Bài tập A1, A2, A3 bằng Appium Python Client + pytest.

| Phần | Nội dung | File |
|------|----------|------|
| A1 | Sắp xếp sản phẩm (explicit/implicit wait, locator, exceptions) | `test_a1_sort.py` |
| A2 | Giỏ hàng thêm/xoá & kéo-thả (ActionChains, popup/alert) | `test_a2_cart.py` |
| A3 | Cuộn danh sách & chụp màn hình (scrollGesture, UiScrollable, screenshot) | `test_a3_scroll.py` |

## Cấu trúc
```
conftest.py        fixture driver + wait, tự chụp ảnh khi test fail
helpers.py         locator + hàm dùng chung
test_a1_sort.py
test_a2_cart.py
test_a3_scroll.py
testcases.md       bảng test case
anh/               ảnh chụp màn hình
```

## Cài đặt
```bash
pip install -r requirements.txt
npm i -g appium
appium driver install uiautomator2
```

## Chạy
1. Bật emulator hoặc cắm điện thoại Android (bật USB debugging), kiểm tra `adb devices`.
2. Cài app Swag Labs / Sauce Labs My Demo App lên thiết bị.
3. Chạy `appium` ở một terminal.
4. Ở terminal khác:
```bash
pytest -v                          # chạy tất cả
pytest -v test_a1_sort.py          # chạy riêng A1
pytest -v > ket-qua-pytest.txt     # lưu kết quả để nộp
```

Đổi địa chỉ Appium bằng biến môi trường `APPIUM_URL` (mặc định `http://127.0.0.1:4723`).

## Lưu ý
- Locator đặt theo `com.saucelabs.mydemoapp.android`; nếu khác, kiểm tra bằng Appium Inspector và sửa trong `helpers.py`.
- Cuộn trên mobile dùng `mobile: scrollGesture` / `UiScrollable`, không dùng `window.scrollTo` như tài liệu Selenium web.
