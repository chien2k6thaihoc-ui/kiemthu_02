# Test cases – Tuần 06 (Swag Labs Android, Appium + pytest)

Cột **Kết quả thực tế** điền sau khi chạy trên máy/thiết bị của nhóm (Pass/Fail).

## A1 – Sắp xếp sản phẩm (`test_a1_sort.py`)

| ID | Mô tả | Các bước | Kết quả mong đợi | Kết quả thực tế |
|----|-------|----------|------------------|-----------------|
| A1-01 | Sắp xếp tên A→Z | Mở app → bấm sort → chọn nameAsc | Danh sách tên tăng dần | |
| A1-02 | Sắp xếp tên Z→A | Mở app → bấm sort → chọn nameDesc | Danh sách tên giảm dần | |
| A1-03 | Sắp xếp giá tăng | Mở app → bấm sort → chọn priceAsc | Giá tăng dần | |
| A1-04 | Sắp xếp giá giảm | Mở app → bấm sort → chọn priceDesc | Giá giảm dần | |
| A1-05 | Custom wait condition | Chờ danh sách có ≥ 2 sản phẩm | Điều kiện đạt, không timeout | |
| A1-06 | Ngoại lệ khi tìm phần tử không có | find_element với id không tồn tại; WebDriverWait 2s | Ném NoSuchElementException và TimeoutException | |

## A2 – Giỏ hàng & kéo-thả (`test_a2_cart.py`)

| ID | Mô tả | Các bước | Kết quả mong đợi | Kết quả thực tế |
|----|-------|----------|------------------|-----------------|
| A2-01 | Thêm rồi xoá sản phẩm | Chọn sản phẩm → Add To Cart → mở giỏ → Remove → xác nhận popup (nếu có) | Giỏ có 1 sản phẩm, sau khi xoá còn 0 | |
| A2-02 | Kéo-thả `drag_and_drop` | Lấy 2 sản phẩm → drag_and_drop(element, target) | Thao tác thực hiện không lỗi | |
| A2-03 | Kéo-thả ActionChains | click_and_hold → move_to_element → release | Thao tác thực hiện không lỗi | |
| A2-04 | Kéo-thả `mobile: dragGesture` | execute_script dragGesture | Thao tác thực hiện không lỗi | |
| A2-05 | Ngoại lệ nút xoá | Tìm "remove item" khi chưa mở giỏ | Ném NoSuchElementException | |

## A3 – Cuộn & chụp màn hình (`test_a3_scroll.py`)

| ID | Mô tả | Các bước | Kết quả mong đợi | Kết quả thực tế |
|----|-------|----------|------------------|-----------------|
| A3-01 | Cuộn bằng UiScrollable + chụp màn hình | scrollIntoView tới sản phẩm cuối → save_screenshot | Phần tử hiển thị; file ảnh > 0 byte | |
| A3-02 | Cuộn bằng scrollGesture | execute_script("mobile: scrollGesture") | Danh sách sau cuộn khác trước cuộn | |
| A3-03 | Chụp ảnh phần tử | element.screenshot(path) | File ảnh được tạo | |
