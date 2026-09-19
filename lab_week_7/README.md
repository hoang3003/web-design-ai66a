# Lab Week 7 - FastAPI: Routing, Request and Response

Ứng dụng quản lý Items sử dụng FastAPI ở backend và HTML/CSS/JavaScript thuần ở frontend. Dữ liệu được lưu trong bộ nhớ và sẽ bị xóa khi server khởi động lại.

## 1. Tạo và kích hoạt môi trường ảo

Mở PowerShell tại thư mục `lab_week_7`, sau đó chạy:

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Trên macOS hoặc Linux, kích hoạt môi trường bằng:

```bash
source .venv/bin/activate
```

## 2. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

## 3. Chạy FastAPI bằng Uvicorn

Chạy lệnh sau khi terminal đang ở thư mục `Backend`:

```powershell
uvicorn main:app --reload
```

Server mặc định chạy tại `http://127.0.0.1:8000`.

## 4. Truy cập Swagger

Mở `http://127.0.0.1:8000/docs` để xem tài liệu và thử trực tiếp tất cả API.

## 5. Test API

Cách đơn giản nhất là dùng nút **Try it out** trong Swagger. Cũng có thể dùng `curl.exe` trong một cửa sổ PowerShell khác.

Tạo item:

```powershell
curl.exe -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" -d '{"name":"Laptop","price":1500}'
```

Lấy danh sách, tìm kiếm, sắp xếp và phân trang:

```powershell
curl.exe "http://127.0.0.1:8000/items?q=lap&min_price=100&sort_by=price&order=desc&skip=0&limit=10"
```

Cập nhật một phần item:

```powershell
curl.exe -X PATCH http://127.0.0.1:8000/items/1 -H "Content-Type: application/json" -d '{"price":1400}'
```

Dự đoán giá nhà:

```powershell
curl.exe -X POST http://127.0.0.1:8000/predict/house-price -H "Content-Type: application/json" -d '{"area_sqm":80,"bedrooms":3,"distance_to_center_km":5}'
```

Các API còn lại có thể được kiểm tra tại Swagger, gồm GET theo ID, PUT, PATCH và DELETE.

## 6. Sử dụng giao diện frontend

Trong khi Uvicorn đang chạy, mở:

`http://127.0.0.1:8000/static/`

Nhấn **Fetch data** để lấy danh sách item. Mỗi dòng có nút **Delete** để xóa item tương ứng. Hãy tạo một vài item bằng Swagger hoặc API POST trước nếu danh sách đang trống.
