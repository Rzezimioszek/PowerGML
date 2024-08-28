# build-in
import os.path
import threading
import time as t

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as msg

from tktooltip import ToolTip

# My
from gml_shp import save_dz_shp, save_pts_shp
from gml_sql import read_sqlite_query, save_sqlite
from gml_xlsx import save_xlsx
from gml_dict import get_gml_version, read_dict
from gml_ezdxf import Drawing

build_ver = '0.1'
class GmlGUI:
    def __init__(self):

        width = 300
        height = 280

        pad = 5

        self.root = tk.Tk()
        self.root.title(f"PowerGML  - {build_ver}")

        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.maxsize(width, 8000)

        self.root.rowconfigure((0, 1, 3, 4), weight=1)
        self.root.rowconfigure(2, weight=10)
        self.root.columnconfigure(0, weight=1)

        self.file_path = tk.StringVar()
        self.file_path.set('')
        self.file_name = tk.StringVar()
        self.file_name.set('')

        # Frame HEAD
        frm_head = ttk.Frame(self.root)
        frm_head.grid(row=0, column=0, padx=0, pady=0, sticky="news")
        frm_head.columnconfigure((0, 1), weight=1)
        frm_head.rowconfigure(0, weight=1)

        lbl_file = ttk.Label(frm_head, text="Wczytaj plik GML ----->")
        lbl_file.grid(row=0, column=0, padx=pad, pady=pad, sticky="nw")

        btn_file = ttk.Button(frm_head, textvariable=self.file_name,
                              command=lambda: self.file_path.set(self.open_file()))
        btn_file.grid(row=0, column=1, padx=pad, pady=pad, sticky="new")
        ToolTip(btn_file, msg="Wskaż ścieżkę do pliku GML w formacie EGIB 2021")

        # Frame save path

        frm_save = ttk.Frame(self.root)
        frm_save.grid(row=1, column=0, padx=0, pady=0, sticky="news")
        frm_save.columnconfigure(0, weight=5)
        frm_save.columnconfigure(1, weight=1)
        frm_save.rowconfigure(0, weight=1)

        self.svd_path = tk.StringVar()
        self.svd_path.set('')

        ent_file = ttk.Entry(frm_save, textvariable=self.svd_path, )
        ent_file.grid(row=0, column=0, padx=pad, pady=pad, sticky="new")
        ToolTip(ent_file, msg="Ścieżka z przedrostkiem do zapisanego pliku"
                              "\nNiepodanie scieżki utworzy pliki w folderze z plikiem GML")

        btn_save = ttk.Button(frm_save, text="Zapis",
                              command=lambda: self.svd_path.set(self.save_file()))
        btn_save.grid(row=0, column=1, padx=pad, pady=pad, sticky="ne")
        ToolTip(btn_save, msg="Wskaż ścieżkę zapisu plików oraz podaj przedrostek dla zapisywanych plików")


        tabControl = ttk.Notebook(self.root)

        # frame 0
        frm_0 = ttk.Frame(tabControl)
        frm_0.grid(row=0, column=0, padx=pad, pady=pad, sticky="news")

        self.v_raw = tk.BooleanVar()
        self.v_raw.set(False)
        ch_raw = ttk.Checkbutton(frm_0, text="Eksport do surowy excel", variable=self.v_raw)
        ch_raw.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_raw, msg="Zapisuje surowe dane z GML do pliku XLSX")

        self.v_sql = tk.BooleanVar()
        self.v_sql.set(False)
        ch_sql = ttk.Checkbutton(frm_0, text="Eksport do surowy sql (db)", variable=self.v_sql)
        ch_sql.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_sql, msg="Zapisuje surowe dane z GML do pliku DB (SQLite3)")

        self.v_rsql = tk.BooleanVar()
        self.v_rsql.set(False)
        ch_rsql = ttk.Checkbutton(frm_0, text="Eksport do moderowany xlsx", variable=self.v_rsql)
        ch_rsql.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_rsql, msg="Zapisuje wybrane dane opsiowe do bardziej użytecznego pliku XLSX")

        tabControl.add(frm_0, text='Opisowe')

        # frame 1

        frm_1 = ttk.Frame(tabControl)
        frm_1.grid(row=0, column=0, padx=pad, pady=pad, sticky="news")


        self.v_shp_d = tk.BooleanVar()
        self.v_shp_d.set(False)
        ch_shp_d = ttk.Checkbutton(frm_1, text="Eksport działek do SHP", variable=self.v_shp_d)
        ch_shp_d.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_shp_d, msg="Zapisuje działki do SHP")


        self.v_shp_p = tk.BooleanVar()
        self.v_shp_p.set(False)
        ch_shp_p = ttk.Checkbutton(frm_1, text="Eksport punktów granicznych do SHP", variable=self.v_shp_p)
        ch_shp_p.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_shp_p, msg="Zapisuje punkty do SHP")


        tabControl.add(frm_1, text='SHP')

        # frame 2

        frm_2 = ttk.Frame(tabControl)
        frm_2.grid(row=0, column=0, padx=pad, pady=pad, sticky="news")


        self.v_dxf_d = tk.BooleanVar()
        self.v_dxf_d.set(False)
        ch_dxf_d = ttk.Checkbutton(frm_2, text="Eksport działek do DXF", variable=self.v_dxf_d)
        ch_dxf_d.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_dxf_d, msg="Zapisuje działki do pliku DXF")

        self.v_dxf_short = tk.BooleanVar()
        self.v_dxf_short.set(False)
        ch_dxf_short = ttk.Checkbutton(frm_2, text="Numer działki zamiast identyfikatora", variable=self.v_dxf_short)
        ch_dxf_short.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_dxf_short, msg="Zapisuje numer działki zamiast pełnego identyfikatora")

        self.v_dxf_p = tk.BooleanVar()
        self.v_dxf_p.set(False)
        ch_dxf_p = ttk.Checkbutton(frm_2, text="Eksport punktów granicznych do DXF", variable=self.v_dxf_p)
        ch_dxf_p.pack(side=tk.TOP, padx=pad, pady=pad, fill=tk.X)
        ToolTip(ch_dxf_p, msg="Zapisuje punkty pod pełną nazwą do DXF")

        tabControl.add(frm_2, text='DXF')
        tabControl.grid(row=2, column=0, padx=pad, pady=pad, sticky="news")

        self.progress = tk.IntVar()
        self.prog_bar = ttk.Progressbar(self.root, maximum=100, variable=self.progress)
        self.prog_bar.grid(row=3, column=0, padx=pad, pady=pad, sticky="ews")

        btn_export = ttk.Button(self.root, text="Eksport", command=lambda: self.task())
        btn_export.grid(row=4, column=0, padx=pad, pady=pad, sticky="ews")
        ToolTip(btn_export, msg="Eksportuje na podstawie wybranych parametrów")

    def mainloop(self):
        self.root.mainloop()

    def task(self):
        self.progress.set(0)
        threading.Thread(target=self.read_gml,
                         args=(self.file_path.get(), self.svd_path.get()),
                         daemon=True).start()

    def open_file(self):

        filetypes_option = (("pliki gml", "*.gml"), ("pliki txt", "*.txt"), ("Wszystkie pliki", "*.*"))
        path = filedialog.askopenfilenames(title="Wybierz plik lub pliki", filetypes=filetypes_option)
        if path is not None:
            path = str(path).replace("('", "")
            path = path.replace("',)", "\t")
            path = path.replace("')", "\t")
            path = path.replace("', '", "\t")
            path = path.strip()

            self.file_name.set(os.path.basename(path))

            return path

        return None

    def save_file(self):
        filetypes = (("dane wynikowe", ".xlsx .shp .prj .qml .db .shx .dbf, .dxf"), ("Wszystkie pliki", "*.*"))
        path = filedialog.asksaveasfilename(title="Wybierz miejsce zapisu plików", filetypes=filetypes)
        if path is not None:
            return path
        return ""

    def read_gml(self, path: str, svd_path: str=''):

        if path == '':
            msg.showerror("Brak pliku gml", 'Niewybrano pliku gml')
            return

        if not os.path.exists(path):
            msg.showerror("Plik GML"
                          , "Plik wejściowy niepoprawny lub nieistnieje we wskazanej lokalizacji")
            return

        tic = t.perf_counter()

        # Sprawdzenie wersji gml
        try:
            version = get_gml_version(path)
            print(f'GML version: {version}')
        except Exception as e:
            version = '2021'
            msg.showerror("Błąd wersji"
                          , f"Brak pewności przy interpretacji wersji GML.\n\n{e}")

        # Wczytanie GMLa do słownika
        try:
            bdict, tags = read_dict(path)
            self.prog_bar.step(30)
        except Exception as e:
            msg.showerror("Błąd DICT"
                          , f"Błąd podczas tworzenia słownika.\n\n{e}")

        # Ścieżka bez rozszerzenia
        if svd_path == '':
            svd_path = path[:-4]
        else:
            svd_path = svd_path

        # Zapis surowych danych do XLSX
        if self.v_raw.get():
            try:
                save_xlsx(bdict, svd_path)
                self.prog_bar.step(15)
            except Exception as e:
                msg.showerror("Błąd XLSX"
                              , f"Błąd podczas tworzenia pliku Excel (.xlsx).\n\n{e}")

        # Zapis danych do SQLite3
        if self.v_sql.get() or self.v_rsql.get():
            try:
                save_sqlite(bdict, svd_path, tags)
                self.prog_bar.step(15)
            except Exception as e:
                msg.showerror("Błąd SQL"
                              , f"Błąd podczas tworzenia pliku SQLite3 (.db).\n\n{e}")

        # Utworzenie Relacji
        if self.v_rsql.get() and version == '2021':
            try:
                read_sqlite_query(bdict, svd_path, self.v_sql.get())
                self.prog_bar.step(15)
            except Exception as e:
                msg.showerror("Błąd SQL"
                              , f"Błąd podczas tworzenia relacji SQLite3 (.db).\n\n{e}")

        # Zapis działek do SHP
        if self.v_shp_d.get():
            try:
                save_dz_shp(bdict, svd_path)
                self.prog_bar.step(15)
            except Exception as e:
                msg.showerror("Błąd SHP"
                              , f"Błąd podczas zapisu działek do SHP.\n\n{e}")

        # Zapis punktów granicznych do SHP
        if self.v_shp_p.get():
            try:
                save_pts_shp(bdict, svd_path, version)

            except Exception as e:
                msg.showerror("Błąd SHP"
                              , f"Błąd podczas zapisu punktów granicznych do SHP.\n\n{e}")

        if self.v_dxf_d.get() or self.v_dxf_p.get():
            dxf = Drawing(bdict)

            # Utworzenie działek do DXF
            if self.v_dxf_d.get():
                dxf.add_poly_with_centroid(shortname=self.v_dxf_short.get())

            # Utworzenie punktów granicznych do DXF
            if self.v_dxf_p.get():
                dxf.add_points()

            # Zapis do pliku
            er = dxf.save(svd_path)
            if not er:
                mess = "Błąd podczas zapisu DXF.\nPlik jest otwarty przez inny program lub nieprawidłowe dane wejściowe"
                msg.showerror("Błąd DXF", mess)

        self.progress.set(100)

        # Informacje o zakończeniu taska
        toc = t.perf_counter()
        ftime = f"{toc - tic:0.4f}s"
        print(f"Wyeksportowano dane zawarte w pliku gml.\n{ftime}")
        msg.showinfo("Eksport zakończony"
                     , f"Wyeksportowano dane zawarte w pliku gml.\n{ftime}")


if __name__ == "__main__":
    gui = GmlGUI()
    gui.mainloop()