import customtkinter as ctk
import sqlite3
from PIL import Image


class Edit(ctk.CTkToplevel):
    def __init__(self, file=str, table=str, create=False, row=-1, id=-1, parent=any):
        super().__init__()
        self.file = str(file)
        self.table = str(table)
        self.create = create
        self.Headers = []
        self.Entries = []
        self.RowsData = []
        self.NumRows = int
        self.row = row
        self.parent = parent
        self.id = id

        self.geometry(
            "600x400+"
            + str(int((self.winfo_screenwidth() - 600) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - 400) / 2)),
        )

        if "db" not in self.file:
            self.conn = sqlite3.connect(self.file + ".db")
        else:
            self.conn = sqlite3.connect(self.file.split(".db")[0] + ".db")
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

        self.refresh(self.table, self.file, None)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.Frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10, padx=10)

        self.bind("<Quit>", self.__del__)
        self.bind("<Return>", self.save)

    def __del__(self, event=None):
        print("deleting")
        self.parent.Frame.grid_forget()
        self.parent.refresh(self.table, self.file, None)
        self.parent.Frame.grid(row=0, column=1, sticky="nsew")
        self.destroy()

    def save(self):
        data = []
        for entry in self.Entries:
            data.append(entry.get())
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
        self.parent.refresh(self.table, self.file, None)
        self.parent.Frame.grid(row=0, column=1, sticky="nsew")
        self.destroy()

    def getEntries(self):
        return self.Entries

    def refresh(self, table, file, event):
        print("refreshing")
        try:
            self.cur.execute("SELECT * FROM " + table)
        except:
            self.conn = sqlite3.connect(file)
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
        self.RowsData = self.cur.fetchall()
        self.NumRows = len(self.RowsData)

        flag = False

        # if len(self.Headers) > 0:
        #     for col, header in enumerate(self.Headers):
        #         self.label = ctk.CTkLabel(self.Frame, text=header)
        #         self.label.grid(row=0, column=col, padx=10, pady=5)

        print(self.Headers)
        print(self.create)
        if self.create and len(self.RowsData) <= 0:
            print(self.Headers)
            for col, header in enumerate(self.Headers):
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
                                self.Frame, text=self.Headers[col] + ": "
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
                            flag = True

                        elif row == self.row:
                            self.label = ctk.CTkLabel(
                                self.Frame, text=self.Headers[col] + ": "
                            )
                            self.label.grid(
                                row=int(col / 2), column=(col % 2) * 2, padx=10, pady=5
                            )
                            entry = ctk.CTkEntry(self.Frame, width=100, state="normal")
                            entry.insert(ctk.END, value)
                            entry.grid(
                                row=int(col / 2),
                                column=(col % 2) * 2 + 1,
                                padx=10,
                                pady=5,
                            )
                            self.Entries.append(entry)


# edit = Edit("profiles.db", "rawMaterial", True, 2, None)
# edit.mainloop()
