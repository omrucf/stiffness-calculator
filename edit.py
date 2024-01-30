import customtkinter as ctk
import sqlite3
from PIL import Image


class Edit(ctk.CTkToplevel):
    def __init__(self, table=str, create=False, row=-1, id=-1, parent=any):
        super().__init__()

        self.focus()
        self.table = str(table)
        self.create = create
        self.Headers = []
        self.Entries = []
        self.RowsData = []
        self.NumRows = int
        self.row = row
        self.parent = parent
        self.id = id

        self.parent.wins = 1

        self.geometry(
            "600x400+"
            + str(int((self.winfo_screenwidth() - 600) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - 400) / 2)),
        )
        if self.create:
            self.title("Create")
        else:
            self.title("Edit")

        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()

        self.Frame = ctk.CTkScrollableFrame(
            self,
            width=450,
            height=300,
            fg_color="grey40",
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
        )
        save = ctk.CTkButton(
            self, text="Save", command=self.save, width=100, bg_color="transparent"
        )
        save.grid(pady=5, row=1, column=1)

        self.refresh(self.table, None)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.Frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10, padx=10)

        # self.bind("<destroy>", self.__del__)
        self.protocol("WM_DELETE_WINDOW", self.__del__)
        self.bind("<Return>", self.save)
        self.focus_force()

    def __del__(self, event=None):
        self.parent.Frame.grid_forget()
        self.parent.refresh(self.table, None)
        self.parent.Frame.grid(row=0, column=1, sticky="nsew")
        self.destroy()

    def save(self):
        data = []
        temp = 0
        for i, entry in enumerate(self.Entries):
            if entry.get() == "" and self.nullity[i + 1][1] == 1:
                entry.configure(fg_color=("#e08288", "#6e4441"), border_color="#f51505")
                temp = temp + 1
            else:
                entry.configure(
                    fg_color=("white", "grey20"), border_color=("#999EA3", "grey30")
                )
            data.append(entry.get())
        if temp > 0:
            return
        data = tuple(data)
        if self.create:
            self.cur.execute(
                """
                             INSERT INTO
                             """
                + self.table
                + " "
                + str(tuple(self.Headers))
                + """VALUES """
                + str(data)
                + """;"""
            )
        else:
            self.cur.execute(
                """
                             UPDATE
                             """
                + self.table
                + """
                             SET
                             """
                + str(tuple(self.Headers))
                + """ = """
                + str(data)
                + """ WHERE id = """
                + str(self.id)
                + """;"""
            )

        self.conn.commit()

        self.parent.Frame.grid_forget()
        self.parent.refresh(self.table, None)
        self.parent.Frame.grid(row=0, column=1, sticky="nsew")
        self.parent.wins = 0
        self.destroy()

    def getEntries(self):
        return self.Entries

    def refresh(self, table, event):
        try:
            self.cur.execute("SELECT * FROM " + table)
        except:
            self.conn = sqlite3.connect("data.db")
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM " + table)
        self.Frame.destroy()
        # self.Frame.grid
        self.Frame = ctk.CTkScrollableFrame(
            self,
            width=450,
            height=300,
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
            fg_color="transparent",
        )
        self.Frame.grid_columnconfigure(0, weight=1)
        self.Frame.grid_columnconfigure(1, weight=1)

        self.Headers = [description[0] for description in self.cur.description[1::]]
        self.headers = self.Headers.copy()
        for i in range(len(self.Headers)):
            if self.headers[i] == "weight":
                self.headers[i] = "weight (kg)"
            elif self.headers[i] == "mold_optimal_temprature":
                self.headers[i] = "mold_optimal_temprature (°C)"
            elif self.headers[i] == "density":
                self.headers[i] = "density (g/cm³)"
            elif self.headers[i] == "elastic_modulus":
                self.headers[i] = "elastic_modulus (MPa)"
            elif self.headers[i] == "shrinkage":
                self.headers[i] = "shrinkage (%)"
            elif self.headers[i] == "profile":
                pass
            else:
                self.headers[i] = self.headers[i] + " (mm)"
                
        for i in range(len(self.Headers)):
            if self.headers[i] == "profile":
                pass
            else:
                self.headers[i] = self.headers[i].replace("_", " ")

        print(self.headers)
        self.RowsData = self.cur.fetchall()
        self.NumRows = len(self.RowsData)
        self.cur.execute("PRAGMA table_info(" + table + ");")
        temp = self.cur.fetchall()
        self.nullity = []
        for tup in temp:
            self.nullity.append((tup[1], tup[3]))

        flag = False

        # if len(self.Headers) > 0:
        #     for col, header in enumerate(self.Headers):
        #         self.label = ctk.CTkLabel(self.Frame, text=header)
        #         self.label.grid(row=0, column=col, padx=10, pady=5)

        if self.create and len(self.RowsData) <= 0:
            for col, header in enumerate(self.headers):
                self.label = ctk.CTkLabel(self.Frame, text=header)
                self.label.grid(
                    row=int(col / 2),
                    column=(col % 2) * 2,
                    padx=10,
                    pady=5,
                )
                entry = ctk.CTkEntry(self.Frame, width=100, state="normal")
                entry.grid(
                    row=int(col / 2),
                    column=(col % 2) * 2 + 1,
                    padx=10,
                    pady=5,
                )
                self.Entries.append(entry)
                flag = True
        if len(self.RowsData) > 0:
            for row, row_data in enumerate(self.RowsData, start=1):
                if not flag:
                    for col, value in enumerate(row_data[1::]):
                        if self.create and len(self.RowsData) > 0:
                            self.label = ctk.CTkLabel(
                                self.Frame, text=self.headers[col] + ": "
                            )
                            self.label.grid(
                                row=int(col / 2), column=(col % 2) * 2, padx=10, pady=5
                            )
                            entry = ctk.CTkEntry(self.Frame, width=100, state="normal")
                            entry.grid(
                                row=int(col / 2),
                                column=(col % 2) * 2 + 1,
                                padx=10,
                                pady=5,
                            )
                            self.Entries.append(entry)
                            if self.nullity[col + 1][1] == 1:
                                self.label.configure(
                                    text=self.label.cget("text")[0:-2] + "*:"
                                )
                            flag = True

                        elif row == self.row:
                            self.label = ctk.CTkLabel(
                                self.Frame, text=self.headers[col] + ": "
                            )
                            self.label.grid(
                                row=int(col / 2), column=(col % 2) * 2, padx=10, pady=5
                            )
                            entry = ctk.CTkEntry(self.Frame, width=100, state="normal")
                            if self.nullity[col + 1][1] == 1:
                                self.label.configure(
                                    text=self.label.cget("text")[0:-2] + "*:"
                                )
                                entry.insert(ctk.END, value)

                            entry.grid(
                                row=int(col / 2),
                                column=(col % 2) * 2 + 1,
                                padx=10,
                                pady=5,
                            )
                            self.Entries.append(entry)
