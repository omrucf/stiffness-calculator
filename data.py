import customtkinter as ctk
import csv
import os
import tkinter as tk


class data(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.data = []
        self.filepath = ""
        self.headers = []
        self.rowsData = []
        self.widths = [100, 50, 200]
        self.itr = -1

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

        with open("data.csv", "r", newline="", encoding="utf-8") as f:
            if os.stat("data.csv").st_size > 0:
                self.headers = f.readline().strip().split(",")
                while True:
                    row = f.readline().strip()
                    if not row:
                        break
                    self.rowsData.append(row.split(","))
            f.close()

        if len(self.headers) > 0:
            for col, header in enumerate(self.headers):
                self.label = ctk.CTkLabel(self.frame, text=header)
                self.label.grid(row=0, column=col, padx=10, pady=5)
            self.itr += 1

        if len(self.rowsData) > 0:
            for row, row_data in enumerate(self.rowsData, start=1):
                for col, value in enumerate(row_data):
                    entry = ctk.CTkEntry(self.frame, width=100)
                    entry.insert(tk.END, value)
                    entry.grid(row=row, column=col, padx=10, pady=5)
                self.itr += 1

        self.newRow()

        # if self.frame.grid_slaves(row=self.itr + 1, column=0)[0].get() == "":
        #     self.frame.grid_slaves(row=self.itr + 1, column=0)[0].destroy()

        saveButton = ctk.CTkButton(
            self, text="Save", corner_radius=4, command=self.save
        )
        saveButton.grid(pady=5)

    def save(self):
        data = []
        print(self.frame.grid_slaves(row=2, column=0)[0].get())
        print(len(self.rowsData))
        for row in range((len(self.rowsData))):
            self.rowsData[row] = []
            for col in range(len(self.headers)):
                if self.frame.grid_slaves(row=row + 1, column=col)[0].get() != "":
                    self.rowsData[row].append(
                        self.frame.grid_slaves(row=row + 1, column=col)[0].get()
                    )
                else:
                    del self.rowsData[len(self.rowsData) - 1]
                    break
        for row in range(len(self.rowsData), len(self.rowsData) + 5):
            self.rowsData.append([])
            for col in range(len(self.headers)):
                if self.frame.grid_slaves(row=row + 1, column=col)[0].get() != "":
                    self.rowsData[row].append(
                        self.frame.grid_slaves(row=row + 1, column=col)[0].get()
                    )
                else:
                    del self.rowsData[len(self.rowsData) - 1]
                    break

        with open("data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for row in self.rowsData:
                writer.writerow(row)
            f.close()
        self.destroy()

    def newRow(self, event=None):
        print(self.frame.grid_slaves(row=self.itr - 1, column=0)[0].get())
        if self.frame.grid_slaves(row=self.itr - 1, column=0)[0].get() != "":
            for col, headers in enumerate(self.headers):
                entry = ctk.CTkEntry(self.frame, width=100)
                entry.grid(
                    padx=10, pady=5, column=col, row=len(self.rowsData) + 1 + self.itr
                )
                entry.bind("<FocusIn>", self.newRow)
            self.itr += 1
