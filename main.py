import customtkinter as ctk

import sqlite3


class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        # creating databases
        self.limitsConn = sqlite3.connect("limits.db")
        self.limitsCur = self.limitsConn.cursor()
        self.profilesConn = sqlite3.connect("profiles.db")
        self.profilesCur = self.profilesConn.cursor()
        self.limitsCur.execute(
            """ CREATE TABLE IF NOT EXISTS ppwt (
                                        id integer PRIMARY KEY,
                                        pp_weight REAL NOT NULL,
                                        weight REAL NOT NULL
                                    ); """
        )
        self.limitsCur.execute(
            """ CREATE TABLE IF NOT EXISTS diameter (
                                        id INTEGER PRIMARY KEY,
                                        diameter REAL NOT NULL,
                                        min_ID REAL NOT NULL,
                                        min_wall_thickness REAL NOT NULL,
                                        socket_outer_circum_BD REAL,
                                        socket_outer_circum_AD REAL,
                                        header_inner_circum REAL
                                    ); """
        )
        self.limitsCur.execute(
            """ CREATE TABLE IF NOT EXISTS moldSize (
                                        id INTEGER PRIMARY KEY,
                                        mold_size REAL NOT NULL,
                                        header_inner_circum REAL NOT NULL,
                                        body_circum REAL NOT NULL,
                                        head_diameter2 REAL NOT NULL,
                                        body_diameter3 REAL NOT NULL
                                    ); """
        )

        self.limitsCur.execute(
            """ CREATE TABLE IF NOT EXISTS moldDiameter (
                                        id INTEGER PRIMARY KEY,
                                        mold_diameter REAL NOT NULL,
                                        mold_optimal_temperature REAL NOT NULL
                                    ); """
        )
        self.limitsConn.commit()

        self.profilesCur.execute(
            """ CREATE TABLE IF NOT EXISTS rawMaterial (
                                        id INTEGER PRIMARY KEY,
                                        profile TEXT NOT NULL,
                                        density REAL NOT NULL,
                                        elastic_modulus REAL NOT NULL,
                                        shrinkage REAL NOT NULL
                                    ); """
        )
        self.profilesCur.execute(
            """ CREATE TABLE IF NOT EXISTS flatDie (
                                        id INTEGER PRIMARY KEY,
                                        profile TEXT NOT NULL,
                                        pitch REAL NOT NULL,
                                        pitch_factor REAL NOT NULL,
                                        thickness REAL NOT NULL
                                    ); """
        )
        self.profilesCur.execute(
            """ CREATE TABLE IF NOT EXISTS claddingDie (
                                        id INTEGER PRIMARY KEY,
                                        profile TEXT NOT NULL,
                                        ppd REAL NOT NULL,
                                        pp_thickness REAL NOT NULL
                                    ); """
        )
        self.profilesConn.commit()
        # app
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
            self, width=self.W * (1 - 0.884), height=self.H - 20
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

        #

        #

        #
        # self.setResize(False)
        # self.resizable(False, False)
        #

        #

    def opencalculator(self):
        from calculator import main as calcSttiff

        self.destroy()
        calculator = calcSttiff(None)
        calculator.mainloop()
        # self.destroy()

    def openData(self, file, table):
        from data import dataLib

        self.destroy()
        data = dataLib(file, table, None)
        data.mainloop()

    def closeSelf(self):
        self.destroy()


main = main()
main.mainloop()
