@echo off
set VENV_NAME=venv

:: --- BUOC 1: KIEM TRA PYTHON ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python chua duoc cai dat. Vui long cai Python truoc.
    pause
    exit /b
)

:: --- BUOC 2: TAO MOI TRUONG AO ---
if exist %VENV_NAME% (
    echo [1/4] Moi truong ao '%VENV_NAME%' da ton tai. Bo qua tao moi.
) else (
    echo [1/4] Dang tao moi truong ao...
    python -m venv %VENV_NAME%
)

:: --- BUOC 3: KICH HOAT ---
echo [2/4] Dang kich hoat moi truong...
call %VENV_NAME%\Scripts\activate

:: --- BUOC 4: CAI DAT (CHE DO GON) ---
:: Cài đặt pip mới (thêm -q để ẩn chữ)
echo [3/4] Dang cap nhat Pip...
python -m pip install --upgrade pip -q

:: Cài đặt Streamlit (thêm -q để ẩn danh sách dài dòng)
echo [4/4] Dang tai va cai dat Streamlit...
echo        (Qua trinh nay se mat 1-2 phut, man hinh se tam dung, vui long cho)...
pip install -r requirements.txt -q

:: Kiem tra xem cai dat co thanh cong khong
if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo    CAI DAT HOAN TAT THANH CONG!
    echo ====================================
) else (
    echo.
    echo [LOI] Co loi xay ra trong qua trinh cai dat.
)

echo.
pause