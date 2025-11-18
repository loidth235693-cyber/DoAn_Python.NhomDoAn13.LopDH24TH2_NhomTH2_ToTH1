# main.py
import tkinter as tk
from tkinter import messagebox
import datetime
from connect_db import connect_db  # import trực tiếp hàm

import font  # import module font để sử dụng cấu hình giao diện
# ====== LOG ĐĂNG NHẬP ======
def log_login(user, success):
    conn = connect_db()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO NHAT_KY(TenDangNhap, ThoiGian, ThanhCong) VALUES (?, ?, ?)",
            (user, datetime.datetime.now(), int(success))
        )
        conn.commit()
    except Exception as e:
        print("Lỗi log login:", e)
    finally:
        conn.close()

# ====== KIỂM TRA LOGIN ======
def check_login(user, password):
    conn = connect_db()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        # Chuyển user thành chữ thường khi truy vấn
        cur.execute(
            "SELECT VaiTro, MaLienKet, TrangThai, MatKhau FROM TAIKHOAN WHERE LOWER(TenDangNhap)=?",
            (user.lower(),)
        )
        row = cur.fetchone()
        if not row:
            return None

        role, ma_lienket, trang_thai, matkhau = row

        if trang_thai == 0:
            return "LOCKED"

        # So sánh mật khẩu không phân biệt hoa/thường
        if password.lower() == matkhau.lower():
            return (role, ma_lienket)
        else:
            return None
    except Exception as e:
        messagebox.showerror("Lỗi SQL", str(e))
        return None
    finally:
        conn.close()

# ====== MỞ GIAO DIỆN THEO VAI TRÒ ======
def open_interface(role, ma_lienket):
    try:
        if role == "ADMIN":
            from giaodien.admin import admin_window
            admin_window()
        elif role == "GVBM":
            from giaodien.gvbm import gvbm_window
            gvbm_window(ma_lienket)
        elif role == "GVCN":
            from giaodien.gvcn import gvcn_window
            gvcn_window(ma_lienket)
        elif role == "HOCSINH":
            from giaodien.hocsinh import hocsinh_window
            hocsinh_window(ma_lienket)
        else:
            messagebox.showerror("Lỗi vai trò", f"Không nhận dạng được vai trò: {role}")
    except ImportError as e:
        messagebox.showerror("Lỗi giao diện", f"Module giao diện không tồn tại: {e}")
    except Exception as e:
        messagebox.showerror("Lỗi giao diện", f"Khởi tạo giao diện thất bại: {e}")
    
# ====== HÀM LOGIN ======
def login():
    user = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not user or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ tên đăng nhập và mật khẩu!")
        return

    result = check_login(user, password)
    if result == "LOCKED":
        messagebox.showerror("Tài khoản bị khóa", "Tài khoản của bạn đã bị khóa, liên hệ quản trị viên.")
        log_login(user, False)
    elif result:
        role, ma_lienket = result
        messagebox.showinfo("Đăng nhập thành công", f"Xin chào {user} ({role})!")
        log_login(user, True)
        main_window.destroy()
        open_interface(role, ma_lienket)
    else:
        messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng!")
        log_login(user, False)

# ====== ĐIỀU HƯỚNG BÀN PHÍM ======
def focus_next_widget(event, next_widget):
    next_widget.focus()
    return "break"

def focus_prev_widget(event, prev_widget):
    prev_widget.focus()
    return "break"

# ====== GIAO DIỆN TKINTER ======
main_window = tk.Tk()
main_window.title("🎓 Đăng nhập hệ thống quản lý học sinh")
main_window.geometry("420x340")
main_window.configure(bg="#E8F4FB")
main_window.resizable(False, False)

# --- Tiêu đề ---
tk.Label(
    main_window, text="🎓 ĐĂNG NHẬP HỆ THỐNG",
    font=("Times New Roman", 17, "bold"),
    bg="#E8F4FB", fg="#0A3D62"
).pack(pady=25)

# --- Ô nhập tài khoản ---
tk.Label(main_window, text="Tên đăng nhập:", bg="#E8F4FB", font=("Times New Roman", 13)).pack(pady=5)
entry_user = tk.Entry(main_window, width=30, font=("Times New Roman", 12))
entry_user.pack()
entry_user.focus()

# --- Ô nhập mật khẩu ---
tk.Label(main_window, text="Mật khẩu:", bg="#E8F4FB", font=("Times New Roman", 13)).pack(pady=5)
entry_pass = tk.Entry(main_window, width=30, show="*", font=("Times New Roman", 12))
entry_pass.pack()

# --- Checkbox hiện mật khẩu ---
show_pass = tk.BooleanVar()
tk.Checkbutton(
    main_window, text="Hiện mật khẩu", bg="#E8F4FB", variable=show_pass,
    command=lambda: entry_pass.config(show="" if show_pass.get() else "*")
).pack(pady=5)

# --- Nút đăng nhập ---
tk.Button(
    main_window, text="Đăng nhập", command=login,
    bg="#0A3D62", fg="white",
    font=("Times New Roman", 13, "bold"), width=15
).pack(pady=15)

# ====== RÀNG BUỘC PHÍM ======
entry_user.bind("<Return>", lambda e: focus_next_widget(e, entry_pass))
entry_pass.bind("<Return>", lambda e: login())
entry_pass.bind("<Up>", lambda e: focus_prev_widget(e, entry_user))
entry_user.bind("<Down>", lambda e: focus_next_widget(e, entry_pass))

main_window.mainloop()
