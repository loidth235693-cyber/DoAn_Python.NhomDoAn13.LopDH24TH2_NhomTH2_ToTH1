# gvbm.py
import tkinter as tk
from tkinter import IntVar, ttk, messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
from connect_db import connect_db
import font
import pandas as pd  # nếu cần xuất Excel sau này

def gvbm_window(magv):
    gvbm_window = tk.Tk()
    gvbm_window.title("Giao diện GVBM")
    gvbm_window.geometry("1200x700")
    gvbm_window.configure(bg=font.BG_COLOR)

    for i in range(4):
        gvbm_window.grid_rowconfigure(i, weight=1)
    gvbm_window.grid_columnconfigure(0, weight=1)
    # ===== Tiêu đề =====
    title_label = tk.Label(
        gvbm_window, text="HỆ THỐNG QUẢN LÝ HỌC SINH",
        font=font.FONT_TIEUDE, bg="#E8F4FB", fg="#0A3D62", pady=10
    )
    title_label.grid(row=0, column=0, sticky="ew")
    gvbm_window.grid_columnconfigure(0, weight=1)

    style = ttk.Style()
    style.theme_use('default')  # đảm bảo theme mặc định để có thể chỉnh màu
    style.configure('TNotebook.Tab', background="#E8F4FB", foreground='black', padding=[10, 5])
    gvbm_window.grid_rowconfigure(1, weight=1)
    gvbm_window.grid_columnconfigure(0, weight=1)

    # ===== Khung chính =====
    frame_cha = tk.Frame(gvbm_window, bg=font.BG_COLOR)
    frame_cha.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    # Tạo frame_con để chứa 2 frame HS và Điểm, căn giữa
    frame_con = tk.Frame(frame_cha, bg=font.BG_COLOR)
    frame_con.grid(row=0, column=0)
    # Căn giữa frame_con trong frame_cha
    frame_cha.grid_columnconfigure(0, weight=1)

    # ---------------- Frame HS ----------------
    frame_hs = ttk.LabelFrame(frame_con, text="Thông tin học sinh", padding=10)
    frame_hs.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
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
    frame_diem = ttk.LabelFrame(frame_con, text="Điểm học kỳ", padding=10)
    frame_diem.grid(row=1, column=1, sticky="n", padx=10, pady=10)
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

   # ---------------- Tab lớp trực tiếp trong scrollable_frame ----------------
    # Danh sách lớp
    danh_sach_lop = ["10A1","10A2","11A1","11A2","12A1","12A2"]

    # Notebook chính: mỗi tab là một lớp
    notebook_lop = ttk.Notebook(gvbm_window)
    notebook_lop.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    gvbm_window.grid_rowconfigure(1, weight=1)
    gvbm_window.grid_columnconfigure(0, weight=1)

    # Hàm tạo treeview
    def create_treeview(tab, cols, height=0):
        tree = ttk.Treeview(tab, columns=cols, show="headings", height=height)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        scroll_v = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        scroll_h = ttk.Scrollbar(tab, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        return tree

    # Cột thông tin HS
    cols_info = ["Mã HS","Họ","Tên lót","Tên","Giới tính","Ngày sinh","Lớp","Tình trạng"]
    # Cột điểm HS
    cols_diem = ["Mã HS","Họ tên","Lớp","Toán","Ngữ văn","Tiếng Anh","GDCD","Lịch sử",
                "Địa lí","Vật lí","Hóa học","Sinh học","Tin học","Công nghệ","TBCN","Xếp loại"]

    # Tạo các tab lớp
    tree_dict = {}  # lưu treeview theo lớp
    for lop in danh_sach_lop:
        tab_lop = ttk.Frame(notebook_lop)
        notebook_lop.add(tab_lop, text=lop)

        # Notebook nhỏ bên trong tab lớp
        notebook_lop_con = ttk.Notebook(tab_lop)
        notebook_lop_con.grid(row=0, column=0, sticky="nsew")

        # Tab Thông tin
        tab_info = ttk.Frame(notebook_lop_con)
        notebook_lop_con.add(tab_info, text="Thông tin")
        tree_info = create_treeview(tab_info, cols_info, height=5)

        # Tab Điểm
        tab_diem = ttk.Frame(notebook_lop_con)
        notebook_lop_con.add(tab_diem, text="Điểm")
        tree_diem = create_treeview(tab_diem, cols_diem, height=5)

        tree_dict[lop] = {"info": tree_info, "diem": tree_diem}

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
        # Xóa toàn bộ dữ liệu trong tất cả treeview
        for lop in tree_dict:
            tree_dict[lop]["info"].delete(*tree_dict[lop]["info"].get_children())

        conn = connect_db()
        if not conn:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu.")
            return

        try:
            cursor = conn.cursor()

            # Lấy toàn bộ danh sách lớp
            cursor.execute("SELECT MaLop FROM LOP ORDER BY MaLop ASC")
            ds_lop = [row[0].strip() for row in cursor.fetchall()]

            if not ds_lop:
                messagebox.showinfo("Thông báo", "Không có lớp nào trong CSDL.")
                return

            for lop in ds_lop:

                # Chỉ load lớp có tồn tại TreeView
                if lop not in tree_dict:
                    continue

                # Lấy danh sách học sinh theo từng lớp
                cursor.execute("""
                    SELECT MAHS, HO, TENLOT, TEN, GIOITINH, NGAYSINH, LOP, TINHTRANG
                    FROM HOCSINH
                    WHERE LOP = ?
                    ORDER BY TEN ASC
                """, lop)

                for row in cursor.fetchall():
                    row = list(row)

                    # Format ngày sinh
                    if row[5]:
                        row[5] = row[5].strftime("%d/%m/%Y")

                    # Xóa khoảng trắng
                    row = [r.strip() if isinstance(r, str) else r for r in row]

                    # Đưa vào TreeView của lớp
                    tree_dict[lop]["info"].insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))

        finally:
            conn.close()

    def load_data_diem(tree_dict, hocky):
        conn = connect_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()

             # 1) Lấy danh sách môn học từ DB
            cursor.execute("SELECT TenMon FROM MONHOC ORDER BY TenMon")
            ds_monhoc = [r[0] for r in cursor.fetchall()]

            # Lấy danh sách lớp
            cursor.execute("SELECT MaLop FROM LOP ORDER BY MaLop")
            ds_lop = [r[0].strip() for r in cursor.fetchall()]

            for lop in ds_lop:
                if lop not in tree_dict:
                    continue

                treeview = tree_dict[lop]["diem"]
                treeview.delete(*treeview.get_children())

                # Cấu hình cột Treeview
                cols = ["Mã HS", "Họ tên", "Lớp"] + ds_monhoc + ["TBCN", "Xếp loại"]
                treeview.config(columns=cols, show="headings")
                for col in cols:
                    treeview.heading(col, text=col)
                    treeview.column(col, anchor="center", width=95)

                # Pivot lấy TBM đã tính sẵn
                pivot_mon = ", ".join([
                    f"MAX(CASE WHEN LTRIM(RTRIM(m.TenMon)) = N'{mon}' THEN d.TBM END) AS [{mon}]"
                    for mon in ds_monhoc
                ])

                sql = f"""
                    SELECT 
                        hs.MaHS,
                        (hs.Ho + ' ' + hs.TenLot + ' ' + hs.Ten) AS HoTen,
                        hs.Lop,
                        {pivot_mon},
                        hs.DiemTBCN,
                        hs.XepLoai
                    FROM HOCSINH hs
                    LEFT JOIN DIEM d ON hs.MaHS = d.MaHS AND d.HocKy = ?
                    LEFT JOIN MONHOC m ON d.MaMon = m.MaMon
                    WHERE hs.Lop = ?
                    GROUP BY hs.MaHS, hs.Ho, hs.TenLot, hs.Ten, hs.Lop, hs.DiemTBCN, hs.XepLoai
                    ORDER BY hs.Ten
                """

                cursor.execute(sql, (hocky, lop))
                for row in cursor.fetchall():
                    row = ["" if v is None else v for v in row]
                    treeview.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Lỗi SQL", f"Lỗi tải điểm TBM: {e}")
        finally:
            conn.close()

    def sua_hs():
        # --- Lấy tab lớp đang chọn ---
        selected_tab = notebook_lop.nametowidget(notebook_lop.select())
        notebook_lop_con = selected_tab.winfo_children()[0]  # Notebook nhỏ trong tab lớp
        tab_info = notebook_lop_con.nametowidget(notebook_lop_con.tabs()[0])  # Tab "Thông tin"
        tree_info = tab_info.winfo_children()[0]  # Treeview HS

        # --- Lấy học sinh đang chọn ---
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

           # Điền dữ liệu vào form thông tin và khóa các ô
            # Điền dữ liệu vào form thông tin và khóa các ô
            for i, entry in enumerate(entries_hs):
                value = row[i]
                
                if isinstance(entry, ttk.Combobox):
                    entry.set(value if value else '')
                    entry.config(state="disabled")  # khóa combobox
                elif isinstance(entry, DateEntry):
                    try:
                        entry.set_date(value)
                    except:
                        entry.set_date(datetime.now())
                    entry.config(state="disabled")  # khóa DateEntry
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value if value else '')
                    entry.config(state="readonly")  # khóa entry (không chỉnh sửa)

                # ---------------- 2) Load DIEM ----------------
            # 1) Lấy danh sách môn học từ DB, chuẩn hóa tên môn
            cur.execute("SELECT TenMon, MaMon FROM MONHOC ORDER BY TenMon")
            ds_monhoc_rows = cur.fetchall()
            ds_monhoc = [r[0].strip() for r in ds_monhoc_rows]
            ten_to_ma = {r[0].strip(): r[1] for r in ds_monhoc_rows}

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
                diem_dict[(ten_mon.strip(), hoc_ky)] = [b1, b2, b3, b4]

            # 4) Lấy danh sách môn giáo viên phụ trách
            cur.execute("SELECT MaMon FROM GIAOVIEN_MONHOC WHERE MaGV = ?", (magv,))
            mon_gv_day = [r[0] for r in cur.fetchall()]

            # 5) Điền dữ liệu vào Entry, tạo Entry nếu chưa có
            for mon in ds_monhoc:
                ma_mon = ten_to_ma[mon]
                for hoc_ky, target_dict, frame in [(1, entry_diem_hk1, tab_hk1), (2, entry_diem_hk2, tab_hk2)]:
                    for col in ["B1","B2","B3","B4"]:
                        key = f"{mon}_{col}"
                        if key not in target_dict:
                            e = tk.Entry(frame, width=7, justify="center", font=font.FONT_CHU)
                            row_idx = ds_monhoc.index(mon) + 1
                            col_idx = ["B1","B2","B3","B4"].index(col) + 1
                            e.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="ew")
                            target_dict[key] = e

                        # Điền dữ liệu
                        values = diem_dict.get((mon, hoc_ky), [None, None, None, None])
                        target_dict[key].delete(0, tk.END)
                        target_dict[key].insert(0, values[["B1","B2","B3","B4"].index(col)]
                                                if values[["B1","B2","B3","B4"].index(col)] is not None else "")

                        # Khóa Entry nếu giáo viên không dạy môn đó
                        if ma_mon not in mon_gv_day:
                            target_dict[key].config(state="readonly")
                        else:
                            target_dict[key].config(state="normal")

            messagebox.showinfo("Thông báo", f"Dữ liệu học sinh {ma_hs} đã được tải!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu học sinh: {e}")
        finally:
            conn.close()

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

            # Lấy môn GV dạy
            cur.execute("SELECT MonDay FROM GIAOVIEN WHERE MaGV = ?", (magv,))
            row = cur.fetchone()
            mon_day = row[0] if row else None
            if not mon_day:
                messagebox.showerror("Lỗi", "Không xác định được môn GV dạy.")
                return

            # Lấy MaMon
            cur.execute("SELECT MaMon FROM MONHOC WHERE TenMon=?", (mon_day,))
            ma_mon = cur.fetchone()
            if not ma_mon:
                messagebox.showerror("Lỗi", f"Không tìm thấy môn {mon_day}.")
                return
            ma_mon = ma_mon[0]

            # Cập nhật điểm, nếu chưa có thì INSERT
            for hoc_ky, entry_dict in [(1, entry_diem_hk1), (2, entry_diem_hk2)]:
                values = {}
                for col in ["B1","B2","B3","B4"]:
                    key = f"{mon_day}_{col}"
                    entry = entry_dict.get(key)
                    val = float(entry.get().strip()) if entry and entry.get().strip() != "" else None
                    values[col] = val

                # Kiểm tra DIEM đã có chưa
                cur.execute("SELECT COUNT(*) FROM DIEM WHERE MaHS=? AND MaMon=? AND HocKy=? AND NamHoc=?", (ma_hs, ma_mon, hoc_ky, "2024-2025"))
                if cur.fetchone()[0] == 0:
                    # Chưa có => INSERT
                    cur.execute("""
                        INSERT INTO DIEM (MaHS, MaMon, HocKy, NamHoc, B1, B2, B3, B4)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ma_hs, ma_mon, hoc_ky, "2024-2025", values["B1"], values["B2"], values["B3"], values["B4"]))
                else:
                    # Đã có => UPDATE
                    cur.execute(f"""
                        UPDATE DIEM
                        SET B1=?, B2=?, B3=?, B4=?
                        WHERE MaHS=? AND MaMon=? AND HocKy=? AND NamHoc=?
                    """, (values["B1"], values["B2"], values["B3"], values["B4"], ma_hs, ma_mon, hoc_ky, "2024-2025"))

            conn.commit()
            messagebox.showinfo("Thông báo", f"Đã lưu điểm học sinh {ma_hs} thành công!")
            lam_moi_form()
            # Reload lại điểm Treeview
            load_data_diem(tree_dict, 1)
            load_data_diem(tree_dict, 2)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Lưu thất bại: {e}")
        finally:
            conn.close()

    def lam_moi_form():
        """Xóa toàn bộ dữ liệu kể cả các ô đang readonly hoặc disabled"""

        try:
            # --- 1) Xóa thông tin học sinh ---
            for entry in entries_hs:

                # ********* Combobox *********
                if isinstance(entry, ttk.Combobox):
                    entry.config(state="normal")     # mở khóa
                    entry.set('')                   # xóa giá trị
                    entry.config(state="readonly")  # khóa lại (nếu muốn)

                # ********* DateEntry *********
                elif isinstance(entry, DateEntry):
                    entry.config(state="normal")  
                    entry.set_date(datetime.today())
                    entry.config(state="normal")  # DateEntry thường không dùng readonly

                # ********* Entry thường *********
                else:
                    entry.config(state="normal")  # mở khóa
                    entry.delete(0, tk.END)
                    entry.config(state="normal")  # giữ bình thường để cho sửa tiếp

            # --- 2) Xóa điểm học kỳ 1 ---
            for key, entry in entry_diem_hk1.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.config(state="normal")

            # --- 3) Xóa điểm học kỳ 2 ---
            for key, entry in entry_diem_hk2.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.config(state="normal")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới form!\n{e}")

    def thoat():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát ứng dụng?"):
            gvbm_window.destroy()

    def export_excel_by_class():
        lop = combo_lop_export.get()
        if not lop or lop not in tree_dict:
            messagebox.showwarning("Chú ý", "Chọn lớp hợp lệ để xuất Excel!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=f"Lưu file Excel lớp {lop}"
        )
        if not file_path:
            return

        tree = tree_dict[lop]["info"]  # xuất dữ liệu thông tin học sinh
        columns = [tree.heading(col)["text"] for col in tree["columns"]]
        data = [tree.item(item)["values"] for item in tree.get_children()]
        df = pd.DataFrame(data, columns=columns)

        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", f"Xuất Excel lớp {lop} thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Excel:\n{e}")

    # ====== FRAME NÚT CHỨC NĂNG DƯỚI CÙNG ======
    frame_button = tk.Frame(gvbm_window, bg=font.BG_COLOR)
    frame_button.grid(row=3, column=0, sticky="ew", pady=0)
    gvbm_window.grid_rowconfigure(2, weight=0)
    gvbm_window.grid_columnconfigure(0, weight=1)

    # Khung con để căn giữa
    frame_button_center = tk.Frame(frame_button, bg=font.BG_COLOR)
    frame_button_center.grid(row=0, column=0)
    frame_button.grid_columnconfigure(0, weight=1)

    tk.Label(frame_button_center, text="Chọn lớp:", bg=font.BG_COLOR, font=font.FONT_CHU).grid(row=0, column=0, padx=5)
    combo_lop_export = ttk.Combobox(frame_button_center, values=danh_sach_lop, state="readonly", width=10)
    combo_lop_export.grid(row=0, column=6, padx=5)
    combo_lop_export.current(0)

    btn_export_class = tk.Button(
    frame_button_center,
    text="📄 Xuất Excel",
    width=14,
    bg="#27ae60", fg="white",
    font=font.FONT_CHU,
    command=export_excel_by_class
    )
    btn_export_class.grid(row=0, column=5, padx=8)

    # ====== NÚT ======
    btn_update = tk.Button(frame_button_center, text="Sửa", width=12,
                       bg="#3326AD", fg="white", font=font.FONT_CHU,
                       command=sua_hs)
    btn_update.grid(row=0, column=0, padx=10)

    btn_clear = tk.Button(frame_button_center, text="Lưu", width=12,
                        bg="#3326AD", fg="white", font=font.FONT_CHU,
                        command=luu_hs)
    btn_clear.grid(row=0, column=1, padx=10)
    btn_lam_moi_hs = tk.Button(
            frame_button_center, text="🔄 Làm mới", command=lam_moi_form, width=12,
            font=font.FONT_CHU, bg="#3326AD", fg="white"
        )
    btn_lam_moi_hs.grid(row=0, column=4, padx=8)
    btn_thoat = tk.Button(
            frame_button_center, text="Thoát", command=thoat, width=12,
            font=font.FONT_CHU, bg="#D4072D", fg="white"
        )
    btn_thoat.grid(row=0, column=4, padx=8)


        # Khi mở giao diện
    load_data_hs(magv)                     # load thông tin HS
    load_data_diem(tree_dict, 1)     # load điểm HK1 cho tất cả lớp
    load_data_diem(tree_dict, 2)     # load điểm HK2 cho tất cả lớp

    
    gvbm_window.mainloop()
