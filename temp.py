# import sqlite3

# conn = sqlite3.connect("data.db")
# cur = conn.cursor()

# # cur.execute(
# #     """CREATE TABLE IF NOT EXISTS diameter (
# #                 id INTEGER PRIMARY KEY,
# #                 pipe_diameter REAL NOT NULL,
# #                 min_wall_thickness REAL NOT NULL,
# #                 mold_diameter REAL NOT NULL,
# #                 mold_optimal_temperature REAL);"""
# # )

# # cur.execute(
# #     """CREATE TABLE IF NOT EXISTS ppwt (
# #                                         id integer PRIMARY KEY,
# #                                         pp_diameter REAL NOT NULL,
# #                                         weight REAL NOT NULL
# #                                     );"""
# # )


# # ppwt = {27:[90],
# # 29:[100],
# # 30:[108],
# # 34:[130],
# # 36:[135],
# # 42:[170],
# # 45:[195],
# # 54:[230],
# # 56:[260],
# # 60:[310],
# # 65:[380],
# # 70:[390],
# # 75:[400],
# # 80:[440],
# # 85:[500],
# # 90:[620],
# # 100:[650],
# # 105:[715],
# # 110:[840],
# # 120:[960]}

# # for p in ppwt:
# #     for w in ppwt[p]:
# #         cur.execute('INSERT INTO ppwt (pp_diameter, weight) VALUES (?, ?)', (p, w))


# # moldDiameter = {
# #     800: [150],
# #     900: [150],
# #     1000: [150],
# #     1200: [160],
# #     1400: [160],
# #     2000: [170],
# # }

# # for m in moldDiameter:
# #     for d in moldDiameter[m]:
# #         cur.execute(
# #             "INSERT INTO moldDiameter (mold_diameter, mold_optimal_temperature) VALUES (?, ?)",
# #             (m, d),
# #         )


# # pipe_diameter	mold_diameter	min_wall_thickness	mold_optimal_temprature
# # diameter = [(600,611.15,3.5, None),
# # (700, 710.47, 4, None),
# # (800, 813.60, 4.5, 150),
# # (1000, 1015.41, 5, 150),
# # (1200, 1218.49, 5, 160),
# # (1600, 1625.93, 5.5, None),
# # (2000, 2027.63, 6, 170)]

# # for d in diameter:
# #     cur.execute(
# #         "INSERT INTO diameter (pipe_diameter, mold_diameter, min_wall_thickness, mold_optimal_temperature) VALUES (?, ?, ?, ?)",
# #         d,
# # )


# cur.execute("""ALTER TABLE claddingDie
# RENAME COLUMN ppd TO pp_diameter;""")
# conn.commit()
# temp = cur.fetchall()
# # all = []
# # for tup in temp:
# #     all.append((tup[1], tup[3]))
# print(temp)


import customtkinter
import os
from PIL import Image


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [
            checkbox.cget("text")
            for checkbox in self.checkbox_list
            if checkbox.get() == 1
        ]


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(
            self, text=item, value=item, variable=self.radiobutton_variable
        )
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = customtkinter.CTkLabel(
            self, text=item, image=image, compound="left", padx=5, anchor="w"
        )
        button = customtkinter.CTkButton(self, text="Command", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTkScrollableFrame example")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(
            master=self,
            width=200,
            command=self.checkbox_frame_event,
            item_list=[f"item {i}" for i in range(50)],
        )
        self.scrollable_checkbox_frame.grid(
            row=0, column=0, padx=15, pady=15, sticky="ns"
        )
        self.scrollable_checkbox_frame.add_item("new item")

        # create scrollable radiobutton frame
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(
            master=self,
            width=500,
            command=self.radiobutton_frame_event,
            item_list=[f"item {i}" for i in range(100)],
            label_text="ScrollableRadiobuttonFrame",
        )
        self.scrollable_radiobutton_frame.grid(
            row=0, column=1, padx=15, pady=15, sticky="ns"
        )
        self.scrollable_radiobutton_frame.configure(width=200)
        self.scrollable_radiobutton_frame.remove_item("item 3")

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            master=self,
            width=300,
            command=self.label_button_frame_event,
            corner_radius=0,
        )
        self.scrollable_label_button_frame.grid(
            row=0, column=2, padx=0, pady=0, sticky="nsew"
        )

    def checkbox_frame_event(self):
        print(
            f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}"
        )

    def radiobutton_frame_event(self):
        print(
            f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}"
        )

    def label_button_frame_event(self, item):
        print(f"label button frame clicked: {item}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
