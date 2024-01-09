import customtkinter as ctk


class createSegmentedButton(ctk.CTkSegmentedButton):
    def __init__(self, master, titles, command):
        super().__init__(master)
        self.titles = titles
        self.command = command
        self.grid_columnconfigure(0, weight=1)
        self.selected = []

        self.button = ctk.CTkSegmentedButton(
            self, values=titles, command=self.command)


    def get(self):
        return self.selected
