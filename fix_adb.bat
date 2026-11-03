@echo off
setlocal

:: Kiem tra quyen Administrator. Neu chua co thi goi UAC de xin quyen
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Dang yeu cau quyen Administrator...
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/k \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title FIX ADB VSMART (VID_339B)
color 0A
echo ===================================================================
echo   FIX ADB CHO VSMART (GHI GUID CHUAN VAO WINUSB)
echo   GUID Chuan cua Android ADB: {F72FE0D4-CBCB-407D-8814-9ED673D0DD6B}
echo ===================================================================
echo.

echo [1/3] Dang ghi GUID chuan vao Registry cho MI_01 va MI_02...
reg add "HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_339B&PID_107D&MI_02\6&5c8ab2a&0&0002\Device Parameters" /v DeviceInterfaceGUIDs /t REG_MULTI_SZ /d "{F72FE0D4-CBCB-407D-8814-9ED673D0DD6B}" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_339B&PID_107D&MI_02\6&5c8ab2a&0&0002\Device Parameters" /v DeviceInterfaceGUID /t REG_SZ /d "{F72FE0D4-CBCB-407D-8814-9ED673D0DD6B}" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_339B&PID_107D&MI_01\6&5c8ab2a&0&0001\Device Parameters" /v DeviceInterfaceGUIDs /t REG_MULTI_SZ /d "{F72FE0D4-CBCB-407D-8814-9ED673D0DD6B}" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_339B&PID_107D&MI_01\6&5c8ab2a&0&0001\Device Parameters" /v DeviceInterfaceGUID /t REG_SZ /d "{F72FE0D4-CBCB-407D-8814-9ED673D0DD6B}" /f

echo.
echo [2/3] Dang restart device qua pnputil de driver nap ngay lap tuc...
pnputil /restart-device "USB\VID_339B&PID_107D&MI_02\6&5C8AB2A&0&0002"
pnputil /restart-device "USB\VID_339B&PID_107D&MI_01\6&5C8AB2A&0&0001"

echo.
echo [3/3] Khoi dong lai adb server...
taskkill /F /IM adb.exe >nul 2>&1
timeout /t 1 /nobreak >nul
adb start-server

echo.
echo ===================================================================
echo KET QUA ADB DEVICES:
echo -------------------------------------------------------------------
adb devices -l
echo -------------------------------------------------------------------
echo.
echo Neu hien ten thiet bi hoac hien chu 'unauthorized':
echo -> Hay MO KHOA MAN HINH DIEN THOAI va bam 'CHO PHEP / ALLOW'.
echo.
pause
