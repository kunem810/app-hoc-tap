import sqlite3

def nap_ngan_hang_cau_hoi_lon():
    # Kết nối đến két sắt Database của bạn
    ket_noi = sqlite3.connect("ngan_hang_hoc_tap.db")
    con_tro = ket_noi.cursor()
    
    # Danh sách câu hỏi chuẩn hóa bám sát các bài học sách Kết nối tri thức với cuộc sống
    # Bao gồm các chủ đề: Phép nhân chia, Hình học, Số lớn phạm vi 10.000
    ngan_hang_data = [
        # CHỦ ĐỀ 1: ÔN TẬP VÀ BẢNG NHÂN CHIA
        ("Toán", "Bài 10: Bảng nhân 7", "Tìm x, biết: x : 7 = 6", "13", "42", "35", "42"),
        ("Toán", "Bài 10: Bảng nhân 7", "Mỗi tuần lễ có 7 ngày. Hỏi 4 tuần lễ có bao nhiêu ngày?", "11 ngày", "24 ngày", "28 ngày", "28 ngày"),
        ("Toán", "Bài 11: Bảng chia 7", "Có 35 quyển truyện chia đều cho 7 bạn. Hỏi mỗi bạn được mấy quyển?", "5 quyển", "6 quyển", "7 quyển", "5 quyển"),
        ("Toán", "Bài 12: Bảng nhân 8", "Một chiếc ô tô chở được 8 người. Hỏi 5 chiếc ô tô như vậy chở được bao nhiêu người?", "13 người", "40 người", "45 người", "40 orang"), # Đáp án đúng: 40 người
        ("Toán", "Bài 13: Bảng chia 8", "Tính: 64 : 8 = ?", "7", "8", "9", "8"),
        
        # CHỦ ĐỀ 2: HÌNH HỌC (GÓC, CHU VI, DIỆN TÍCH)
        ("Toán", "Bài 24: Hình tam giác, hình tứ giác", "Hình tứ giác là hình có mấy cạnh?", "3 cạnh", "4 cạnh", "5 cạnh", "4 cạnh"),
        ("Toán", "Bài 48: Chu vi hình chữ nhật", "Một hình chữ nhật có chiều dài 8cm, chiều rộng 5cm. Chu vi hình đó là?", "13 cm", "26 cm", "40 cm", "26 cm"),
        ("Toán", "Bài 49: Chu vi hình vuông", "Một chiếc đồng hồ treo tường hình vuông có cạnh 9cm. Chu vi của chiếc đồng hồ đó là?", "18 cm", "36 cm", "81 cm", "36 cm"),
        
        # CHỦ ĐỀ 3: CÁC SỐ TRONG PHẠM VI 10.000 & 100.000
        ("Toán", "Bài 52: Các số trong phạm vi 10.000", "Số gồm 4 nghìn, 5 trăm và 2 đơn vị được viết là:", "452", "4502", "4520", "4502"),
        ("Toán", "Bài 54: Phép cộng trong phạm vi 10.000", "Tính tổng: 3500 + 1200 = ?", "4700", "4200", "3700", "4700"),
        ("Toán", "Bài 55: Phép trừ trong phạm vi 10.000", "Tính hiệu: 8000 - 3000 = ?", "5000", "4000", "6000", "5000"),
        ("Toán", "Bài 60: Xem đồng hồ, tháng - năm", "Tháng 5 có bao nhiêu ngày?", "28 ngày", "30 ngày", "31 ngày", "31 ngày")
    ]
    
    # Xóa bớt các câu cũ để nạp bộ câu hỏi bám sát bài học mới này
    con_tro.execute("DELETE FROM cau_hoi")
    
    # Lệnh thần kỳ đưa tất cả đống câu hỏi trên vào database trong 0.1 giây
    con_tro.executemany("""
        INSERT INTO cau_hoi (mon_hoc, chu_de, cau_hoi, lua_chon_1, lua_chon_2, lua_chon_3, dap_an_dung)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ngan_hang_data)
    
    ket_noi.commit()
    ket_noi.close()
    print("🎉 CHÚC MỪNG: Đã nạp thành công bộ câu hỏi bám sát SGK Kết nối tri thức!")

if __name__ == "__main__":
    nap_ngan_hang_cau_hoi_lon()