I. YÊU CẦU HỆ THỐNG

1. Máy tính đang sử dụng Windows 10/11
2. Máy tính đã cài đặt Python (Phiên bản 3.9 trở lên, khuyến kích sử dụng bản 3.11).
3. Khi cài đặt Python, hãy đảm bảo đã tích chọn vào ô:
   "Add Python to PATH" (Để có thể chạy lệnh Python từ cửa sổ lệnh).

II. CÁC BƯỚC THỰC HIỆN


BƯỚC 1: CÀI ĐẶT MÔI TRƯỜNG (Chỉ cần làm lần đầu tiên)
- Tìm file có tên là 'setup.bat'.
- Nhấp đúp chuột vào file này.
- Chương trình sẽ tự động:
    + Tạo môi trường ảo (thư mục 'venv') để giữ cho máy tính sạch sẽ.
    + Cập nhật công cụ cài đặt (Pip).
    + Cài đặt thư viện Streamlit.
- Lưu ý: Trong quá trình cài đặt, màn hình có thể sẽ tạm dừng khoảng 1-2
  phút (do đang tải dữ liệu ngầm). Vui lòng đợi cho đến khi hiện thông báo
  "CAI DAT HOAN TAT THANH CONG!".

BƯỚC 3: HUẤN LUYỆN MÔ HÌNH (Có thể bỏ qua vì mô hình đã có sẵn)
- Sau khi cài đặt xong ở Bước 1, tìm file 'training.bat'.
- Nhấp đúp chuột vào file này.
- Sau khi chạy xong sẽ có 2 file: `stroke\_final\_model.pkl` và `preprocessor\_meta.pkl`.

BƯỚC 3: CHẠY ỨNG DỤNG
- Sau khi cài đặt xong ở Bước 1, tìm file 'run.bat'.
- Nhấp đúp chuột vào file này.
- Một cửa sổ lệnh sẽ hiện ra và trình duyệt web sẽ tự động mở trang web
  của ứng dụng (thường là địa chỉ http://localhost:8501).

III. CẤU TRÚC THƯ MỤC DỰ ÁN

stroke_alert_vn/
├── app.py                              ← Mã nguồn ứng dụng chính
├── train_model.py                      ← Mã nguồn huấn luyện model
├── requirements.txt                    ← Danh sách thư viện
├── readme.txt                          ← Tài liệu hướng dẫn cài đặt
├── healthcare-dataset-stroke-data.csv  ← Dataset Kaggle (đã có sẵn)
├── stroke_final_model.pkl              ← Tự động tạo sau khi train (đã có sắn)
└── preprocessor_meta.pkl               ← Tự động tạo sau khi train (đã có sẵn)
└── setup.bat                           ← Script cài đặt ban đầu.
└── run.bat                             ← Script khởi động ứng dụng nhanh
└── training.bat                        ← Script huấn luyện mô hình
└── venv/                               ← Thư mục chứa môi trường ảo (tự động tạo ra)

IV. XỬ LÝ LỖI THƯỜNG GẶP

1. Lỗi "Python không được tìm thấy":
   Hãy cài lại Python và nhớ tích chọn "Add Python to PATH".
 
2. Lỗi không chạy được ứng dụng:
   Hãy chắc chắn bạn đã chạy file 'setup.bat' trước khi chạy 'run.bat' và 'training.bat'.

3. Muốn dừng ứng dụng:
   Đóng trình duyệt hoặc quay lại cửa sổ lệnh và nhấn tổ hợp phím Ctrl + C.