# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Hải Đăng |
| MSSV | 2A202602963 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/TheDeepVoid/K4-L3L4-Track2-Day21-NguyenHaiDang-2A202602963-CI-CD-for-AI-Systems |
| Ngày nộp | 07/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |
| 4 | 300 | 0.05 | 3 | 0.7163 | 0.8780 |
| 5 | 200 | 0.2 | 3 | 0.7032 | 0.8700 |

**Bộ siêu tham số đã chọn:** `n_estimators=300`, `learning_rate=0.05`, `max_depth=3`.

**Lý do:** Bộ này có f1_score cao nhất trong 5 lần chạy nên được chọn cho Bước 2. Lần 1 có accuracy bằng lần 4 (0,8780) nhưng f1 thấp hơn (0,7109), chứng tỏ accuracy không đo được chất lượng trên lớp thiểu số. Lần 2 chỉ đạt f1 0,6051 nên bị quality gate chặn vì quá ít cây và quá nông. Giảm learning_rate buộc phải tăng n_estimators để bù; learning_rate=0.2 làm mô hình quá khớp nên f1 thấp hơn.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập Adult mất cân bằng lớp: chỉ khoảng 24,8% mẫu có thu nhập trên 50K. Mô hình luôn đoán "thu nhập thấp" đạt accuracy 0,752 nhưng vô dụng vì f1_score của lớp dương bằng 0. F1 đo khả năng tìm đúng các mẫu thu nhập cao, còn accuracy bị lớp đa số chi phối, nên lab lấy f1_score với ngưỡng 0,65 làm chỉ số quyết định. Không dùng average="weighted" hay "macro" vì trung bình đó pha lẫn lớp đa số: mô hình đoán toàn lớp thấp vẫn có weighted F1 khoảng 0,65.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow báo ImportError với SQLAlchemy 2.1.3 | MLflow 2.13 không tương thích SQLAlchemy mới hơn 2.0 | Ghim `sqlalchemy==2.0.36` trong requirements.txt |
| `az vm create` thất bại SkuNotAvailable ở malaysiawest | Standard_B1s hết chỗ trong Malaysia West | Chuyển sang Standard_B2ats_v2 (free-tier, còn trống) |
| Upload model fail KeyError ARTIFACT_BUCKET | Secret chỉ nạp vào env của bước Authenticate | Thêm `env: ARTIFACT_BUCKET` vào step Upload model |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`, 22.361 mẫu) | 0,7163 | 0,8780 |
| Bước 3 (thêm `train_batch2`, 44.722 mẫu) | 0,7431 | 0,8880 |

**Nhận xét:** Cả hai chỉ số đều tăng: f1_score thêm 0,0268, accuracy thêm 0,0100. Hai nửa dữ liệu cùng phân phối nên mức tăng chủ yếu do mô hình thấy nhiều mẫu hơn để ước tính chính xác ranh giới quyết định, dữ liệu mới không khó hơn; với cùng phân phối, kết quả thường chỉ dao động trong khoảng nhỏ. Quan trọng nhất, commit dữ liệu đã kích hoạt pipeline, mô hình mới qua quality gate và được triển khai lên VM không cần can thiệp thủ công.
