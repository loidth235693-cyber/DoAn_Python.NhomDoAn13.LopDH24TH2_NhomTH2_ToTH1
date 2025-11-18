import tkinter as tk
from tkinter import ttk
from connect_db import connect_db
import datetime
import font

def hocsinh_window(mahs):
    hs_win = tk.Tk()
    hs_win.title("Giao diện học sinh")
    hs_win.state('zoomed')
    hs_win.configure(bg=font.BG_COLOR)

    # ====== Cấu hình grid cho hs_win ======
    hs_win.grid_rowconfigure(1, weight=1)
    hs_win.grid_columnconfigure(1, weight=1)

    # ====== Tiêu đề ======
    title_label = tk.Label(
        hs_win,
        text="🎓 Xin chào Học Sinh",
        font=("Times New Roman", 17, "bold"),
        bg="#E8F4FB", fg="#0A3D62"
    )
    title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # ====== Frame thông tin cá nhân ======
    fields = ['Mã HS','Họ và tên','Giới tính','Ngày sinh','Lớp','Điểm TB CN','Xếp loại','Tình trạng']

    frame_info = tk.Frame(hs_win, bg=font.PANEL_BG, bd=2, relief="groove")
    frame_info.grid(row=1, column=0, sticky="ns", padx=10, pady=10)
    
    for i in range(len(fields)+1):
        frame_info.grid_rowconfigure(i, weight=1)
    frame_info.grid_columnconfigure(1, weight=1)

    tk.Label(frame_info, text="THÔNG TIN HỌC SINH", bg=font.PANEL_BG, fg=font.FG_COLOR,
             font=font.FONT_TIEUDE).grid(row=0, column=0, columnspan=2, pady=(10,20))

    entries = {}
    for i, field in enumerate(fields):
        tk.Label(frame_info, text=field, anchor='w', bg=font.PANEL_BG, fg=font.FG_COLOR,
                 font=font.FONT_LABEL).grid(row=i+1, column=0, padx=5, pady=5, sticky='w')
        ent = tk.Entry(frame_info, width=25, state='readonly', justify='center', font=font.FONT_CHU)
        ent.grid(row=i+1, column=1, padx=5, pady=5, sticky='ew')
        entries[field] = ent

    # ====== Frame tab bên phải ======
    frame_tabs = tk.Frame(hs_win, bg=font.BG_COLOR)
    frame_tabs.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    frame_tabs.grid_rowconfigure(0, weight=1)
    frame_tabs.grid_columnconfigure(0, weight=1)

    tab_control = ttk.Notebook(frame_tabs)
    tab_control.grid(row=0, column=0, sticky="nsew")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TNotebook.Tab', font=font.FONT_LABEL, padding=[10,5])
    style.configure('Treeview', font=font.FONT_CHU, rowheight=25)
    style.configure('Treeview.Heading', font=font.FONT_LABEL)

    # ====== Tab Điểm ======
    tab_diem = ttk.Frame(tab_control)
    tab_control.add(tab_diem, text="Điểm học kỳ")
    tab_diem.grid_rowconfigure(0, weight=1)
    tab_diem.grid_columnconfigure(0, weight=1)

    notebook_diem = ttk.Notebook(tab_diem)
    notebook_diem.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tab_hk1 = ttk.Frame(notebook_diem)
    tab_hk2 = ttk.Frame(notebook_diem)
    notebook_diem.add(tab_hk1, text="Học kỳ 1")
    notebook_diem.add(tab_hk2, text="Học kỳ 2")

    # Treeview có scrollbar cho HK1
    tree_diem_hk1 = ttk.Treeview(tab_hk1, columns=("Môn","B1","B2","B3","B4","TBM"), show="headings")
    tree_diem_hk2 = ttk.Treeview(tab_hk2, columns=("Môn","B1","B2","B3","B4","TBM"), show="headings")

    for tree in (tree_diem_hk1, tree_diem_hk2):
        vsb = ttk.Scrollbar(tree.master, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        vsb.grid(row=0, column=1, sticky="ns")
        tree.master.grid_rowconfigure(0, weight=1)
        tree.master.grid_columnconfigure(0, weight=1)
        for col in ("Môn","B1","B2","B3","B4","TBM"):
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

    # ====== Tab Khoản phí ======
    tab_phi = ttk.Frame(tab_control)
    tab_control.add(tab_phi, text="Khoản phí")
    tab_phi.grid_rowconfigure(0, weight=1)
    tab_phi.grid_columnconfigure(0, weight=1)

    tree_phi = ttk.Treeview(tab_phi, columns=("Học phí","BHYT","BHTN","Tháng BHYT","Mức BHTN","Tổng tiền"), show="headings")
    vsb_phi = ttk.Scrollbar(tab_phi, orient="vertical", command=tree_phi.yview)
    tree_phi.configure(yscrollcommand=vsb_phi.set)
    tree_phi.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    vsb_phi.grid(row=0, column=1, sticky="ns")
    for col in ("Học phí","BHYT","BHTN","Tháng BHYT","Mức BHTN","Tổng tiền"):
        tree_phi.heading(col, text=col)
        tree_phi.column(col, width=120, anchor='center')

    # ====== Load dữ liệu ======
    def load_hocsinh_info(mahs):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT MaHS, HoTen, GioiTinh, NgaySinh, Lop, DiemTBCN, XepLoai, TinhTrang
            FROM HOCSINH WHERE MaHS=?
        """, (mahs,))
        row = cur.fetchone()
        if row:
            hoten = row[1]
            title_label.config(text=f"🎓 Xin chào {hoten}")
            for i, field in enumerate(fields):
                entries[field].config(state='normal')
                value = row[i]
                if isinstance(value, datetime.date):
                    value = value.strftime('%Y-%m-%d')
                elif value is None:
                    value = ""
                entries[field].delete(0, tk.END)
                entries[field].insert(0, value)
                entries[field].config(state='readonly')
        conn.close()
        
    def load_diem(mahs):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT M.TenMon, D.HocKy, D.B1, D.B2, D.B3, D.B4, D.TBM
            FROM DIEM D
            JOIN MONHOC M ON D.MaMon = M.MaMon
            WHERE D.MaHS=? ORDER BY M.TenMon
        """, (mahs,))
        rows = cur.fetchall()
        tree_diem_hk1.delete(*tree_diem_hk1.get_children())
        tree_diem_hk2.delete(*tree_diem_hk2.get_children())

        for r in rows:
            if r.HocKy == 1:
                tree_diem_hk1.insert('', tk.END, values=[r.TenMon, r.B1, r.B2, r.B3, r.B4, r.TBM])
            elif r.HocKy == 2:
                tree_diem_hk2.insert('', tk.END, values=[r.TenMon, r.B1, r.B2, r.B3, r.B4, r.TBM])
        conn.close()

    def load_khoanphi(mahs):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT HocPhi, BHYT, BHTN, Thang_BHYT, Muc_BHTN, TongTien
            FROM KHOANPHI WHERE MaHS=? ORDER BY NamHoc
        """, (mahs,))
        rows = cur.fetchall()
        tree_phi.delete(*tree_phi.get_children())
        for r in rows:
            tree_phi.insert('', tk.END, values=[r.HocPhi, r.BHYT, r.BHTN, r.Thang_BHYT, r.Muc_BHTN, r.TongTien])

    # ==================== Load tất cả ====================
    load_diem(mahs)
    load_khoanphi(mahs)
    load_hocsinh_info(mahs)
    hs_win.mainloop()
