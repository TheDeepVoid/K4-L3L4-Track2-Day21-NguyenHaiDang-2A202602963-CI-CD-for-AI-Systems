# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

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

**Lý do:** Bộ này có f1_score cao nhất trong 5 lần chạy (0,7163) nên được chọn để đi vào Bước 2. Lần chạy 4 và lần chạy 1 có accuracy trùng nhau (0,8780) nhưng f1_score khác nhau (0,7163 so với 0,7109), chứng tỏ accuracy không phân biệt được chất lượng thực của mô hình trên lớp thiểu số. Lần chạy 2 với n_estimators=50, learning_rate=0.05, max_depth=2 chỉ đạt f1 0,6051 và sẽ bị quality gate chặn, cho thấy gradient boosting quá yếu khi số cây ít và quá nông. Quan sát thấy đánh đổi giữa n_estimators và learning_rate: giảm learning_rate xuống 0,05 buộc phải tăng n_estimators lên 300 (lần 4 tốt nhất) trong khi learning_rate=0.2 với cùng 200 cây cho f1 thấp hơn (lần 5) do mỗi cây đóng góp quá mạnh và làm mô hình quá khớp.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập Adult có phân bố lớp mất cân bằng: chỉ khoảng 24,8% mẫu thuộc lớp thu nhập trên 50K, tức là tỷ lệ lớp xấp xỉ 75/25. Một mô hình không học gì mà luôn trả lời "thu nhập thấp" sẽ đạt accuracy 0,752 — con số trông khá cao nhưng mô hình hoàn toàn vô dụng vì không bắt được một trường hợp thu nhập cao nào, f1_score của lớp dương bằng 0. F1 của lớp dương đo khả năng tìm ra đúng các mẫu thu nhập cao (sự cân bằng giữa độ chính xác và độ phủ của lớp thiểu số), trong khi accuracy chỉ phản ánh tỷ lệ dự đoán đúng chung và bị lớp đa số chi phối. Vì vậy lab này lấy f1_score làm chỉ số quyết định với ngưỡng 0,65. Khi gọi f1_score không dùng average="weighted" hay average="macro" vì hai kiểu trung bình này pha lẫn đóng góp của lớp đa số, làm giá trị bị kéo lên cao và mất ý nghĩa của ngưỡng: một mô hình luôn đoán lớp thấp có weighted F1 khoảng 0,65 dù vô dụng.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow báo lỗi ImportError với SQLAlchemy 2.1.3 | MLflow 2.13 không tương thích với bản SQLAlchemy mới hơn 2.0 | Ghim `sqlalchemy==2.0.36` trong requirements.txt |
| `az vm create` thất bại với SkuNotAvailable ở malaysiawest | Standard_B1s hết chỗ trống trong khu vực Malaysia West | Chuyển sang Standard_B2ats_v2 (size free-tier, còn trống trong khu vực) |
| Bước Upload model trong pipeline fail với KeyError ARTIFACT_BUCKET | Secret chỉ được nạp vào env của bước Authenticate | Thêm `env: ARTIFACT_BUCKET` vào step Upload model trong workflow |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
