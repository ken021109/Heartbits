@echo off

:: --- BUOC 1: KIEM TRA MOI TRUONG ---
if not exist venv (
    echo [LOI] Khong tim thay thu muc 'venv'.
    echo Vui long chay file cai dat [setup.bat] truoc.
    pause
    exit /b
)

:: --- BUOC 2: KIEM TRA FILE DATA ---
if not exist healthcare-dataset-stroke-data.csv (
    echo [LOI] Khong tim thay file du lieu 'healthcare-dataset-stroke-data.csv'.
    echo Vui long dam bao file CSV nam cung thu muc voi file bat nay.
    pause
    exit /b
)

:: --- BUOC 3: KIEM TRA FILE CODE TRAIN ---
if not exist training_logicstic.py (
    echo [LOI] Khong tim thay file 'training_logicstic.py'.
    pause
    exit /b
)

:: --- BUOC 4: TIEN HANH HUAN LUYEN ---
echo [THONG BAO] Dang kich hoat moi truong ao va huan luyen mo hinh AI...
echo ------------------------------------------------------------------
call venv\Scripts\activate

:: Chạy script training
python training_logicstic.py

echo ------------------------------------------------------------------
echo [HOAN THANH] Mo hinh da duoc huan luyen va dong goi thanh cong.
echo Bay gio ban co the chay file [run.bat] de mo ung dung.
pause