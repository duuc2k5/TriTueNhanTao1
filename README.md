# Tìm Đường Đi Tối Ưu Trên Bản Đồ Địa Hình Bằng Thuật Toán A*

## 📋 Mô Tả Bài Toán

Bài toán tìm con đường tối ưu từ điểm xuất phát đến điểm đích trên một bản đồ địa hình 3D. Độ khó di chuyển phụ thuộc vào độ cao của địa hình, đặc biệt là độ dốc giữa các điểm liền kề.

### Đặc Điểm Chính:
- **Terrain (Địa hình)**: Lưới 50×50 điểm với độ cao từ 0 đến 1000 mét
- **Chi phí di chuyển**: Phụ thuộc vào độ dốc
  - Đi lên: chi phí = 2.0 × (độ cao chênh lệch)
  - Đi xuống: chi phí = 0.5 × (độ cao chênh lệch)
  - Di chuyển ngang: chi phí = 1.0
- **Điểm xuất phát**: (0, 0) - góc dưới bên trái
- **Điểm đích**: (49, 49) - góc trên bên phải

## 🎯 Mục Tiêu

So sánh hiệu suất của **3 heuristic hàm** khác nhau trong thuật toán A*:

### 1. **Euclidean Distance** (Khoảng cách Euclide)
```python
h(pos) = √((x_goal - x)² + (y_goal - y)²)
```
- Đơn giản, phổ biến nhất
- Cho ước tính tương đối cân bằng

### 2. **Manhattan Distance** (Khoảng cách Manhattan)
```python
h(pos) = |x_goal - x| + |y_goal - y|
```
- Phù hợp cho lưới chỉ cho phép di chuyển 4 hướng
- Thường ít chính xác hơn Euclidean cho lưới 8 hướng

### 3. **Custom Heuristic** (Heuristic Tùy Chỉnh)
```python
h(pos) = max(0.5 × horizontal_distance, 0.5 × |height_difference|)
```
- Tính đến yếu tố độ cao của địa hình
- Được thiết kế đặc biệt cho bài toán này

## 🔧 Cách Sử Dụng

### Yêu Cầu:
```
numpy
matplotlib
```

### Chạy chương trình:
```bash
python TriTueNhanTao.py
```

### Output:
- **Bảng so sánh**: In ra bảng kết quả của 3 heuristic
- **Hình ảnh**: `terrain_paths.png` (2 hình)
  - Trái: Bản đồ địa hình 2D với đường đi
  - Phải: Mô hình 3D địa hình

## 📊 Kết Quả So Sánh

Chương trình đánh giá 3 tiêu chí:

| Tiêu Chí | Ý Nghĩa |
|----------|---------|
| **Chi phí** | Tổng chi phí của con đường (thấp nhất tốt) |
| **Số bước** | Số lượng bước di chuyển |
| **Số nút mở rộng** | Số lượng nút được khám phá bởi A* (thấp nhất tốt) |
| **Thời gian** | Thời gian thực thi (nhanh nhất tốt) |

## 🚀 Các Hàm Chính

### `generate_terrain(size, seed)`
- Tạo bản đồ địa hình bằng kết hợp các sóng sine/cosine và nhiễu Gaussian
- Đảm bảo độ cao nằm trong khoảng [0, 1000]

### `move_cost(terrain, current, next)`
- Tính chi phí di chuyển giữa 2 điểm liền kề
- Tính đến độ dốc: đi lên gấp đôi chi phí, đi xuống bằng nửa chi phí

### `astar(terrain, start, goal, heuristic_name)`
- Triển khai thuật toán A*
- Trả về: đường đi, chi phí, số nút mở rộng, thời gian thực thi

### `plot_results(terrain, results)`
- Vẽ bản đồ 2D và 3D
- Hiển thị đường đi của cả 3 heuristic để so sánh

## 🔍 Phân Tích

### Khi nào heuristic nào tốt nhất?
- **Euclidean**: Cân bằng tốt giữa độ chính xác và tốc độ
- **Manhattan**: Thường kém hiệu quả cho bài toán này vì địa hình là 8-neighbors
- **Custom**: Thường tốt nhất vì kết hợp yếu tố địa hình vào heuristic

### Ứng Dụng Thực Tế:
- Lập kế hoạch chuyển động cho robot trên địa hình
- Trò chơi: tìm đường cho NPC trên bản đồ có độ cao
- Định tuyến xe trên đất núi

## 📝 Ghi Chú

- Seed được đặt cố định (seed=7) để có kết quả lặp lại được
- Bản đồ được tạo bằng công thức toán học để đảm bảo tính nhất quán
- A* được triển khai với closed set để tránh khám phá lại nút

---

**Tác Giả**: Dự án Trí Tuệ Nhân Tạo  
**Ngôn Ngữ**: Python 3.7+  
**Thư viện**: NumPy, Matplotlib
