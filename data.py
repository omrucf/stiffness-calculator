import customtkinter as ctk
import sqlite3


class data(ctk.CTk):
    def __init__(self, file, table):
        super().__init__()
        self.widths = [100, 50, 200]
        self.itr = -1

        self.file = file
        self.table = table

        self.conn = sqlite3.connect(self.file)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT * FROM " + self.table)

        self.headers = [description[0] for description in self.cur.description[1::]]
        self.rowsData = self.cur.fetchall()
        self.numRows = len(self.rowsData)
        self.entries = []

        self.frame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=330,
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
        )
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.title("data")
        self.resizable(False, False)
        self.geometry(
            "600x400+"
            + str(int((self.winfo_screenwidth() - 600) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - 400) / 2)),
        )

        if len(self.headers) > 0:
            for col, header in enumerate(self.headers):
                self.label = ctk.CTkLabel(self.frame, text=header)
                self.label.grid(row=0, column=col, padx=10, pady=5)
            self.itr += 1

        if len(self.rowsData) > 0:
            for row, row_data in enumerate(self.rowsData, start=1):
                for col, value in enumerate(row_data[1::]):
                    entry = ctk.CTkEntry(self.frame, width=100)
                    entry.insert(ctk.END, value)
                    entry.grid(row=row, column=col, padx=10, pady=5)
                    self.entries.append(entry)
                self.itr += 1

        self.newRow()

        # if self.frame.grid_slaves(row=self.itr + 1, column=0)[0].get() == "":
        #     self.frame.grid_slaves(row=self.itr + 1, column=0)[0].destroy()

        saveButton = ctk.CTkButton(
            self, text="Save", corner_radius=4, command=self.save
        )
        saveButton.grid(pady=5)

    def save(self):
        flag = False
        data = []
        tupleTemp = []
        for i, entry in enumerate(self.entries):
            if i % len(self.headers) == 0 and flag:
                data.append(tuple(tupleTemp))
                tupleTemp = []
                flag = False
            if entry.get() != "":
                flag = True
                tupleTemp.append(entry.get())
            if flag and entry.get() == "":
                raise Exception("Please fill all the fields")

        self.cur.execute("""DELETE FROM """ + self.table + ";")

        for i, row in enumerate(data):
            self.cur.execute(
                """INSERT INTO """
                + self.table
                + str(tuple(self.headers))
                + """ VALUES """
                + str(row)
                + ";"
            )
        self.conn.commit()
        self.destroy()

    def newRow(self, event=None):
        # print(self.frame.grid_slaves(row=self.itr - 1, column=0)[0].get())
        # if self.frame.grid_slaves(row=self.itr - 1, column=0)[0].get() != "":
        data = []
        for i, entry in enumerate(self.entries):
            if entry.get() != "":
                data.append(entry.get())
        if len(data) > self.itr * len(self.headers):
            return
        for col, headers in enumerate(self.headers):
            entry = ctk.CTkEntry(self.frame, width=100)
            entry.grid(
                padx=10, pady=5, column=col, row=len(self.rowsData) + 1 + self.itr
            )

            if col == 0:
                entry.bind("<FocusIn>", self.newRow)
                entry.bind("<FocusOut>", self.nothing)
            self.entries.append(entry)
        self.itr += 1

    def nothing(self, event=None):
        self.bind_all("<FocusIn>", self.nothing)
        pass


# 

