@echo off

:: --- BUOC 1: KIEM TRA MOI TRUONG ---
if not exist .venv (
    echo [LOI] Khong tim thay thu muc 'venv'.
    echo Vui long chay file cai dat [setup.bat] truoc
    pause
    exit /b
)

:: --- BUOC 2: KIEM TRA FILE CODE ---
if not exist app.py (
    echo [LOI] Khong tim thay file 'app.py'.
    echo Vui long kiem tra xem ban da co file code chua.
    pause
    exit /b
)

:: --- BUOC 3: CHAY UNG DUNG ---
echo [THONG BAO] Dang kich hoat moi truong ao...
call venv\Scripts\activate

echo [THONG BAO] Dang khoi dong Streamlit...
echo             Trinh duyet se tu dong mo trong giay lat.
echo             Nhan Ctrl+C trong cua so nay neu muon dung chuong trinh.
echo ------------------------------------------------------------------

:: Chạy ứng dụng
streamlit run app.py

:: Giữ màn hình lại nếu chương trình bị tắt đột ngột
pause