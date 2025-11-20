# gvcn.py
import tkinter as tk
from tkinter import IntVar, ttk, messagebox
from tkinter import filedialog
import pandas as pd
from tkcalendar import DateEntry
from datetime import datetime
from connect_db import connect_db
import font

def gvcn_window(magv):
    gvcn_window = tk.Tk()
    gvcn_window.title("Giao diện GVCN")
    gvcn_window.geometry("1200x700")
    gvcn_window.configure(bg=font.BG_COLOR)
    
    style = ttk.Style()
    style.theme_use('default') 
    style.configure('TNotebook.Tab', background="#E8F4FB", foreground='black', padding=[10, 5])

    for i in range(4):
        gvcn_window.grid_rowconfigure(i, weight=1)
    gvcn_window.grid_columnconfigure(0, weight=1)
    
    # ===== Tiêu đề =====
    title_label = tk.Label(
        gvcn_window, text="HỆ THỐNG QUẢN LÝ HỌC SINH",
        font=font.FONT_TIEUDE, bg="#E8F4FB", fg="#0A3D62", pady=10
    )
    title_label.grid(row=0, column=0, sticky="ew")
    gvcn_window.grid_columnconfigure(0, weight=1)

    gvcn_window.grid_rowconfigure(1, weight=1)
    gvcn_window.grid_columnconfigure(0, weight=1)

    # ===== Khung chính =====
    frame_cha = tk.Frame(gvcn_window, bg=font.BG_COLOR)
    frame_cha.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
    frame_cha.grid_columnconfigure((0,1,2), weight=1, uniform="col")

    # ---------------- Frame HS ----------------
    frame_hs = ttk.LabelFrame(frame_cha, text="Thông tin học sinh", padding=10)
    frame_hs.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    for i in range(8): frame_hs.grid_rowconfigure(i, weight=1)
    frame_hs.grid_columnconfigure(0, weight=0)
    frame_hs.grid_columnconfigure(1, weight=2)

    labels_hs = ["Mã HS:", "Họ:", "Tên lót:", "Tên:", "Giới tính:", "Ngày sinh:", "Lớp:", "Tình trạng:"]
    entries_hs = []

    for i, text in enumerate(labels_hs):
        tk.Label(frame_hs, text=text, width=12, anchor="e",
                 bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=i, column=0, padx=5, pady=5)
        if text == "Giới tính:":
            combo = ttk.Combobox(frame_hs, values=["Nam", "Nữ"], width=18, state="readonly")
            combo.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries_hs.append(combo)
        elif text == "Ngày sinh:":
            date_entry = DateEntry(frame_hs, width=18)
            date_entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries_hs.append(date_entry)
        elif text == "Lớp:":
            combo_lop = ttk.Combobox(frame_hs, values=["10A1","10A2","11A1","11A2","12A1","12A2"], width=18, state="readonly")
            combo_lop.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries_hs.append(combo_lop)
        elif text == "Tình trạng:":
            combo_tt = ttk.Combobox(frame_hs, values=["Đang học","Bảo lưu","Nghỉ học"], width=18, state="readonly")
            combo_tt.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries_hs.append(combo_tt)
        else:
            e = tk.Entry(frame_hs, width=20)
            e.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries_hs.append(e)

    # ---------------- Frame Điểm ----------------
    frame_diem = ttk.LabelFrame(frame_cha, text="Điểm học kỳ", padding=10)
    frame_diem.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    frame_diem.grid_rowconfigure(0, weight=0)
    frame_diem.grid_columnconfigure(0, weight=1)

    notebook_hk = ttk.Notebook(frame_diem)
    notebook_hk.grid(row=0, column=0, sticky="ew")

    tab_hk1 = ttk.Frame(notebook_hk)
    tab_hk2 = ttk.Frame(notebook_hk)
    notebook_hk.add(tab_hk1, text="Học kỳ 1")
    notebook_hk.add(tab_hk2, text="Học kỳ 2")

    monhoc = ["Toán","Ngữ văn","Tiếng Anh","Vật lí","Hóa học","Sinh học","Lịch sử","Địa lí","GDCD","Tin học","Công nghệ"]
    cols_bang = ["B1","B2","B3","B4"]

    def tao_bang_diem(container, monhoc, cols):
        entry_dict = {}
        tk.Label(container, text="Môn", width=12, anchor="w",
                 bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=0, padx=5, pady=2)
        for i, col in enumerate(cols):
            tk.Label(container, text=col, width=7, bg=font.BG_COLOR,
                     fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=i+1, padx=2, pady=2)
        for r, mon in enumerate(monhoc, start=1):
            container.grid_rowconfigure(r, weight=1)
            tk.Label(container, text=mon, width=12, anchor="w",
                     bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=r, column=0, padx=5, pady=2)
            for c, col in enumerate(cols):
                container.grid_columnconfigure(c+1, weight=1)
                e = tk.Entry(container, width=7, justify="center", font=font.FONT_CHU)
                e.grid(row=r, column=c+1, padx=2, pady=2, sticky="ew")
                entry_dict[f"{mon}_{col}"] = e
        return entry_dict

    entry_diem_hk1 = tao_bang_diem(tab_hk1, monhoc, cols_bang)
    entry_diem_hk2 = tao_bang_diem(tab_hk2, monhoc, cols_bang)

    # ---------------- Frame Khoản phí ----------------
    frame_phi = ttk.LabelFrame(frame_cha, text="Khoản phí & Trạng thái", padding=10)
    frame_phi.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
    for r in range(5): frame_phi.grid_rowconfigure(r, weight=0)
    for c in range(4): frame_phi.grid_columnconfigure(c, weight=1)

    var_hocphi = IntVar(value=0)
    var_bhyt = IntVar(value=0)
    var_bhtn = IntVar(value=0)

    tk.Label(frame_phi, text="Học phí:", anchor="e", width=12,
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    tk.Radiobutton(frame_phi, text="Đã đóng", variable=var_hocphi, value=1,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=1, sticky="w", padx=5)
    tk.Radiobutton(frame_phi, text="Chưa đóng", variable=var_hocphi, value=0,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=2, sticky="w", padx=5)

    tk.Label(frame_phi, text="BHYT:", anchor="e", width=12,
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Radiobutton(frame_phi, text="Đã đóng", variable=var_bhyt, value=1,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=1, column=1, sticky="w", padx=5)
    tk.Radiobutton(frame_phi, text="Chưa đóng", variable=var_bhyt, value=0,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=1, column=2, sticky="w", padx=5)
    combo_bhyt = ttk.Combobox(frame_phi, values=[3,6,12], width=10, state="disabled")
    combo_bhyt.grid(row=1, column=3, sticky="w", padx=5)

    tk.Label(frame_phi, text="BHTN:", anchor="e", width=12,
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Radiobutton(frame_phi, text="Đã đóng", variable=var_bhtn, value=1,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=2, column=1, sticky="w", padx=5)
    tk.Radiobutton(frame_phi, text="Chưa đóng", variable=var_bhtn, value=0,
                fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=2, column=2, sticky="w", padx=5)
    combo_bhtn = ttk.Combobox(frame_phi, values=[1,2,3,4], width=10, state="disabled")
    combo_bhtn.grid(row=2, column=3, sticky="w", padx=5)

    tk.Label(frame_phi, text="Tổng tiền:", anchor="e", width=12,
            bg=font.BG_COLOR, fg="#006400", font=font.FONT_CHU).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    lbl_tongtien = tk.Label(frame_phi, text="0", fg="#006400", bg=font.BG_COLOR, font=font.FONT_CHU)
    lbl_tongtien.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    # Enable/disable combobox BHYT/BHTN
    var_bhyt.trace_add("write", lambda *args: combo_bhyt.config(state="readonly" if var_bhyt.get()==1 else "disabled"))
    var_bhtn.trace_add("write", lambda *args: combo_bhtn.config(state="readonly" if var_bhtn.get()==1 else "disabled"))

    # ---------------- Frame Danh sách Học sinh ----------------
    frame_ds_hs = ttk.LabelFrame(gvcn_window, text="Danh sách học sinh", padding=(5,5))
    frame_ds_hs.grid(row=2, column=0, sticky="nsew", padx=10, pady=0)
    gvcn_window.grid_rowconfigure(1, weight=0)
    gvcn_window.grid_columnconfigure(0, weight=1)
    frame_ds_hs.grid_rowconfigure(0, weight=1)
    frame_ds_hs.grid_columnconfigure(0, weight=1)

    # NOTEBOOK danh sách học sinh
    notebook_hs = ttk.Notebook(frame_ds_hs)
    notebook_hs.grid(row=0, column=0, sticky="nsew")

    # ---------------- TAB Thông tin ----------------
    tab_info = ttk.Frame(notebook_hs)
    notebook_hs.add(tab_info, text="Thông tin")
    cols_info = ["Mã HS","Họ","Tên lót","Tên","Giới tính","Ngày sinh","Lớp","Tình trạng"]

    tree_info = ttk.Treeview(tab_info, columns=cols_info, show="headings", height=3)  # giới hạn chiều cao
    for col in cols_info:
        tree_info.heading(col, text=col)
        tree_info.column(col, width=120, anchor="center")

    scroll_info_v = ttk.Scrollbar(tab_info, orient="vertical", command=tree_info.yview)
    scroll_info_h = ttk.Scrollbar(tab_info, orient="horizontal", command=tree_info.xview)
    tree_info.configure(yscrollcommand=scroll_info_v.set, xscrollcommand=scroll_info_h.set)

    tree_info.grid(row=0, column=0, sticky="nsew")
    scroll_info_v.grid(row=0, column=1, sticky="ns")
    scroll_info_h.grid(row=1, column=0, sticky="ew")
    tab_info.grid_rowconfigure(0, weight=1)
    tab_info.grid_columnconfigure(0, weight=1)

    # ---------------- TAB Điểm ----------------
    tab_diem = ttk.Frame(notebook_hs)
    notebook_hs.add(tab_diem, text="Điểm")

    notebook_diem = ttk.Notebook(tab_diem)
    notebook_diem.grid(row=0, column=0, sticky="nsew")
    tab_hk1_tv = ttk.Frame(notebook_diem)
    tab_hk2_tv = ttk.Frame(notebook_diem)
    notebook_diem.add(tab_hk1_tv, text="Học kỳ 1")
    notebook_diem.add(tab_hk2_tv, text="Học kỳ 2")

    cols_diem = ["Mã HS","Họ tên","Lớp","Toán","Ngữ văn","Tiếng Anh","GDCD","Lịch sử",
                "Địa lí","Vật lí","Hóa học","Sinh học","Tin học","Công nghệ","TBCN","Xếp loại"]

    def create_treeview(tab, cols, height=10):
        tree = ttk.Treeview(tab, columns=cols, show="headings", height=height)  # giới hạn chiều cao
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor="center")
        scroll_v = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        scroll_h = ttk.Scrollbar(tab, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        return tree

    tree_hk1 = create_treeview(tab_hk1_tv, cols_diem, height=3)
    tree_hk2 = create_treeview(tab_hk2_tv, cols_diem, height=3)

    # ---------------- TAB Khoản phí ----------------
    tab_phi = ttk.Frame(notebook_hs)
    notebook_hs.add(tab_phi, text="Khoản phí")
    cols_phi = ["Mã HS","Họ tên","Lớp","Học phí",
                "BHYT","Tháng BHYT","BHTN","Mức BHTN","Tổng tiền"]
    tree_phi = create_treeview(tab_phi, cols_phi, height=3)

    
# ===================== HỆ THỐNG ĐIỀU HƯỚNG FULL TAB =====================

    # Gom tất cả widget của toàn TAB theo đúng thứ tự focus
    focus_list = []

    # 1) Thêm các Entry/Combo của Thông tin học sinh
    focus_list.extend(entries_hs)

    # 2) Thêm Entry điểm học kỳ 1
    for key in entry_diem_hk1:
        focus_list.append(entry_diem_hk1[key])

    # 3) Thêm Entry điểm học kỳ 2
    for key in entry_diem_hk2:
        focus_list.append(entry_diem_hk2[key])

    # 4) Thêm Khoản phí (radio + combo)
    focus_list.extend([
        combo_bhyt,
        combo_bhtn,
    ])


    # ===================== Hàm điều hướng =====================

    def focus_next(event):
        widget = event.widget
        if widget in focus_list:
            idx = focus_list.index(widget)
            if idx < len(focus_list) - 1:
                focus_list[idx + 1].focus_set()
        return "break"

    def focus_prev(event):
        widget = event.widget
        if widget in focus_list:
            idx = focus_list.index(widget)
            if idx > 0:
                focus_list[idx - 1].focus_set()
        return "break"


    # Điều hướng theo mũi tên trong bảng điểm (di chuyển 4 cột)
    def arrow_navigation(event, entry_dict, monhoc, cols):
        widget = event.widget
        if widget not in entry_dict.values():
            return

        # Tìm vị trí dòng & cột
        items = list(entry_dict.items())
        keys = list(entry_dict.keys())
        index = list(entry_dict.values()).index(widget)

        mon_index = index // len(cols)
        col_index = index % len(cols)

        # Lên
        if event.keysym == "Up" and mon_index > 0:
            new_widget = entry_dict[f"{monhoc[mon_index-1]}_{cols[col_index]}"]
            new_widget.focus_set()

        # Xuống
        elif event.keysym == "Down" and mon_index < len(monhoc)-1:
            new_widget = entry_dict[f"{monhoc[mon_index+1]}_{cols[col_index]}"]
            new_widget.focus_set()

        # Trái
        elif event.keysym == "Left" and col_index > 0:
            new_widget = entry_dict[f"{monhoc[mon_index]}_{cols[col_index-1]}"]
            new_widget.focus_set()

        # Phải
        elif event.keysym == "Right" and col_index < len(cols)-1:
            new_widget = entry_dict[f"{monhoc[mon_index]}_{cols[col_index+1]}"]
            new_widget.focus_set()

        return "break"


    # ===================== GÁN SỰ KIỆN =====================

    # Toàn bộ Entry/Combobox
    for widget in focus_list:
        widget.bind("<Return>", focus_next)
        widget.bind("<Shift-Return>", focus_prev)

    # Điều hướng mũi tên cho Thông tin học sinh & Khoản phí (nhảy tuần tự)
    for widget in entries_hs + [combo_bhyt, combo_bhtn]:
        widget.bind("<Down>", focus_next)
        widget.bind("<Up>", focus_prev)

    # Điều hướng 4 hướng trong bảng điểm
    for widget in entry_diem_hk1.values():
        widget.bind("<Up>", lambda e: arrow_navigation(e, entry_diem_hk1, monhoc, cols_bang))
        widget.bind("<Down>", lambda e: arrow_navigation(e, entry_diem_hk1, monhoc, cols_bang))
        widget.bind("<Left>", lambda e: arrow_navigation(e, entry_diem_hk1, monhoc, cols_bang))
        widget.bind("<Right>", lambda e: arrow_navigation(e, entry_diem_hk1, monhoc, cols_bang))

    for widget in entry_diem_hk2.values():
        widget.bind("<Up>", lambda e: arrow_navigation(e, entry_diem_hk2, monhoc, cols_bang))
        widget.bind("<Down>", lambda e: arrow_navigation(e, entry_diem_hk2, monhoc, cols_bang))
        widget.bind("<Left>", lambda e: arrow_navigation(e, entry_diem_hk2, monhoc, cols_bang))
        widget.bind("<Right>", lambda e: arrow_navigation(e, entry_diem_hk2, monhoc, cols_bang))

    def load_data_hs(magv):
        # Xóa dữ liệu cũ
        tree_info.delete(*tree_info.get_children())
        tree_phi.delete(*tree_phi.get_children())
        tree_hk1.delete(*tree_hk1.get_children())
        tree_hk2.delete(*tree_hk2.get_children())

        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu.")
            return

        try:
            cursor = conn.cursor()

            # ---------------- Load Bảng Thông tin học sinh lớp chủ nhiệm ----------------
            cursor.execute("""
                SELECT MAHS, HO, TENLOT, TEN, GIOITINH, NGAYSINH, LOP, TINHTRANG
                FROM HOCSINH
                WHERE LOP = (SELECT MaLop FROM LOP WHERE GVCN = ?)
                ORDER BY TEN ASC
            """, magv)

            for row in cursor.fetchall():
                row = list(row)
                if row[5]:  # NGAYSINH
                    row[5] = row[5].strftime("%d/%m/%Y")
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_info.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def load_data_phi(magv):
        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối CSDL.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.MaHS, h.HoTen, h.Lop,
                    k.HocPhi, k.BHYT, k.Thang_BHYT,
                    k.BHTN, k.Muc_BHTN, k.TongTien
                FROM HOCSINH h
                LEFT JOIN KHOANPHI k 
                    ON h.MaHS = k.MaHS AND k.NamHoc='2024-2025'
                WHERE h.Lop = (SELECT MaLop FROM LOP WHERE GVCN = ?)
                ORDER BY h.HoTen
            """, magv)

            rows = cursor.fetchall()
            tree_phi.delete(*tree_phi.get_children())
            for row in rows:
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_phi.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu khoản phí: {e}")
        finally:
            conn.close()

    def load_data_diem(treeview, hocky, magv):
        treeview.delete(*treeview.get_children())
        conn = connect_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # 1) Lấy danh sách môn học từ DB
            cursor.execute("SELECT TenMon FROM MONHOC ORDER BY TenMon")
            ds_monhoc = [r[0] for r in cursor.fetchall()]

            # 2) Tạo cột Treeview: Mã HS, Họ tên, Lớp + môn + TBCN + Xếp loại
            cols = ["Mã HS", "Họ tên", "Lớp"] + ds_monhoc + ["TBCN", "Xếp loại"]
            treeview.config(columns=cols, show="headings")
            for col in cols:
                treeview.heading(col, text=col)
                treeview.column(col, width=90, anchor="center")

            # 3) Truy vấn dữ liệu TBM từ bảng DIEM
            # Sử dụng MAX(CASE...) để pivot theo môn
            sql = f"""
                SELECT 
                    hs.MaHS, hs.HoTen, hs.Lop,
                    {', '.join([f"MAX(CASE WHEN m.TenMon = N'{mon}' THEN d.TBM END) AS [{mon}]" for mon in ds_monhoc])},
                    hs.DiemTBCN, hs.XepLoai
                FROM HOCSINH hs
                LEFT JOIN DIEM d ON hs.MaHS = d.MaHS AND d.HocKy = ?
                LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                WHERE hs.Lop = (SELECT MaLop FROM LOP WHERE GVCN = ?)
                GROUP BY hs.MaHS, hs.HoTen, hs.Lop, hs.DiemTBCN, hs.XepLoai
                ORDER BY hs.HoTen
            """
            cursor.execute(sql, (hocky, magv))

            for row in cursor.fetchall():
                # Chuyển None thành ''
                row = [v if v is not None else '' for v in row]
                treeview.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải điểm TBM: {e}")
        finally:
            conn.close()

    def sua_hs():
        selected = tree_info.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Chưa chọn học sinh để sửa!")
            return

        ma_hs = tree_info.item(selected[0])['values'][0]

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()

            # ---------------- 1) Load HOCSINH ----------------
            cur.execute("""
                SELECT MaHS, Ho, TenLot, Ten, GioiTinh, NgaySinh, Lop, TinhTrang
                FROM HOCSINH
                WHERE MaHS = ?
            """, (ma_hs,))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Không tìm thấy học sinh.")
                return

            # Điền dữ liệu vào form thông tin
            for i, entry in enumerate(entries_hs):
                value = row[i]
                if isinstance(entry, ttk.Combobox):
                    entry.set(value if value else '')
                elif isinstance(entry, DateEntry):
                    try:
                        entry.set_date(value)
                    except:
                        entry.set_date(datetime.now())
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value if value else '')

                # ---------------- 2) Load DIEM ----------------
            # 1) Lấy danh sách môn học từ DB
            cur.execute("SELECT TenMon FROM MONHOC ORDER BY TenMon")
            ds_monhoc = [r[0] for r in cur.fetchall()]

            # 2) Xóa dữ liệu cũ
            for e in entry_diem_hk1.values(): e.delete(0, tk.END)
            for e in entry_diem_hk2.values(): e.delete(0, tk.END)

            # 3) Load dữ liệu từ DIEM
            cur.execute("""
                SELECT m.TenMon, d.HocKy, d.B1, d.B2, d.B3, d.B4
                FROM DIEM d
                LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                WHERE d.MaHS = ?
            """, (ma_hs,))

            diem_dict = {}  # diem_dict[(TenMon, HocKy)] = [B1,B2,B3,B4]
            for ten_mon, hoc_ky, b1, b2, b3, b4 in cur.fetchall():
                diem_dict[(ten_mon, hoc_ky)] = [b1, b2, b3, b4]

            # 4) Điền dữ liệu vào Entry, tạo Entry nếu chưa có
            for mon in ds_monhoc:
                for hoc_ky, target_dict, frame in [(1, entry_diem_hk1, tab_hk1), (2, entry_diem_hk2, tab_hk2)]:
                    for col in ["B1","B2","B3","B4"]:
                        key = f"{mon}_{col}"
                        if key not in target_dict:
                            # Tạo Entry nếu chưa tồn tại
                            e = tk.Entry(frame, width=7, justify="center", font=font.FONT_CHU)
                            # Xác định vị trí dòng/column
                            row_idx = ds_monhoc.index(mon) + 1
                            col_idx = ["B1","B2","B3","B4"].index(col) + 1
                            e.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="ew")
                            target_dict[key] = e
                        # Điền dữ liệu
                        values = diem_dict.get((mon, hoc_ky), [None, None, None, None])
                        target_dict[key].delete(0, tk.END)
                        target_dict[key].insert(0, values[["B1","B2","B3","B4"].index(col)] if values[["B1","B2","B3","B4"].index(col)] is not None else "")

            # ---------------- 3) Load KHOANPHI vào frame ----------------
            cur.execute("""
                SELECT DaDong_HocPhi, HocPhi, 
                    DaDong_BHYT, Thang_BHYT, BHYT,
                    DaDong_BHTN, Muc_BHTN, BHTN,
                    TongTien
                FROM KHOANPHI
                WHERE MaHS = ? AND NamHoc='2024-2025'
            """, (ma_hs,))

            row = cur.fetchone()
            if row:
                var_hocphi.set(row[0])
                var_bhyt.set(row[2])
                combo_bhyt.set(row[3])
                var_bhtn.set(row[5])
                combo_bhtn.set(row[6])
                lbl_tongtien.config(text=str(row[8]))

            messagebox.showinfo("Thông báo", "Dữ liệu học sinh đã được tải!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu học sinh: {e}")
        finally:
            conn.close()

    # ====== Lưu học sinh + điểm + khoản phí ======
    def luu_hs():
        ma_hs = entries_hs[0].get().strip()
        if not ma_hs:
            messagebox.showwarning("Chú ý", "Chưa nhập Mã HS!")
            return

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()

            # 1) Cập nhật HOCSINH
            values = [e.get().strip() if not isinstance(e, DateEntry) else e.get_date() for e in entries_hs]
            cur.execute("""
                UPDATE HOCSINH
                SET Ho=?, TenLot=?, Ten=?, GioiTinh=?, NgaySinh=?, Lop=?, TinhTrang=?
                WHERE MaHS=?
            """, (*values[1:], ma_hs))

                # 2) Cập nhật DIEM (B1-B4) từ Entry, trigger tự tính TBM/TBCN/Xếp loại
            for hoc_ky, entry_dict in [(1, entry_diem_hk1), (2, entry_diem_hk2)]:
                for key, entry in entry_dict.items():
                    mon, col = key.split("_")
                    val = entry.get().strip()
                    val = float(val) if val != "" else None

                    # Lấy MaMon
                    cur.execute("SELECT MaMon FROM MONHOC WHERE TenMon=?", (mon,))
                    ma_mon = cur.fetchone()
                    if not ma_mon:
                        continue
                    ma_mon = ma_mon[0]

                    cur.execute(f"""
                        UPDATE DIEM
                        SET {col}=?
                        WHERE MaHS=? AND MaMon=? AND HocKy=? AND NamHoc=?
                    """, (val, ma_hs, ma_mon, hoc_ky, "2024-2025"))
            # ---- Xử lý BHYT ----
            if var_bhyt.get() == 1:
                thang_bhyt = combo_bhyt.get().strip()
                thang_bhyt = int(thang_bhyt) if thang_bhyt else None
            else:
                thang_bhyt = None

            # ---- Xử lý BHTN ----
            if var_bhtn.get() == 1:
                muc_bhtn = combo_bhtn.get().strip()
                muc_bhtn = int(muc_bhtn) if muc_bhtn else None
            else:
                muc_bhtn = None


            cur.execute("""
                UPDATE KHOANPHI
                SET DaDong_HocPhi=?,
                    DaDong_BHYT=?, Thang_BHYT=?,
                    DaDong_BHTN=?, Muc_BHTN=?
                WHERE MaHS=? AND NamHoc=?
            """, (
                int(var_hocphi.get()),         # YES/NO học phí
                int(var_bhyt.get()),           # YES/NO BHYT
                thang_bhyt,                    # NULL hoặc 1–12
                int(var_bhtn.get()),           # YES/NO BHTN
                muc_bhtn,                      # NULL hoặc mức tiền
                ma_hs, "2024-2025"
            ))

            conn.commit()
            messagebox.showinfo("Thông báo", f" Đã Lưu học sinh {ma_hs} thành công!")
            lam_moi_form()
            # -------- Reload dữ liệu lên Treeview --------
            load_data_hs(magv)          # Treeview danh sách học sinh
            load_data_diem(tree_hk1, 1, magv)  # Treeview điểm học kỳ 1
            load_data_diem(tree_hk2, 2, magv)  # Treeview điểm học kỳ 2
            load_data_phi(magv)          # Treeview các khoản phí

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Lưu thất bại: {e}")
        finally:
            conn.close()

    # =========================
    # HÀM LÀM MỚI FORM HỌC SINH
    # =========================
    def lam_moi_form():
        """Xóa dữ liệu tất cả Entry, Combobox, DateEntry và reset giá trị mặc định"""
        try:
            # Xóa tất cả Entry trong frame thông tin học sinh
            for entry in entries_hs:
                if isinstance(entry, ttk.Combobox):
                    entry.set('')  # Combobox có set()
                elif isinstance(entry, DateEntry):
                    entry.set_date(datetime.today())  # DateEntry dùng set_date()
                else:
                    entry.delete(0, 'end')  # Xóa Entry

            # Reset điểm học kỳ 1
            for key, entry in entry_diem_hk1.items():
                entry.delete(0, 'end')

            # Reset điểm học kỳ 2
            for key, entry in entry_diem_hk2.items():
                entry.delete(0, 'end')

            # Reset các biến khoản phí
            var_hocphi.set(0)
            var_bhyt.set(0)
            combo_bhyt.set('')
            var_bhtn.set(0)
            combo_bhtn.set('')
            lbl_tongtien.config(text='0')

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới form!\n{e}")

    def xuat_excel_lop(magv):
        """
        Xuất danh sách học sinh + điểm TBM + TBCN + Xếp loại ra file Excel
        magv: Mã giáo viên chủ nhiệm
        """
        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return

        try:
            cursor = conn.cursor()

            # 1) Lấy danh sách môn học để xuất TBM
            cursor.execute("SELECT TenMon FROM MONHOC ORDER BY TenMon")
            ds_monhoc = [r[0] for r in cursor.fetchall()]

            # 2) Lấy thông tin học sinh + TBM + TBCN + Xếp loại
            sql = f"""
                SELECT 
                    hs.MaHS, hs.HoTen, hs.Lop,
                    {', '.join([f"MAX(CASE WHEN m.TenMon = N'{mon}' THEN d.TBM END) AS [{mon}]" for mon in ds_monhoc])},
                    hs.DiemTBCN, hs.XepLoai
                FROM HOCSINH hs
                LEFT JOIN DIEM d ON hs.MaHS = d.MaHS
                LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                WHERE hs.Lop = (SELECT MaLop FROM LOP WHERE GVCN = ?)
                GROUP BY hs.MaHS, hs.HoTen, hs.Lop, hs.DiemTBCN, hs.XepLoai
                ORDER BY hs.HoTen
            """
            cursor.execute(sql, (magv,))
            rows = cursor.fetchall()

            # 3) Tạo DataFrame
            cols = ["Mã HS","Họ tên","Lớp"] + ds_monhoc + ["TBCN","Xếp loại"]
            data = [[v if v is not None else '' for v in row] for row in rows]
            df = pd.DataFrame(data, columns=cols)

            # 4) Chọn file lưu
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files","*.xlsx"), ("All files","*.*")],
                title="Lưu danh sách học sinh"
            )
            if not file_path:
                return  # hủy

            # 5) Xuất Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", f"Đã xuất danh sách học sinh ra {file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất Excel thất bại: {e}")
        finally:
            conn.close()

    def thoat():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát ứng dụng?"):
            gvcn_window.destroy()

    # ===========================
    #    CÁC NÚT CHỨC NĂNG HS
    # ===========================
    frame_btn_hs = tk.Frame(gvcn_window, bg=font.BG_COLOR)
    frame_btn_hs.grid(row=3, column=0, pady=5, sticky= "s")
    gvcn_window.grid_rowconfigure(3, weight=1),

    btn_sua_hs = tk.Button(
        frame_btn_hs, text="✏ Sửa", command=sua_hs, width=12,
        font=font.FONT_CHU, bg="#3326AD", fg="white"
    )
    btn_sua_hs.grid(row=0, column=1, padx=8)

    btn_luu_hs = tk.Button(
        frame_btn_hs, text="💾 Lưu", command=luu_hs, width=12,
        font=font.FONT_CHU, bg="#3326AD", fg="white"
    )
    btn_luu_hs.grid(row=0, column=2, padx=8)

    btn_lam_moi_hs = tk.Button(
            frame_btn_hs, text="🔄 Làm mới", command=lam_moi_form, width=12,
            font=font.FONT_CHU, bg="#3326AD", fg="white"
        )
    btn_lam_moi_hs.grid(row=0, column=4, padx=8)
    btn_xuat_excel = tk.Button(
    frame_btn_hs, text="📄 Xuất Excel", command=lambda: xuat_excel_lop(magv),
    width=12, font=font.FONT_CHU, bg="#4CAF50", fg="white"
    )
    btn_xuat_excel.grid(row=0, column=5, padx=8)
    btn_thoat = tk.Button(
            frame_btn_hs, text="Thoát", command=thoat, width=12,
            font=font.FONT_CHU, bg="#D4072D", fg="white"
        )
    btn_thoat.grid(row=0, column=6, padx=8)

    # ==== Load dữ liệu khi mở tab ====
    load_data_hs(magv)
    load_data_phi(magv)
    load_data_diem(tree_hk1, 1, magv)
    load_data_diem(tree_hk2, 2, magv)      

    gvcn_window.mainloop()