import customtkinter as ctk
import sqlite3
from PIL import Image


class dataLib(ctk.CTk):
    def __init__(self, file, table, prev):
        if prev != None:
            prev.destroy()
        super().__init__()
        self.widths = [100, 50, 200]
        # self.itr = -1

        self.title("Stiffness calculator")
        self.W = 1300
        self.H = 800

        self.geometry(
            str(self.W)
            + "x"
            + str(self.H)
            + "+"
            + str(int((self.winfo_screenwidth() - self.W) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - self.H) / 2))
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Creaeting Frames

        self.menuBar = ctk.CTkFrame(
            self, width=self.W * (1 - 0.8515), height=self.H - 20
        )
        self.menuBar.grid_propagate(False)
        self.menuBar.grid(
            padx=10, pady=10, sticky="nw", row=0, column=0, columnspan=1, rowspan=5
        )

        # labels

        self.tablesLabel = ctk.CTkLabel(
            self.menuBar, fg_color="transparent", text="Tables"
        )
        self.tablesLabel.grid(row=0, column=0, pady=5)

        self.profilesLabel = ctk.CTkLabel(
            self.menuBar, fg_color="transparent", text="Profiles"
        )
        self.profilesLabel.grid(row=5, column=0, pady=5)

        #

        #

        # buttons

        self.ppwtTable = ctk.CTkButton(
            self.menuBar,
            text="ppwt",
            command=lambda: self.openData("limits.db", "ppwt"),
        )
        self.ppwtTable.grid(row=1, column=0, pady=5, padx=5)
        self.diameterTable = ctk.CTkButton(
            self.menuBar,
            text="Diameter",
            command=lambda: self.openData("limits.db", "diameter"),
        )
        self.diameterTable.grid(row=2, column=0, pady=5, padx=2)
        self.moldSizeTable = ctk.CTkButton(
            self.menuBar,
            text="mold size",
            command=lambda: self.openData("limits.db", "moldSize"),
        )
        self.moldSizeTable.grid(row=3, column=0, pady=5, padx=2)
        self.moldDiameterTable = ctk.CTkButton(
            self.menuBar,
            text="mold diameter",
            command=lambda: self.openData("limits.db", "moldDiameter"),
        )
        self.moldDiameterTable.grid(row=4, column=0, pady=5, padx=2)
        self.materialProfileB = ctk.CTkButton(
            self.menuBar,
            text="material",
            command=lambda: self.openData("profiles.db", "rawMaterial"),
        )

        self.materialProfileB.grid(row=6, column=0, pady=5, padx=2)
        self.flatDiaProfileB = ctk.CTkButton(
            self.menuBar,
            text="flat die",
            command=lambda: self.openData("profiles.db", "flatDie"),
        )
        self.flatDiaProfileB.grid(row=7, column=0, pady=5, padx=2)
        self.claddingDieProfileB = ctk.CTkButton(
            self.menuBar,
            text="cladding die",
            command=lambda: self.openData("profiles.db", "claddingDie"),
        )
        self.claddingDieProfileB.grid(row=8, column=0, pady=5, padx=2)

        self.calculatorB = ctk.CTkButton(
            self.menuBar,
            text="calculate stiffness",
            command=self.opencalculator,
        )
        self.calculatorB.grid(row=9, column=0, pady=5, padx=2)

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
            width=self.W * 0.8515,
            height=self.H - 50,
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
        )

        # self.frame.grid_propagate(False)
        # self.menuBar = ctk.CTkFrame(
        #     self, width=self.W * (1 - 0.8515), height=self.H - 20
        # )
        # self.menuBar.grid_propagate(False)
        # self.menuBar.grid(
        #     padx=10, pady=10, sticky="nw", row=0, column=0, columnspan=1, rowspan=5
        # )
        self.frame.grid(row=0, column=2, sticky="nw", pady=10, rowspan=5, columnspan=10)

        self.title("data")
        self.resizable(False, False)
        # self.geometry(
        #     "600x400+"
        #     + str(int((self.winfo_screenwidth() - 600) / 2))
        #     + "+"
        #     + str(int((self.winfo_screenheight() - 400) / 2)),
        # )

        if len(self.headers) > 0:
            create = ctk.CTkButton(
                self.frame,
                text="Add",
                command=lambda: self.edit(None, True),
                width=15,
                # fg_color="transparent",
            )
            create.grid(row=0, column=0, padx=10, pady=5, sticky="n")
            for col, header in enumerate(self.headers):
                self.label = ctk.CTkLabel(self.frame, text=header)
                self.label.grid(row=0, column=col + 1, padx=10, pady=5)

        editIcon = ctk.CTkImage(
            light_image=Image.open("edit.png"),
            size=(15, 15),
            dark_image=Image.open("edit.png"),
        )
        # self.itr += 1

        if len(self.rowsData) > 0:
            for row, row_data in enumerate(self.rowsData, start=1):
                edit = ctk.CTkButton(
                    self.frame,
                    text="",
                    command=lambda row=row: self.edit(row, False),
                    width=15,
                    height=15,
                    image=editIcon,
                    bg_color="transparent",
                    fg_color="transparent",
                )
                edit.grid(row=row, column=0, padx=10, pady=5)
                for col, value in enumerate(row_data[1::]):
                    entry = ctk.CTkEntry(self.frame, width=100, state="normal")
                    entry.insert(ctk.END, value)
                    entry.configure(state="disabled")
                    entry.grid(row=row, column=col + 1, padx=10, pady=5)
                    self.entries.append(entry)
                # self.itr += 1

        # if self.frame.grid_slaves(row=self.itr + 1, column=0)[0].get() == "":
        #     self.frame.grid_slaves(row=self.itr + 1, column=0)[0].destroy()

    def edit(self, row, create):
        tempFrame = ctk.CTkScrollableFrame(
            self.frame,
            width=450,
            height=300,
            fg_color="grey40",
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
        )
        tempFrame.grid(
            row=0,
            column=len(self.headers) + 2,
            columnspan=10,
            rowspan=10,
            sticky="se",
            pady=10,
        )
        save = ctk.CTkButton(
            tempFrame,
            text="Save",
            command=lambda: self.save(create, tempFrame, row),
            width=100,
        )
        save.grid(
            sticky="se",
            column=3,
            row=int(len(self.headers) / 2),
            padx=10,
            pady=5,
        )
        if create:
            for col, header in enumerate(self.headers):
                label = ctk.CTkLabel(tempFrame, text=header + ": ")
                label.grid(row=int(col / 2), column=int(col % 2) * 2, padx=10, pady=5)
                entry = ctk.CTkEntry(tempFrame, width=100)
                entry.grid(
                    row=int(col / 2), column=int(col % 2) * 2 + 1, padx=10, pady=5
                )
                self.entries.append(entry)
        else:
            row = row - 1
            for col, header in enumerate(self.headers):
                label = ctk.CTkLabel(tempFrame, text=header + ": ")
                label.grid(row=int(col / 2), column=int(col % 2) * 2, padx=10, pady=5)
                entry = ctk.CTkEntry(tempFrame, width=100)
                entry.insert(ctk.END, self.entries[row * len(self.headers) + col].get())
                entry.grid(
                    row=int(col / 2), column=int(col % 2) * 2 + 1, padx=10, pady=5
                )
                self.entries.append(entry)

    def save(self, create, tempFrame, row):
        # tempFrame.destroy()
        if create:
            for col in range(len(self.headers)):
                loc = -len(self.headers) + col
                temp = self.entries[loc].get()
                tempEntry = ctk.CTkEntry(self.frame, width=100, state="normal")
                tempEntry.insert(ctk.END, self.entries[-len(self.headers)].get())
                del self.entries[-len(self.headers)]
                self.entries.append(tempEntry)
                tempEntry.configure(state="disabled")

            editIcon = ctk.CTkImage(
                light_image=Image.open("edit.png"),
                size=(15, 15),
                dark_image=Image.open("edit.png"),
            )
            edit = ctk.CTkButton(
                self.frame,
                text="",
                command=lambda row=len(self.rowsData) + 1: self.edit(row, False),
                width=15,
                height=15,
                image=editIcon,
                bg_color="transparent",
                fg_color="transparent",
            )
            edit.grid(row=len(self.rowsData) + 1, column=0, padx=10, pady=5)

            for col, header in enumerate(self.headers):
                self.entries[-len(self.headers) + col].grid(
                    row=len(self.rowsData) + 1, column=col + 1, padx=10, pady=5
                )
        else:
            for col in range(len(self.headers)):
                self.entries[row * len(self.headers) + col].configure(state="normal")
                self.entries[row * len(self.headers) + col].delete(0, ctk.END)
                self.entries[row * len(self.headers) + col].insert(
                    0, self.entries[-len(self.headers) + col].get()
                )
                del self.entries[-len(self.headers) + col]

            for col in range(len(self.headers)):
                self.entries[row * len(self.headers) + col].grid(
                    row=row + 1, column=col + 1, padx=10, pady=5
                )
                if self.entries[row * len(self.headers) + col].get() == "":
                    try:
                        self.entries[row * len(self.headers) + col].grid_forget()
                        self.frame.grid_slaves(row=row + 1, column=0)[0].grid_forget()
                    except:
                        pass

        flag = False
        data = []
        tupleTemp = []
        for i, entry in enumerate(self.entries):
            if i % (len(self.headers)) == 0 and flag:
                data.append(tuple(tupleTemp))
                tupleTemp = []
                flag = False
            if entry.get().replace(" ", "") != "":
                flag = True
                tupleTemp.append(entry.get())
                print(tupleTemp)
            if flag and entry.get() == "":
                raise Exception("Please fill all the fields")
            if i == len(self.entries) - 1 and tupleTemp != []:
                data.append(tuple(tupleTemp))

        self.cur.execute("""DELETE FROM """ + self.table + ";")
        print(data)
        for i, row in enumerate(data):
            print(row)
            self.cur.execute(
                """INSERT INTO """
                + self.table
                + str(tuple(self.headers))
                + """ VALUES """
                + str(row)
                + ";"
            )
        self.conn.commit()
        tempFrame.destroy()
        tempFrame.grid_forget()
        # self.destroy()

    def opencalculator(self):
        from calculator import main as calcSttiff

        self.destroy()

        calculator = calcSttiff(None)
        calculator.mainloop()
        # self.destroy()

    def openData(self, file, table):
        self.destroy()
        data = dataLib(file, table, None)
        data.mainloop()


data = dataLib("limits.db", "ppwt", None)
data.mainloop()
