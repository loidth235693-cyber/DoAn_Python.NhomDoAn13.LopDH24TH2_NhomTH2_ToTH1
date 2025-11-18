# connect_db.py
import pyodbc
from tkinter import messagebox

# ====== CẤU HÌNH KẾT NỐI ======
DB_CONFIG = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",  # driver mặc định
    "SERVER": r"SUA\SQLEXPRESS",                 # dùng raw string để tránh escape
    "DATABASE": "QLHOCSINH_1_9",                # tên cơ sở dữ liệu
    "UID": "sa",                                # tên tài khoản SQL
    "PWD": "sql2017"                            # mật khẩu SQL
}

def connect_db():
    """
    Kết nối SQL Server, trả về conn hoặc None nếu lỗi
    """
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['DRIVER']};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            f"UID={DB_CONFIG['UID']};"
            f"PWD={DB_CONFIG['PWD']};"
        )
        conn = pyodbc.connect(conn_str, autocommit=True)
        return conn
    except Exception as e:
        messagebox.showerror("❌ Lỗi kết nối CSDL", str(e))
        return None
