import tkinter as tk
from tkinter import IntVar, ttk
from tkinter import filedialog
from openpyxl import Workbook
import font
from connect_db import connect_db
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry

def admin_window():
    admin_window = tk.Tk()
    admin_window.title("ADMIN")
    admin_window.geometry("1200x700")
    admin_window.configure(bg="#E8F4FB")

    for i in range(3):
        admin_window.grid_rowconfigure(i, weight=1)
    admin_window.grid_columnconfigure(0, weight=1)
    # ====== Tiêu đề chính ======
    title_label = tk.Label(
        admin_window,
        text="🎓HỆ THỐNG QUẢN LÝ HỌC SINH",
        font=("Times New Roman", 17, "bold"),
        bg="#E8F4FB", fg="#0A3D62"
    )
    title_label.grid(row=0, column=0, sticky="n") 
    admin_window.grid_rowconfigure(0, weight=1)

    style = ttk.Style()
    style.theme_use('default')  # đảm bảo theme mặc định để có thể chỉnh màu
    style.configure('TNotebook.Tab', background="#E8F4FB", foreground='black', padding=[10, 5])
    
    # ====== Notebook chính ======
    tab_control = ttk.Notebook(admin_window)
    tab_control.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
    admin_window.grid_rowconfigure(0, weight=0)

    # --- Tab Quản lý thông tin ---
    QLTT = ttk.Frame(tab_control)
    tab_control.add(QLTT, text="Quản lý thông tin",)

    # --- Tab Quản lý danh sách ---
    QLDS = ttk.Frame(tab_control)
    tab_control.add(QLDS, text="Quản lý danh sách")
    
    # ====== Sub-notebook Quản lý thông tin ======
    sub_notebook_tt = ttk.Notebook(QLTT)
    sub_notebook_tt.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    sub_notebook_tt.grid_rowconfigure(0, weight=1)
    sub_notebook_tt.grid_columnconfigure(0, weight=1)

    # Cho QLTT co giãn theo cả row và column
    QLTT.grid_rowconfigure(0, weight=1)
    QLTT.grid_columnconfigure(0, weight=1)

    # Tạo tab cho Học sinh và Giáo viên
    tab_hocsinh = ttk.Frame(sub_notebook_tt)
    tab_giaovien = ttk.Frame(sub_notebook_tt)
    sub_notebook_tt.add(tab_hocsinh, text="Học sinh")
    sub_notebook_tt.add(tab_giaovien, text="Giáo viên")
        
    # ============================================================
    # ---------------------- TAB THÔNG TIN HỌC SINH ------------------------
    # ============================================================
    scrollable_frame = ttk.Frame(tab_hocsinh)
    scrollable_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    tab_hocsinh.grid_rowconfigure(0, weight=0)
    tab_hocsinh.grid_columnconfigure(0, weight=1)

    # ===== Khung chính chứa 3 phần: Học sinh - Điểm - Khoản phí =====
    frame_cha = tk.Frame(scrollable_frame, bg=font.BG_COLOR)
    frame_cha.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    frame_cha.grid_columnconfigure((0,1,2), weight=1, uniform="col")
    frame_cha.grid_rowconfigure(0, weight=0)

    # ---------------- Frame Thông tin học sinh ----------------
    frame_hs = ttk.LabelFrame(frame_cha, text="Thông tin học sinh", padding=10)
    frame_hs.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
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

    # ---------------- Frame Điểm học kỳ ----------------
    frame_diem = ttk.LabelFrame(frame_cha, text="Điểm học kỳ", padding=10)
    frame_diem.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
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
    frame_phi = ttk.LabelFrame(frame_cha, text="Khoản phí", padding=10)
    frame_phi.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
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
    frame_ds_hs = ttk.LabelFrame(scrollable_frame, text="Danh sách học sinh", padding=(5,5))
    frame_ds_hs.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
    scrollable_frame.grid_rowconfigure(1, weight=0)
    scrollable_frame.grid_columnconfigure(0, weight=1)
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
    # ===========================
    #   HÀM LOAD DỮ LIỆU HỌC SINH
    # ===========================
    def load_data_hs():
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
            # ---------------- Load Bảng Thông tin học sinh ----------------
            cursor.execute("""
                SELECT MAHS, HO, TENLOT, TEN, GIOITINH, NGAYSINH, LOP, TINHTRANG
                FROM HOCSINH 
                ORDER BY TEN ASC
            """)
            for row in cursor.fetchall():
                row = list(row)
                if row[5]:
                    row[5] = row[5].strftime("%d/%m/%Y")
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_info.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    # ===========================
    #    Load dữ liệu Khoản phí
    # ===========================
    def load_data_phi():
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
                LEFT JOIN KHOANPHI k ON h.MaHS = k.MaHS AND k.NamHoc='2024-2025'
                ORDER BY h.Lop, h.HoTen
            """)
            rows = cursor.fetchall()
            tree_phi.delete(*tree_phi.get_children())
            for row in rows:
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_phi.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu khoản phí: {e}")
        finally:
            conn.close()
    load_data_phi()
    # ===========================
    #    Load dữ liệu Điểm số
    # ===========================
    def load_data_diem(treeview, hocky):
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
            sql = f"""
                SELECT 
                    hs.MaHS, hs.HoTen, hs.Lop,
                    {', '.join([f"MAX(CASE WHEN m.TenMon = N'{mon}' THEN d.TBM END) AS [{mon}]" for mon in ds_monhoc])},
                    hs.DiemTBCN, hs.XepLoai
                FROM HOCSINH hs
                LEFT JOIN DIEM d ON hs.MaHS = d.MaHS AND d.HocKy = ?
                LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                GROUP BY hs.MaHS, hs.HoTen, hs.Lop, hs.DiemTBCN, hs.XepLoai
                ORDER BY hs.Lop, hs.HoTen
            """
            cursor.execute(sql, (hocky,))

            for row in cursor.fetchall():
                row = [v if v is not None else '' for v in row]
                treeview.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải điểm TBM: {e}")
        finally:
            conn.close()
    load_data_diem(tree_hk1, 1)
    load_data_diem(tree_hk2, 2) 

    def them_hs():
        # --- 1) Lấy dữ liệu từ form ---
        mahs = entries_hs[0].get().strip()
        if not mahs:
            messagebox.showwarning("Chú ý", "Chưa nhập Mã HS!")
            return
        ho = entries_hs[1].get().strip()
        tenlot = entries_hs[2].get().strip()
        ten = entries_hs[3].get().strip()
        gioitinh = entries_hs[4].get().strip()
        ngaysinh = entries_hs[5].get_date()
        lop = entries_hs[6].get()
        tinhtrang = entries_hs[7].get().strip()

        if not ho or not ten:
            messagebox.showwarning("Chú ý", "Chưa nhập đủ họ và tên!")
            return

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()

            # --- Kiểm tra trùng Mã HS ---
            cur.execute("SELECT MaHS FROM HOCSINH WHERE MaHS=?", (mahs,))
            if cur.fetchone():
                messagebox.showwarning("Trùng Mã HS", f"Học sinh {mahs} đã tồn tại!")
                return

            # --- 2) Thêm HOCSINH ---
            cur.execute("""
                INSERT INTO HOCSINH(MAHS, HO, TENLOT, TEN, GIOITINH, NGAYSINH, LOP, TINHTRANG)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (mahs, ho, tenlot, ten, gioitinh, ngaysinh, lop, tinhtrang))

            # --- 3) Thêm DIEM cho HK1 và HK2 ---
            for hk, entry_dict in [(1, entry_diem_hk1), (2, entry_diem_hk2)]:
                for mon in monhoc:
                    b1 = entry_dict[f"{mon}_B1"].get() or None
                    b2 = entry_dict[f"{mon}_B2"].get() or None
                    b3 = entry_dict[f"{mon}_B3"].get() or None
                    b4 = entry_dict[f"{mon}_B4"].get() or None

                    cur.execute("SELECT MaMon FROM MONHOC WHERE TenMon=?", (mon,))
                    ma_mon = cur.fetchone()
                    if ma_mon:
                        ma_mon = ma_mon[0]
                        cur.execute("""
                            INSERT INTO DIEM(MaHS, MaMon, HocKy, B1, B2, B3, B4, NamHoc)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (mahs, ma_mon, hk, b1, b2, b3, b4, "2024-2025"))

            # --- 4) Thêm KHOANPHI ---
            da_hocphi = 1 if var_hocphi.get() == 1 else 0
            da_bhyt = 1 if var_bhyt.get() == 1 else 0
            thang_bhyt = combo_bhyt.get() or None
            da_bhtn = 1 if var_bhtn.get() == 1 else 0
            muc_bhtn = combo_bhtn.get() or None

            cur.execute("""
                INSERT INTO KHOANPHI(MaHS, NamHoc, DaDong_HocPhi, DaDong_BHYT, Thang_BHYT, DaDong_BHTN, Muc_BHTN)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (mahs, "2024-2025", da_hocphi, da_bhyt, thang_bhyt, da_bhtn, muc_bhtn))

            conn.commit()
            messagebox.showinfo("Thành công", f"Thêm học sinh {ho} {tenlot} {ten} thành công!")

            # --- 6) Reset form ---
            for e in entries_hs:
                if isinstance(e, tk.Entry) or isinstance(e, DateEntry):
                    e.delete(0, tk.END)
                elif isinstance(e, ttk.Combobox):
                    e.set('')
            var_hocphi.set(0); var_bhyt.set(0); var_bhtn.set(0)
            lbl_tongtien.config(text="0")
            for d in list(entry_diem_hk1.values()) + list(entry_diem_hk2.values()):
                d.delete(0, tk.END)
            lam_moi_form()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()
           # --- 5) Reload Treeview + tính TBM ---
        load_data_hs()          # danh sách học sinh
        load_data_diem(tree_hk1, 1)  # điểm HK1
        load_data_diem(tree_hk2, 2)  # điểm HK2
        load_data_phi()         # khoản phí
    
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
            load_data_hs()          # Treeview danh sách học sinh
            load_data_diem(tree_hk1, 1)  # Treeview điểm học kỳ 1
            load_data_diem(tree_hk2, 2)  # Treeview điểm học kỳ 2
            load_data_phi()          # Treeview các khoản phí

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Lưu thất bại: {e}")
        finally:
            conn.close()
    # ====== Xóa học sinh ======
    def xoa_hs():
        selected = tree_info.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Chưa chọn học sinh để xóa!")
            return
        ma_hs = tree_info.item(selected[0])['values'][0]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa học sinh {ma_hs}?"):
            return

        conn = connect_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            # xóa dữ liệu liên quan
            cur.execute("DELETE FROM DIEM WHERE MaHS=?", (ma_hs,))
            cur.execute("DELETE FROM KHOANPHI WHERE MaHS=?", (ma_hs,))
            cur.execute("DELETE FROM HOCSINH WHERE MaHS=?", (ma_hs,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa học sinh {ma_hs}")
            load_data_hs()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))
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

    # ===========================
    #    CÁC NÚT CHỨC NĂNG HS
    # ===========================
    frame_btn_hs = tk.Frame(scrollable_frame)
    frame_btn_hs.grid(row=2, column=0)
    scrollable_frame.grid_rowconfigure(2, weight=0)

    btn_them_hs = tk.Button(
        frame_btn_hs, text="➕ Thêm", command=them_hs, width=12,
        font=font.FONT_CHU, bg="#3326AD", fg="white"
    )
    btn_them_hs.grid(row=0, column=0, padx=8)

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

    btn_xoa_hs = tk.Button(
        frame_btn_hs, text="🗑 Xóa", command=xoa_hs, width=12,
        font=font.FONT_CHU, bg="#F44336", fg="white"
    )
    btn_xoa_hs.grid(row=0, column=4, padx=8)

    btn_lam_moi_hs = tk.Button(
            frame_btn_hs, text="🔄 Làm mới", command=lam_moi_form, width=12,
            font=font.FONT_CHU, bg="#3326AD", fg="white"
        )
    btn_lam_moi_hs.grid(row=0, column=3, padx=8)
    # ============================================================
    # ---------------------- TAB GIÁO VIÊN ------------------------
    # ============================================================
    tab_giaovien.grid_rowconfigure(1, weight=1)
    tab_giaovien.grid_columnconfigure(0, weight=1)

    # ===== Tạo container căn giữa =====
    container_gv = tk.Frame(tab_giaovien, bg=font.BG_COLOR)
    container_gv.grid(row=0, column=0, sticky="nsew")
    container_gv.grid_rowconfigure(0, weight=1)
    container_gv.grid_columnconfigure(0, weight=1)

    # ===== Frame thông tin giáo viên =====
    frame_gv = ttk.LabelFrame(container_gv, text="Thông tin giáo viên", padding=5, width=400, height=500)
    frame_gv.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    # ----- Form thông tin giáo viên -----
    tk.Label(frame_gv, text="Mã GV:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=0, column=0, padx=5, pady=5)
    entry_magv = tk.Entry(frame_gv, width=25, font=font.FONT_CHU)
    entry_magv.grid(row=0, column=1, sticky="w")

    tk.Label(frame_gv, text="Họ tên:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=1, column=0, padx=5, pady=5)
    entry_hoten = tk.Entry(frame_gv, width=25, font=font.FONT_CHU)
    entry_hoten.grid(row=1, column=1, sticky="w")

    tk.Label(frame_gv, text="Giới tính:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=2, column=0, padx=5, pady=5)
    var_gioitinh = tk.StringVar(value="Nam")
    tt_nam = ttk.Radiobutton(frame_gv, text="Nam", variable=var_gioitinh, value="Nam")
    tt_nam.grid(row=2, column=1, sticky="w", padx=5)
    tt_nu = ttk.Radiobutton(frame_gv, text="Nữ", variable=var_gioitinh, value="Nữ")
    tt_nu.grid(row=2, column=1, sticky="e", padx=40)

    tk.Label(frame_gv, text="Ngày sinh:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=3, column=0, padx=5, pady=5)
    date_ngaysinh_gv = DateEntry(frame_gv, width=22, background="lightblue",
                                foreground="black", date_pattern="dd/mm/yyyy")
    date_ngaysinh_gv.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    tk.Label(frame_gv, text="Môn dạy chính:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=4, column=0, padx=5, pady=5)
    combo_monday = ttk.Combobox(frame_gv,
                                values=["Toán", "Ngữ Văn", " Tiếng Anh", "Vật Lí", "Hóa Học", "Sinh Học", "Lịch Sử", "Địa Lí", "GDCD", "Tin Học", "Công Nghệ"],
                                width=22, state="readonly")
    combo_monday.grid(row=4, column=1, sticky="w", padx=5, pady=5)

    tk.Label(frame_gv, text="Vai trò:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=5, column=0, padx=5, pady=5)
    combo_vaitro = ttk.Combobox(frame_gv,
                                values=["GVBM", "GVCN", "ADMIN"], width=22, state="readonly")
    combo_vaitro.grid(row=5, column=1, sticky="w", padx=5, pady=5)

    tk.Label(frame_gv, text="SĐT:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=6, column=0, padx=5, pady=5)
    entry_sdt = tk.Entry(frame_gv, width=25, font=font.FONT_CHU)
    entry_sdt.grid(row=6, column=1, sticky="w", padx=5, pady=5)

    tk.Label(frame_gv, text="Email:", width=14, anchor="e",
            bg=font.BG_COLOR, fg=font.FG_COLOR, font=font.FONT_CHU).grid(row=7, column=0, padx=5, pady=5)
    entry_email = tk.Entry(frame_gv, width=25, font=font.FONT_CHU)
    entry_email.grid(row=7, column=1, sticky="w", padx=5, pady=5)

    # ---------------- Frame Danh sách Giáo viên ----------------
    frame_ds_gv = ttk.LabelFrame(container_gv, text="Danh sách giáo viên", padding=10)
    frame_ds_gv.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
    frame_ds_gv.grid_rowconfigure(0, weight=1)
    frame_ds_gv.grid_columnconfigure(0, weight=1)

    # Treeview Giáo viên
    cols_gv = ["Mã GV", "Họ tên", "Giới tính", "Ngày sinh", "Môn dạy", "Vai trò", "SoDT", "Email"]
    tree_gv = ttk.Treeview(frame_ds_gv, columns=cols_gv, show="headings")
    for col in cols_gv:
        tree_gv.heading(col, text=col)
        tree_gv.column(col, width=120, anchor="center")

    # Scrollbar
    scrollbar_gv_v = ttk.Scrollbar(frame_ds_gv, orient="vertical", command=tree_gv.yview)
    scrollbar_gv_h = ttk.Scrollbar(frame_ds_gv, orient="horizontal", command=tree_gv.xview)
    tree_gv.configure(yscrollcommand=scrollbar_gv_v.set, xscrollcommand=scrollbar_gv_h.set)
    tree_gv.grid(row=0, column=0, sticky="nsew")
    scrollbar_gv_v.grid(row=0, column=1, sticky="ns")
    scrollbar_gv_h.grid(row=1, column=0, sticky="ew")

    # ===================== HỆ THỐNG ĐIỀU HƯỚNG TAB GIÁO VIÊN =====================

    # Gom tất cả widget theo thứ tự để nhấn Enter → nhảy tiếp
    focus_gv = [
        entry_magv,
        entry_hoten,
        tt_nam,
        tt_nu,
        date_ngaysinh_gv,
        combo_monday,
        combo_vaitro,
        entry_sdt,
        entry_email
    ]

    # ------- Hàm nhảy tới widget kế tiếp -------
    def focus_next_gv(event):
        widget = event.widget
        if widget in focus_gv:
            idx = focus_gv.index(widget)
            if idx < len(focus_gv) - 1:
                focus_gv[idx + 1].focus_set()
        return "break"

    # ------- Hàm nhảy tới widget trước -------
    def focus_prev_gv(event):
        widget = event.widget
        if widget in focus_gv:
            idx = focus_gv.index(widget)
            if idx > 0:
                focus_gv[idx - 1].focus_set()
        return "break"

    # ===================== GÁN SỰ KIỆN =====================

    for w in focus_gv:
        # Enter → đi tới
        w.bind("<Return>", focus_next_gv)
        # Shift+Enter → lùi lại
        w.bind("<Shift-Return>", focus_prev_gv)
        # ↓ → đi tới
        w.bind("<Down>", focus_next_gv)
        # ↑ → lùi lại
        w.bind("<Up>", focus_prev_gv)

    # ===========================
    #   HÀM TÁCH HỌ TÊN GIÁO VIÊN
    # ===========================
    def tach_ho_ten(hoten):
        """
        Tách một chuỗi Họ tên đầy đủ thành Họ, Tên lót, Tên.
        Trả về: ho, tenlot, ten
        """
        parts = hoten.strip().split()
        if not parts:
            return "", "", ""
        ho = parts[0]                     # Họ
        ten = parts[-1]                   # Tên
        tenlot = " ".join(parts[1:-1]) if len(parts) > 2 else ""  # Tên lót (nếu có)
        return ho, tenlot, ten

    def lam_moi_gv():
        entry_magv.delete(0, 'end')
        entry_hoten.delete(0, 'end')
        var_gioitinh.set("Nam")
        date_ngaysinh_gv.set_date(datetime.today())
        combo_monday.set("")
        combo_vaitro.set("")
        entry_sdt.delete(0, 'end')       
        entry_email.delete(0, 'end') 

    def load_data_gv():
        tree_gv.delete(*tree_gv.get_children())
        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MaGV, HoTen, GioiTinh, NgaySinh, MonDay, VaiTro, SoDT, Email FROM GIAOVIEN")
            rows = cursor.fetchall()
            for row in rows:
                ho, tenlot, ten = tach_ho_ten(row[1])
                ngay = row[3].strftime("%d/%m/%Y") if row[3] else ""
                tree_gv.insert("", "end", values=[row[0], row[1], row[2], ngay, row[4], row[5], row[6], row[7]])
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def them_gv():
        magv = entry_magv.get().strip()
        hoten = entry_hoten.get().strip()
        gioitinh = var_gioitinh.get()
        ngaysinh = date_ngaysinh_gv.get_date()
        monday = combo_monday.get()
        vaitro = combo_vaitro.get()
        sdt = entry_sdt.get().strip()       # SĐT
        email = entry_email.get().strip()   # Email

        if not magv or not hoten:
            messagebox.showwarning("Chú ý", "Chưa nhập đủ thông tin Mã GV và Họ tên!")
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO GIAOVIEN(MaGV, HoTen, GioiTinh, NgaySinh, MonDay, VaiTro, SoDT, Email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (magv, hoten, gioitinh, ngaysinh, monday, vaitro, sdt, email))
            conn.commit()
            messagebox.showinfo("Thành công", f"Thêm giáo viên {hoten} thành công!")
            load_data_gv()
            lam_moi_gv()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()


    def xoa_gv():
        selected = tree_gv.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Chưa chọn giáo viên để xóa!")
            return
        magv = tree_gv.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có muốn xóa giáo viên {magv}?"):
            conn = connect_db()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM GIAOVIEN WHERE MaGV=?", magv)
                conn.commit()
                messagebox.showinfo("Thông báo", f"Đã xóa giáo viên {magv}.")
                load_data_gv()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Lỗi", str(e))
            finally:
                conn.close()

    def sua_gv():
        selected = tree_gv.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Chưa chọn giáo viên để sửa!")
            return
        item = tree_gv.item(selected[0])
        # Chỉ unpack đúng 8 cột
        magv, hoten, gioitinh, ngay, monday, vaitro, sdt, email = item['values']
        entry_magv.delete(0, 'end')
        entry_magv.insert(0, magv)
        entry_hoten.delete(0, 'end')
        entry_hoten.insert(0, hoten)
        var_gioitinh.set(gioitinh)
        date_ngaysinh_gv.set_date(datetime.strptime(ngay, "%d/%m/%Y") if ngay else datetime.today())
        combo_monday.set(monday)
        combo_vaitro.set(vaitro)
        entry_sdt.delete(0, 'end')
        entry_sdt.insert(0, sdt if sdt else "")
        entry_email.delete(0, 'end')
        entry_email.insert(0, email if email else "")



    def luu_gv():
        magv = entry_magv.get().strip()
        hoten = entry_hoten.get().strip()
        gioitinh = var_gioitinh.get()
        ngaysinh = date_ngaysinh_gv.get_date()
        monday = combo_monday.get()
        vaitro = combo_vaitro.get()
        sdt = entry_sdt.get().strip()
        email = entry_email.get().strip()

        if not magv or not hoten:
            messagebox.showwarning("Chú ý", "Chưa nhập đủ thông tin Mã GV và Họ tên!")
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE GIAOVIEN 
                SET HoTen=?, GioiTinh=?, NgaySinh=?, MonDay=?, VaiTro=?, SoDT=?, Email=? 
                WHERE MaGV=?
            """, (hoten, gioitinh, ngaysinh, monday, vaitro, sdt, email, magv))
            conn.commit()
            messagebox.showinfo("Thông báo", f"Đã lưu thông tin giáo viên {hoten}.")
            load_data_gv()
            lam_moi_gv()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()


    # =========================
    #   GẮN HÀM CHO NÚT
    # =========================
    frame_btn_gv = tk.Frame(container_gv, bg=font.BG_COLOR)
    frame_btn_gv.grid(row=2, column=0, pady=5)

    btn_them_gv = tk.Button(frame_btn_gv, text=" Thêm", width=12, font=font.FONT_CHU, bg="#3326AD", fg="white", command=them_gv)
    btn_them_gv.grid(row=0, column=0, padx=8)

    btn_capnhat_gv = tk.Button(frame_btn_gv, text=" Lưu", width=12, font=font.FONT_CHU, bg="#3326AD", fg="white", command=luu_gv)
    btn_capnhat_gv.grid(row=0, column=2, padx=8)

    btn_xoa_gv = tk.Button(frame_btn_gv, text="🗑 Xóa", width=12, font=font.FONT_CHU, bg="#F44336", fg="white", command=xoa_gv)
    btn_xoa_gv.grid(row=0, column=4, padx=8)

    btn_reset_gv = tk.Button(frame_btn_gv, text="Làm mới", width=12, font=font.FONT_CHU, bg="#3326AD", fg="white", command=lam_moi_gv)
    btn_reset_gv.grid(row=0, column=3, padx=8)

    btn_sua_gv = tk.Button(frame_btn_gv, text="Sửa", width=12, font=font.FONT_CHU, bg="#3326AD", fg="white", command=sua_gv)
    btn_sua_gv.grid(row=0, column=1, padx=8)

# ====== Sub-notebook Quản lý danh sách ======
    sub_notebook_ds = ttk.Notebook(QLDS)
    sub_notebook_ds.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Cho QLDS co giãn theo cả row và column
    QLDS.grid_rowconfigure(0, weight=1)
    QLDS.grid_columnconfigure(0, weight=1)

    # Tạo các tab bên trong Sub-notebook Danh sách
    tab_dshocsinh = ttk.Frame(sub_notebook_ds)
    tab_dsgiaovien = ttk.Frame(sub_notebook_ds)
    tab_lop = ttk.Frame(sub_notebook_ds)
    tab_thoikhoabieu = ttk.Frame(sub_notebook_ds)

    sub_notebook_ds.add(tab_dshocsinh, text="Danh sách học sinh")
    sub_notebook_ds.add(tab_dsgiaovien, text="Danh sách giáo viên")
    sub_notebook_ds.add(tab_lop, text="Danh sách lớp")

    # =====================================================
    # ---------------- TAB DANH SÁCH HỌC SINH -------------
    # =====================================================
    tab_dshocsinh.grid_rowconfigure(0, weight=1)
    tab_dshocsinh.grid_columnconfigure(0, weight=1)

    # Khung cuộn chứa notebook
    frame_scroll_hs = ttk.Frame(tab_dshocsinh)
    frame_scroll_hs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_scroll_hs.grid_rowconfigure(0, weight=1)
    frame_scroll_hs.grid_columnconfigure(0, weight=1)

    # ===== Notebook chính cho học sinh =====
    notebook_hs = ttk.Notebook(frame_scroll_hs)
    notebook_hs.grid(row=0, column=0, sticky="nsew")
    notebook_hs.grid_rowconfigure(0, weight=1)
    notebook_hs.grid_columnconfigure(0, weight=1)

    # --- Tab 1: Điểm số ---
    tab_diem = ttk.Frame(notebook_hs)
    notebook_hs.add(tab_diem, text="Điểm số")
    tab_diem.grid_rowconfigure(0, weight=1)
    tab_diem.grid_columnconfigure(0, weight=1)

    # ----- Notebook cho Học kỳ (HK1/HK2) -----
    notebook_hocky = ttk.Notebook(tab_diem)
    notebook_hocky.grid(row=0, column=0, sticky="nsew")
    notebook_hocky.grid_rowconfigure(0, weight=1)
    notebook_hocky.grid_columnconfigure(0, weight=1)

    tab_hk1 = ttk.Frame(notebook_hocky)
    tab_hk2 = ttk.Frame(notebook_hocky)
    notebook_hocky.add(tab_hk1, text="Học kỳ 1")
    notebook_hocky.add(tab_hk2, text="Học kỳ 2")

    for tab in (tab_hk1, tab_hk2):
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

    # ----- Cột Treeview điểm số -----
    cols_diem = [
        "Mã HS", "Họ", "Tên Lót", "Tên", "Giới Tính", "Ngày Sinh", "Lớp",
        "Toán", "Ngữ văn", "Tiếng Anh", "Vật lí", "Hóa học", "Sinh học",
        "Lịch sử", "Địa lí", "GDCD", "Tin học", "Công nghệ",
        "TBCN", "Xếp loại", "Tình Trạng"
    ]

    def create_treeview(parent, columns):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            if col == "Mã HS":
                tree.column(col, width=70, anchor="center", stretch=False)
            elif col in ["Họ", "Tên Lót", "Tên"]:
                tree.column(col, width=150, anchor="w")
            elif col in ["TBCN", "Xếp loại"]:
                tree.column(col, width=80, anchor="center")
            else:
                tree.column(col, width=80, anchor="center")
            tree.heading(col, text=col)
        # Scrollbars
        scroll_v = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        scroll_h = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")
        return tree

    # Treeview HK1 & HK2
    tree_hk1 = create_treeview(tab_hk1, cols_diem)
    tree_hk2 = create_treeview(tab_hk2, cols_diem)

    # --- Tab 2: Khoản phí ---
    tab_phi = ttk.Frame(notebook_hs)
    notebook_hs.add(tab_phi, text="Khoản phí")
    tab_phi.grid_rowconfigure(0, weight=1)
    tab_phi.grid_columnconfigure(0, weight=1)

    cols_phi = ["Mã HS", "Họ tên", "Lớp", "Học phí", "BHYT", "Tháng BHYT", "BHTN", "Mức BHTN", "Tổng tiền"]
    tree_phi = create_treeview(tab_phi, cols_phi)

    # ===========================
    #    Load dữ liệu Khoản phí
    # ===========================
    def load_data_dshs_phi():
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
                LEFT JOIN KHOANPHI k ON h.MaHS = k.MaHS AND k.NamHoc='2024-2025'
                ORDER BY h.Lop, h.HoTen
            """)
            rows = cursor.fetchall()
            tree_phi.delete(*tree_phi.get_children())
            for row in rows:
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_phi.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu khoản phí: {e}")
        finally:
            conn.close()

 
    # ===========================
    #    Load dữ liệu Điểm số
    # ===========================
    def load_data_dshs_diem(treeview, hocky):
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
            sql = f"""
                SELECT 
                    hs.MaHS, hs.HoTen, hs.Lop,
                    {', '.join([f"MAX(CASE WHEN m.TenMon = N'{mon}' THEN d.TBM END) AS [{mon}]" for mon in ds_monhoc])},
                    hs.DiemTBCN, hs.XepLoai
                FROM HOCSINH hs
                LEFT JOIN DIEM d ON hs.MaHS = d.MaHS AND d.HocKy = ?
                LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                GROUP BY hs.MaHS, hs.HoTen, hs.Lop, hs.DiemTBCN, hs.XepLoai
                ORDER BY hs.Lop, hs.HoTen
            """
            cursor.execute(sql, (hocky,))

            for row in cursor.fetchall():
                row = [v if v is not None else '' for v in row]
                treeview.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải điểm TBM: {e}")
        finally:
            conn.close()

    # ==== Load dữ liệu khi mở tab ====
    load_data_dshs_phi()
    load_data_dshs_diem(tree_hk1, 1)
    load_data_dshs_diem(tree_hk2, 2)

    # ===========================
    #    HÀM XUẤT EXCEL
    # ===========================
    def xuat_excel_dshs():
        import pandas as pd
        from tkinter import filedialog, messagebox

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Lưu file Excel"
        )
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

                # ===== Xuất điểm học kỳ 1 =====
                data_hk1 = [tree_hk1.item(i)["values"] for i in tree_hk1.get_children()]
                cols_hk1 = [tree_hk1.heading(c)["text"] for c in tree_hk1["columns"]]
                df_hk1 = pd.DataFrame(data_hk1, columns=cols_hk1)
                df_hk1.to_excel(writer, sheet_name="HK1", index=False)

                # ===== Xuất điểm học kỳ 2 =====
                data_hk2 = [tree_hk2.item(i)["values"] for i in tree_hk2.get_children()]
                cols_hk2 = [tree_hk2.heading(c)["text"] for c in tree_hk2["columns"]]
                df_hk2 = pd.DataFrame(data_hk2, columns=cols_hk2)
                df_hk2.to_excel(writer, sheet_name="HK2", index=False)

                # ===== Xuất khoản phí =====
                data_phi = [tree_phi.item(i)["values"] for i in tree_phi.get_children()]
                cols_phi_actual = [tree_phi.heading(c)["text"] for c in tree_phi["columns"]]
                df_phi = pd.DataFrame(data_phi, columns=cols_phi_actual)
                df_phi.to_excel(writer, sheet_name="KhoanPhi", index=False)

            messagebox.showinfo("Thành công", f"Xuất Excel thành công!\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xuất Excel: {e}")

    btn_xuat = tk.Button(
        tab_dshocsinh,
        text="Xuất Excel",
        bg="#4A90E2",
        fg="white",
        font=("Arial", 12, "bold"),
        command=xuat_excel_dshs
    )
    btn_xuat.grid(row=1, column=0, pady=10)

    # =====================================================
    # ---------------- TAB DANH SÁCH GIÁO VIÊN -------------
    # =====================================================
    tab_dsgiaovien.grid_rowconfigure(0, weight=1)
    tab_dsgiaovien.grid_columnconfigure(0, weight=1)

    # Khung cuộn
    frame_scroll_gv = ttk.Frame(tab_dsgiaovien)
    frame_scroll_gv.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_scroll_gv.grid_rowconfigure(0, weight=1)
    frame_scroll_gv.grid_columnconfigure(0, weight=1)

    # ===== Notebook chính cho giáo viên =====
    notebook_gv = ttk.Notebook(frame_scroll_gv)
    notebook_gv.grid(row=0, column=0, sticky="nsew")
    notebook_gv.grid_rowconfigure(0, weight=1)
    notebook_gv.grid_columnconfigure(0, weight=1)

    # ----- Tab 1: Thông tin GV -----
    tab_thongtin = ttk.Frame(notebook_gv)
    notebook_gv.add(tab_thongtin, text="Thông tin GV")
    tab_thongtin.grid_rowconfigure(0, weight=1)
    tab_thongtin.grid_columnconfigure(0, weight=1)

    cols_tt = ["Mã GV", "Họ tên", "Giới tính", "Ngày sinh", "Vai trò", "SĐT", "Email"]
    tree_tt = ttk.Treeview(tab_thongtin, columns=cols_tt, show="headings")
    for col in cols_tt:
        tree_tt.heading(col, text=col, anchor='center')
        tree_tt.column(col, width=120, anchor='center')
    tree_tt.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # ----- Tab 2: Phân công môn dạy -----
    tab_monday = ttk.Frame(notebook_gv)
    notebook_gv.add(tab_monday, text="Phân công môn dạy")
    tab_monday.grid_rowconfigure(0, weight=1)
    tab_monday.grid_columnconfigure(0, weight=1)

    cols_monday = ["Mã GV", "Tên GV", "Môn dạy"]
    tree_monday = ttk.Treeview(tab_monday, columns=cols_monday, show="headings")
    for col in cols_monday:
        tree_monday.heading(col, text=col, anchor='center')
        tree_monday.column(col, width=150, anchor='center')
    tree_monday.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # ----- Tab 3: Tài khoản & phân quyền -----
    tab_taikhoan = ttk.Frame(notebook_gv)
    notebook_gv.add(tab_taikhoan, text="Tài khoản & quyền")
    tab_taikhoan.grid_rowconfigure(0, weight=1)
    tab_taikhoan.grid_columnconfigure(0, weight=1)

    cols_tk = ["Tên đăng nhập", "Họ tên", "Vai trò", "Trạng thái"]
    tree_tk = ttk.Treeview(tab_taikhoan, columns=cols_tk, show="headings")
    for col in cols_tk:
        tree_tk.heading(col, text=col, anchor='center')
        tree_tk.column(col, width=150, anchor='center')
    tree_tk.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # ===========================
    #    Hàm load dữ liệu giáo viên
    # ===========================
    def load_data_dsgv():
        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu.")
            return
        try:
            cursor = conn.cursor()

            # 1. Thông tin GV
            cursor.execute("""
                SELECT MaGV, HoTen, GioiTinh, NgaySinh, VaiTro, SoDT, Email
                FROM GIAOVIEN
                ORDER BY MaGV
            """)
            rows = cursor.fetchall()
            tree_tt.delete(*tree_tt.get_children())
            for row in rows:
                row = list(row)
                if row[3]:
                    row[3] = row[3].strftime("%d/%m/%Y")
                row = [r.strip() if isinstance(r, str) else r for r in row]
                tree_tt.insert("", tk.END, values=row)

            # 2. Phân công môn dạy
            cursor.execute("""
                SELECT 
                    g.MaGV, 
                    g.HoTen AS TenGV,
                    ISNULL(Mon.MonDay, '') AS MonDay
                FROM GIAOVIEN g
                LEFT JOIN (
                    SELECT 
                        gm.MaGV,
                        STRING_AGG(m.TenMon, ', ') AS MonDay
                    FROM GIAOVIEN_MONHOC gm
                    JOIN MONHOC m ON gm.MaMon = m.MaMon
                    GROUP BY gm.MaGV
                ) Mon ON g.MaGV = Mon.MaGV
                ORDER BY g.MaGV
            """)
            rows = cursor.fetchall()
            tree_monday.delete(*tree_monday.get_children())
            for row in rows:
                tree_monday.insert("", tk.END, values=(row[0], row[1], row[2]))

            # 3. Tài khoản & phân quyền
            cursor.execute("""
                SELECT 
                    t.TenDangNhap,
                    ISNULL(g.HoTen, '') AS HoTen,
                    t.VaiTro, 
                    CASE WHEN t.TrangThai=1 THEN N'Hoạt động' ELSE N'Khóa' END AS TrangThai
                FROM TAIKHOAN t
                LEFT JOIN GIAOVIEN g ON t.MaLienKet = g.MaGV
                WHERE t.VaiTro IN ('GVBM', 'GVCN', 'ADMIN')
                ORDER BY t.TenDangNhap
            """)
            rows = cursor.fetchall()
            tree_tk.delete(*tree_tk.get_children())
            for row in rows:
                tree_tk.insert("", tk.END, values=(row[0], row[1].strip() if isinstance(row[1], str) else row[1], row[2], row[3]))


        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            conn.close()

    # Gọi load
    load_data_dsgv()
    # ===========================
    #    HÀM XUẤT EXCEL DS GIÁO VIÊN
    # ===========================
    def xuat_excel_giaovien():
        import pandas as pd
        from tkinter import filedialog, messagebox

        # Chọn nơi lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Lưu file Excel danh sách giáo viên"
        )
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

                # ===== Sheet 1: Thông tin giáo viên =====
                data_tt = []
                for item in tree_tt.get_children():
                    data_tt.append(tree_tt.item(item)["values"])
                if data_tt:
                    df_tt = pd.DataFrame(data_tt, columns=cols_tt)
                    df_tt.to_excel(writer, sheet_name="ThongTinGV", index=False)

                # ===== Sheet 2: Phân công môn dạy =====
                data_md = []
                for item in tree_monday.get_children():
                    data_md.append(tree_monday.item(item)["values"])
                if data_md:
                    df_md = pd.DataFrame(data_md, columns=cols_monday)
                    df_md.to_excel(writer, sheet_name="MonDay", index=False)

                # ===== Sheet 3: Tài khoản & phân quyền =====
                data_tk = []
                for item in tree_tk.get_children():
                    data_tk.append(tree_tk.item(item)["values"])
                if data_tk:
                    df_tk = pd.DataFrame(data_tk, columns=cols_tk)
                    df_tk.to_excel(writer, sheet_name="TaiKhoan", index=False)


            messagebox.showinfo("Thành công", f"Xuất Excel thành công!\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xuất Excel: {e}")
    btn_export_gv = tk.Button(
    tab_dsgiaovien,
    text="Xuất Excel",
    bg="#4A90E2",
    fg="white",
    font=("Arial", 12, "bold"),
    command=xuat_excel_giaovien
    )
    btn_export_gv.grid(row=1, column=0, pady=10)

    # =====================================================
    # ---------------- TAB DANH SÁCH LỚP -----------------
    # =====================================================
    tab_lop.grid_rowconfigure(0, weight=1)
    tab_lop.grid_columnconfigure(0, weight=1)

    # Notebook con cho các lớp
    notebook_lop = ttk.Notebook(tab_lop)
    notebook_lop.grid(row=0, column=0, sticky="nsew")
    notebook_lop.grid_rowconfigure(0, weight=1)
    notebook_lop.grid_columnconfigure(0, weight=1)

    # Danh sách lớp (ví dụ 6 lớp)
    danh_sach_lop = ["10A1", "10A2", "11A1", "11A2", "12A1", "12A2"]
    tree_lop_dict = {}  # lưu Treeview theo lớp

    for lop in danh_sach_lop:
        tab = ttk.Frame(notebook_lop)
        notebook_lop.add(tab, text=lop)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Treeview cho từng lớp
        cols_lop = ["Mã HS", "Họ", "Tên Lót", "Tên", "Giới Tính", "Ngày Sinh", "Tình Trạng"]
        tree = ttk.Treeview(tab, columns=cols_lop, show="headings")
        for col in cols_lop:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Scrollbar
        scroll_v = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_v.set)
        scroll_v.grid(row=0, column=1, sticky="ns")
        
        tree_lop_dict[lop] = tree  # lưu lại để load dữ liệu

    # ===========================
    # Load dữ liệu học sinh theo lớp
    # ===========================
    def load_data_dshs_lop():
        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối CSDL.")
            return
        try:
            cursor = conn.cursor()
            for lop, tree in tree_lop_dict.items():
                cursor.execute("""
                    SELECT MaHS, Ho, TenLot, Ten, GioiTinh, NgaySinh, TinhTrang
                    FROM HOCSINH
                    WHERE Lop = ?
                    ORDER BY Ho, TenLot, Ten
                """, (lop,))
                rows = cursor.fetchall()
                tree.delete(*tree.get_children())
                for row in rows:
                    row = list(row)
                    if row[5]:  # Ngày sinh
                        row[5] = row[5].strftime("%d/%m/%Y")
                    row = [r.strip() if isinstance(r, str) else r for r in row]
                    tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu lớp: {e}")
        finally:
            conn.close()

    # Gọi load dữ liệu khi mở tab
    load_data_dshs_lop()
    # ===========================
    #     HÀM XUẤT EXCEL CÁC LỚP
    # ===========================
    def xuat_excel_lop():
        import pandas as pd
        from tkinter import filedialog, messagebox

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Lưu danh sách lớp ra Excel"
        )
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

                for lop, tree in tree_lop_dict.items():

                    # lấy dữ liệu Treeview
                    data = []
                    for item in tree.get_children():
                        data.append(tree.item(item)["values"])

                    # nếu lớp không có học sinh thì bỏ qua
                    if not data:
                        continue

                    df = pd.DataFrame(data, columns=cols_lop)
                    df.to_excel(writer, sheet_name=lop, index=False)

            messagebox.showinfo("Thành công", "Xuất danh sách lớp ra Excel thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xuất Excel: {e}")
    btn_export_lop = tk.Button(
    tab_lop,
    text="Xuất Excel",
    bg="#4A90E2",
    fg="white",
    font=("Arial", 12, "bold"),
    command=xuat_excel_lop
    )
    btn_export_lop.grid(row=1, column=0, pady=10)

    def tree_to_rows(tree):
        """Đọc Treeview và trả về header + data, đảm bảo đủ cột."""
        cols = [tree.heading(c)["text"] for c in tree["columns"]]
        rows = []
        for i in tree.get_children():
            vals = list(tree.item(i)["values"])
            if len(vals) < len(cols):
                vals += [""] * (len(cols) - len(vals))
            rows.append(vals)
        return cols, rows

    def export_all_to_excel():
        # Chọn file lưu
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Lưu file Excel"
        )
        if not file_path:
            return

        wb = Workbook()
        # Xóa sheet mặc định
        wb.remove(wb.active)

        try:
            # --- Học sinh HK1 ---
            cols, rows = tree_to_rows(tree_hk1)
            ws = wb.create_sheet("HS_HK1")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            # --- Học sinh HK2 ---
            cols, rows = tree_to_rows(tree_hk2)
            ws = wb.create_sheet("HS_HK2")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            # --- Khoản phí ---
            cols, rows = tree_to_rows(tree_phi)
            ws = wb.create_sheet("KhoanPhi")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            # --- Giáo viên ---
            cols, rows = tree_to_rows(tree_tt)
            ws = wb.create_sheet("GV_ThongTin")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            cols, rows = tree_to_rows(tree_monday)
            ws = wb.create_sheet("GV_PhanCong")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            cols, rows = tree_to_rows(tree_tk)
            ws = wb.create_sheet("GV_TaiKhoan")
            ws.append(cols)
            for r in rows:
                ws.append(r)

            # --- Lớp ---
            for lop, tree in tree_lop_dict.items():
                cols, rows = tree_to_rows(tree)
                ws = wb.create_sheet(f"Lop_{lop}")
                ws.append(cols)
                for r in rows:
                    ws.append(r)

            wb.save(file_path)
            messagebox.showinfo("Thành công", f"Xuất Excel thành công:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Excel: {e}")

    frame_btn = ttk.Frame(QLDS)
    frame_btn.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    btn_export = ttk.Button(frame_btn, text="Xuất Excel", command=export_all_to_excel)
    btn_export.pack()

    #================================
    #        LOAD DỮ LIỆU           #
    load_data_hs()
    load_data_phi()
    load_data_diem(tree_hk1, 1)
    load_data_diem(tree_hk2, 2) 
    load_data_gv()
    load_data_dshs_phi()
    load_data_dshs_diem(tree_hk1, 1)
    load_data_dshs_diem(tree_hk2, 2)
    admin_window.mainloop()
