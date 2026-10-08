# kiemthu_02 — Kiểm thử tự động app Android **Swag Labs**

Repo thực hành kiểm thử tự động của nhóm **App**: **Appium 2 + driver UiAutomator2**, viết test bằng **Python + pytest**.

- Tuần 04: [`tuan-04/test_smoke.py`](tuan-04/test_smoke.py) — mở ứng dụng Swag Labs và kiểm tra **có ô nhập tên đăng nhập**.
- Tài khoản app dùng về sau: `standard_user` / `secret_sauce`.
- Nhánh nộp bài mỗi tuần: `week-<NN>` → gộp vào `main`.

> Phiên bản đã dùng và kiểm chứng trên máy thành viên ngày 2026-10-08: Python 3.14.8 · pytest 9.1.1 · Appium-Python-Client 6.0.7 · selenium 4.50.0 · Node.js 26.10.0 · npm 11.19.1 · Appium CLI 3.8.0 · driver `uiautomator2@8.7.0` · JDK 17.0.12 · adb 1.0.41.

---

## 1. Cần cài những gì

| # | Thành phần | Dùng để làm gì |
|---|---|---|
| 1 | Python 3.11+ và `pip` | Chạy pytest và Appium client |
| 2 | `Appium-Python-Client`, `pytest` | Thư viện gửi lệnh WebDriver + framework test |
| 3 | Node.js + npm | Cài và chạy Appium server |
| 4 | Appium CLI + driver `uiautomator2` | Server + driver điều khiển Android |
| 5 | JDK 17 | Android SDK/emulator cần Java |
| 6 | Android SDK (`platform-tools`, `emulator`) | `adb`, máy ảo Android |
| 7 | File `.apk` Swag Labs | Ứng dụng bị kiểm thử |

## 2. Cài đặt

### 2.1 Python + thư viện

```powershell
python --version
python -m pip install -U Appium-Python-Client pytest
python -m pip show Appium-Python-Client pytest
```

### 2.2 Node.js + Appium server + driver

```powershell
node --version
npm --version
npm install -g appium
appium driver install uiautomator2
appium --version
appium driver list --installed
```

### 2.3 JDK 17

Cài JDK 17 rồi khai báo biến môi trường (Windows → *Edit the system environment variables*):

```powershell
# Ví dụ; thay bằng đường dẫn JDK 17 trên máy bạn
setx JAVA_HOME "D:\Programs\Java\jdk-17"
java -version   # phải in ra 17.x
```

### 2.4 Android SDK + biến môi trường

Cài Android Studio → **SDK Manager** → cài *Android SDK Platform-Tools* và *Android Emulator*.

```powershell
setx ANDROID_HOME "$env:LOCALAPPDATA\Android\Sdk"
# Thêm vào PATH:
#   %ANDROID_HOME%\platform-tools      (để có lệnh adb)
#   %ANDROID_HOME%\emulator            (để có lệnh emulator)
```

Mở **terminal mới** rồi kiểm tra:

```powershell
adb version
emulator -list-avds
```

### 2.5 Máy ảo Android (hoặc điện thoại thật)

- **Máy ảo (khuyến nghị nếu máy yếu không cắm được điện thoại):** Android Studio → *Device Manager* → tạo AVD (ví dụ đã dùng: `Medium_Phone_API_37.0`) → khởi động.
- **Điện thoại thật:** bật *Developer options* → *USB debugging*, cắm cáp, chọn chế độ **MTP**, rồi bấm **Cho phép gỡ lỗi USB** + tick *Luôn cho phép từ máy tính này*.

## 3. Chuẩn bị thiết bị và ứng dụng

```powershell
# 1) Phải thấy đúng 1 thiết bị ở trạng thái "device" (không phải "unauthorized")
adb devices -l

# 2) Chạy máy ảo nếu dùng AVD
emulator -avd Medium_Phone_API_37.0

# 3) Tải .apk Swag Labs tại:
#    https://github.com/saucelabs/sample-app-mobile/releases
adb install -r "$env:USERPROFILE\Downloads\sample-app-mobile-<version>.apk"

# 4) Xác nhận app đã có trên thiết bị
adb shell pm list packages | findstr swaglabs
```

> `test_smoke.py` đặt `no_reset = True`, nghĩa là **Appium không tự cài app** — phải cài `.apk` trước bằng bước 3.

## 4. Bật Appium server (giữ terminal này mở)

```powershell
appium
```

Chờ tới khi thấy dòng tương tự:

```
Appium REST http interface listener started on http://0.0.0.0:4723
```

Test kết nối tới `http://127.0.0.1:4723` (đúng địa chỉ mà `test_smoke.py` dùng).

## 5. Sửa `device_name` cho khớp thiết bị của bạn

[`tuan-04/test_smoke.py`](tuan-04/test_smoke.py#L11) đang ghi cứng serial của máy một thành viên:

```python
options.device_name = "ATLSVB4103012319"
```

Lấy serial thật từ `adb devices -l` rồi sửa lại cho khớp. *(Lưu ý: driver UiAutomator2 thường bỏ qua `deviceName` khi chỉ có một thiết bị, nhưng khi cắm nhiều máy thì nên sửa, hoặc thêm `options.udid = "<serial>"` để chỉ đúng máy.)*

## 6. Chạy bài kiểm thử

Từ **thư mục gốc repo**:

```powershell
python -m pytest tuan-04/test_smoke.py -v
```

Kết quả mong đợi:

```
tuan-04/test_smoke.py::test_swaglabs_smoke PASSED
1 passed in ...s
```

## 7. Bài thực hành bắt buộc: cố ý gây lỗi

1. Sửa locator trong `test_smoke.py`: `test-Username` → `test-Username-sai`.
2. Chạy lại → phải thấy `NoSuchElementException` và `1 failed` (đây là **lỗi cố ý**, không phải lỗi cài đặt).
3. Sửa lại `test-Username` → chạy lại → `PASSED`.

Ảnh chụp cả hai trạng thái nằm ở [`tuan-04/anh/`](tuan-04/anh), ghi chép ở [`tuan-04/notes.md`](tuan-04/notes.md) mục 3.

## 8. Lỗi thường gặp và cách sửa

| Thông báo | Nguyên nhân | Cách sửa |
|---|---|---|
| `The term 'adb' is not recognized` | Chưa thêm `platform-tools` vào `PATH` | Thêm `%ANDROID_HOME%\platform-tools` vào `PATH`, mở terminal mới |
| `Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported` | Appium server chưa thấy Android SDK | Đặt `ANDROID_HOME`, rồi **khởi động lại** Appium server |
| `adb devices` để trống | Chưa bật *USB debugging*, hoặc điện thoại chưa **Cho phép** máy tính, hoặc AVD chưa chạy | Bật lại *Gỡ lỗi USB*, rút/cắm cáp, chọn MTP, bấm **Cho phép**; nếu không hiện hộp thoại → *Thu hồi quyền gỡ lỗi USB* rồi cắm lại; hoặc khởi động AVD |
| Thiết bị hiện `unauthorized` | Chưa chấp nhận khoá RSA | Bấm **Cho phép** trên điện thoại |
| `Connection refused` / không kết nối được cổng `4723` | Appium server chưa chạy | Chạy `appium` ở terminal riêng (mục 4) |
| `NoSuchElementException` ở `test-Username` | App chưa ở màn đăng nhập, app chưa cài, hoặc locator sai | Kiểm tra bước 3; nếu vừa cố ý sửa locator thì đổi lại `test-Username` |
| `An element could not be located on the page` ngay khi mở app | Chưa cài `.apk` (do `no_reset = True`) | Chạy lại `adb install -r <file>.apk` |

## 9. Cấu trúc repo

```
.
├── README.md              # tài liệu này (W04)
├── tuan-04/               # W04: smoke test
│   ├── test_smoke.py
│   ├── notes.md
│   └── anh/               # ảnh bằng chứng chạy test
└── ...                    # tuan-05 … tuan-11
```

## 10. Quy ước khi thêm tuần mới

- Mỗi tuần một thư mục `tuan-<NN>` ở gốc repo, đẩy lên nhánh `week-<NN>` rồi gộp `main`.
- Comment tiếng Việt giải thích từng bước trong bài test.
- Không dùng `time.sleep` — dùng wait tường minh (`WebDriverWait`) khi cần chờ.
- **Không xoá/ghi đè ảnh, log, ghi chú của các tuần trước.**
