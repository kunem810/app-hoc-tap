from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu trúc dữ liệu kết quả mà Trang web sẽ gửi về cho Python
class KetQuaHocTap(BaseModel):
    cau_hoi: str
    dap_an_chon: str
    ket_qua: str  # "Đúng" hoặc "Sai"

def khoi_tao_database():
    ket_noi = sqlite3.connect("ngan_hang_hoc_tap.db")
    con_tro = ket_noi.cursor()
    
    # 1. Bảng chứa câu hỏi (Đã làm ở bài trước)
    con_tro.execute("""
        CREATE TABLE IF NOT EXISTS cau_hoi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mon_hoc TEXT,
            chu_de TEXT,
            cau_hoi TEXT,
            lua_chon_1 TEXT,
            lua_chon_2 TEXT,
            lua_chon_3 TEXT,
            dap_an_dung TEXT
        )
    """)
    
    # 2. BẢNG MỚI: Lưu lịch sử làm bài để bố mẹ theo dõi năng lực của con
    con_tro.execute("""
        CREATE TABLE IF NOT EXISTS lich_su_lam_bai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay_thang TEXT,
            cau_hoi TEXT,
            dap_an_chon TEXT,
            ket_qua TEXT
        )
    """)
    
    # Nạp câu hỏi mẫu nếu bảng trống
    con_tro.execute("SELECT COUNT(*) FROM cau_hoi")
    if con_tro.fetchone()[0] == 0:
        cac_cau_mau = [
            ("Toán", "Chủ đề 1", "Tính nhẩm: 7 x 6 = ?", "36", "42", "48", "42"),
            ("Toán", "Chủ đề 1", "Một hình vuông có cạnh dài 5cm. Chu vi hình vuông đó là?", "15 cm", "20 cm", "25 cm", "20 cm"),
            ("Toán", "Chủ đề 1", "Số liền sau của số 999 là số nào?", "998", "1000", "1001", "1000")
        ]
        con_tro.executemany("""
            INSERT INTO cau_hoi (mon_hoc, chu_de, cau_hoi, lua_chon_1, lua_chon_2, lua_chon_3, dap_an_dung)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, cac_cau_mau)
        print("-> Đã nạp thành công câu hỏi mẫu vào Database!")
    
    ket_noi.commit()
    ket_noi.close()

khoi_tao_database()

# API 1: Gửi câu hỏi cho trang web (Đã làm ở bài trước)
@app.get("/lay-cau-hoi")
def gui_cau_hoi_cho_be():
    ket_noi = sqlite3.connect("ngan_hang_hoc_tap.db")
    con_tro = ket_noi.cursor()
    con_tro.execute("SELECT cau_hoi, lua_chon_1, lua_chon_2, lua_chon_3, dap_an_dung FROM cau_hoi")
    du_lieu_goc = con_tro.fetchall()
    ket_noi.close()
    
    danh_sach_cau_hoi = []
    for dong in du_lieu_goc:
        cấu_trúc_câu = {
            "cauHoi": dong[0],
            "dapAn": [dong[1], dong[2], dong[3]],
            "dapAnDung": dong[4]
        }
        danh_sach_cau_hoi.append(cấu_trúc_câu)
    return danh_sach_cau_hoi

# API 2: Tiếp nhận kết quả làm bài của bé và cất vào két sắt
@app.post("/luu-ket-qua")
def luu_ket_qua_lam_bai(du_lieu: KetQuaHocTap):
    # SỬA LẠI CHÍNH XÁC TÊN FILE Ở DÒNG DƯỚI ĐÂY:
    ket_noi = sqlite3.connect("ngan_hang_hoc_tap.db") 
    con_tro = ket_noi.cursor()
    
    thoi_gian_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    con_tro.execute("""
        INSERT INTO lich_su_lam_bai (ngay_thang, cau_hoi, dap_an_chon, ket_qua)
        VALUES (?, ?, ?, ?)
    """, (thoi_gian_hien_tai, du_lieu.cau_hoi, du_lieu.dap_an_chon, du_lieu.ket_qua))
    
    ket_noi.commit()
    ket_noi.close()
    return {"status": "Thành công", "message": "Đã ghi nhận kết quả của bé!"}