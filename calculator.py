import math
import customtkinter as ctk
from data import data as dataLib
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

        self.modeNames = ["Select Mode", "PR", "OP", "VW", "SQ"]
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
        self.elastic_modulus = -1
        self.density = -1
        self.shrinkage = -1

        self.pipe_length = -1
        self.pd = -1
        self.p = -1
        self.s1 = -1  # wall_thickness
        self.ppd = -1
        self.s4 = -1  # pp_thickness

        # Creaeting Frames

        self.rawMaterialFrame = ctk.CTkFrame(
            self, width=(self.W * 0.94444), height=(self.H / 11)
        )
        self.rawMaterialFrame.grid_propagate(False)
        self.rawMaterialFrame.grid(
            padx=5, pady=10, sticky="n", row=0, column=1, columnspan=2
        )

        self.productionFrame = ctk.CTkFrame(
            self, width=(self.W * 0.94444), height=(self.H / 4) + 15
        )
        self.productionFrame.grid_propagate(False)
        self.productionFrame.grid(
            padx=5, pady=10, sticky="n", row=1, column=1, columnspan=2
        )

        self.machineLimitsFrame = ctk.CTkFrame(
            self, width=(self.W * 0.94444), height=(self.H / 4) + 30
        )
        self.machineLimitsFrame.grid_propagate(False)
        self.machineLimitsFrame.grid(
            padx=5, pady=10, sticky="n", row=2, column=1, columnspan=2, rowspan=2
        )
        self.machineLimitsFrame.grid_propagate(False)
        self.resultsFrame = ctk.CTkFrame(
            self, width=(self.W * 0.94444), height=(self.H / 4)
        )
        self.resultsFrame.grid_propagate(False)
        self.resultsFrame.grid(
            padx=5, pady=10, sticky="n", row=4, column=1, columnspan=2, rowspan=2
        )
        self.menuBar = ctk.CTkFrame(self, width=260, height=self.H - 20)
        self.menuBar.grid_propagate(False)
        self.menuBar.grid(
            padx=10, pady=10, sticky="nw", row=0, column=0, columnspan=1, rowspan=5
        )

        self.modeFrame = ctk.CTkFrame(
            self.menuBar, width=self.W * (1 - 0.72222), height=(self.H / 20)
        )
        self.modeFrame.grid(padx=5, pady=10, sticky="nw", row=0, column=0)

        #

        #

        #

        self.modes = ctk.CTkOptionMenu(
            self.modeFrame,
            values=self.modeNames,
            command=self.modeCommand,
            corner_radius=0,
        )
        self.modes.grid()

        items = self.profilesCur.execute("SELECT profile FROM rawMaterial").fetchall()
        items = [item[0] for item in items]
        self.materialprofile = ctk.CTkOptionMenu(
            self.rawMaterialFrame,
            values=["Material profiles"] + list(items) + ["New profile"],
            anchor="w",
            command=self.materialCommand,
            corner_radius=0,
            dynamic_resizing=False,
        )

        items = self.profilesCur.execute("SELECT profile FROM flatDie").fetchall()
        items = [item[0] for item in items]

        self.flatDieProfile = ctk.CTkOptionMenu(
            self.productionFrame,
            values=["Flat die profiles"] + list(items) + ["New profile"],
            command=self.dieCommand,
            anchor="w",
            corner_radius=0,
            dynamic_resizing=False,
        )

        items = self.profilesCur.execute("SELECT profile FROM claddingDie").fetchall()
        items = [item[0] for item in items]

        self.claddingDieProfile = ctk.CTkOptionMenu(
            self.productionFrame,
            values=list(items) + ["New profile"],
            command=self.claddingCommand,
            anchor="w",
            corner_radius=0,
            dynamic_resizing=False,
            width=165,
        )
        self.claddingDieProfile.set("Cladding die profiles")

        #

        #

        #

        #

        #

        # raw material
        self.rawMaterialError = ctk.CTkLabel(
            self.rawMaterialFrame, text="", text_color="red"
        )
        self.rawMaterialError.grid(
            row=0, column=1, padx=10, pady=5, columnspan=3, sticky="w"
        )
        self.rawMaterilaLabel = ctk.CTkLabel(
            self.rawMaterialFrame,
            text="Raw Material:",
            fg_color="transparent",
            anchor="w",
            width=10,
        )

        self.rawMaterilaLabel.grid(
            row=0, column=0, padx=5, pady=2, columnspan=2, sticky="w"
        )

        self.materialNameLabel = ctk.CTkLabel(
            self.rawMaterialFrame,
            text="Profile Name",
            fg_color="transparent",
            anchor="w",
            width=10,
        )
        self.materialNameEntry = ctk.CTkEntry(
            self.rawMaterialFrame, placeholder_text="", width=100
        )

        self.densityLabel = ctk.CTkLabel(
            self.rawMaterialFrame,
            text="Density",
            fg_color="transparent",
            anchor="w",
            width=10,
        )
        self.densityLabel.grid_forget()
        self.densityEntry = ctk.CTkEntry(
            self.rawMaterialFrame, placeholder_text="", width=50, state="disabled"
        )
        self.densityUnitLabel = ctk.CTkLabel(
            self.rawMaterialFrame,
            text="(g/cm3)",
            fg_color="transparent",
        )
        self.densityEntry.grid_forget()

        self.elasticLabel = ctk.CTkLabel(
            self.rawMaterialFrame, fg_color="transparent", text="Elastic Modulus"
        )
        self.elasticLabel.grid_forget()
        self.elasticEntry = ctk.CTkEntry(
            self.rawMaterialFrame, placeholder_text="", width=50, state="disabled"
        )
        self.elasticUnitLabel = ctk.CTkLabel(
            self.rawMaterialFrame, fg_color="transparent", text="(Mpa)"
        )
        self.elasticEntry.grid_forget()

        self.shrinkageLabel = ctk.CTkLabel(
            self.rawMaterialFrame, fg_color="transparent", text="Shrinkage Rate"
        )
        self.shrinkageLabel.grid_forget()
        self.shrinkageUnitLabel = ctk.CTkLabel(
            self.rawMaterialFrame, fg_color="transparent", text="(%)"
        )
        self.shrinkageEntry = ctk.CTkEntry(
            self.rawMaterialFrame, placeholder_text="", width=50, state="disabled"
        )
        self.shrinkageEntry.grid_forget()

        #

        #

        #

        #

        #

        # production
        self.productionError = ctk.CTkLabel(
            self.productionFrame, text="", text_color="red"
        )
        self.productionError.grid(
            row=0, column=1, padx=10, pady=5, columnspan=3, sticky="w"
        )
        self.productionName = ctk.CTkLabel(
            self.productionFrame,
            fg_color="transparent",
            text="Production:",
        )
        self.productionName.grid(
            row=0, column=0, padx=5, pady=5, columnspan=2, sticky="w"
        )

        self.dieNameLabel = ctk.CTkLabel(
            self.productionFrame,
            text="Profile Name",
            fg_color="transparent",
            anchor="w",
            width=10,
        )
        self.dieNameEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=150
        )

        self.claddingNameLabel = ctk.CTkLabel(
            self.productionFrame,
            text="Profile Name",
            fg_color="transparent",
            anchor="w",
            width=10,
        )
        self.claddingNameEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=150
        )

        self.pipeLengthLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Pipe Length"
        )
        self.pipeLengthLabel.grid_forget()
        self.pipeLengthUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.pipeLengthEnry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70
        )
        self.pipeLengthEnry.grid_forget()

        self.pipeDiameterLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Pipe Diameter"
        )
        self.pipeDiameterLabel.grid_forget()
        self.pipeDiameterUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.pipeDiameterEnry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70
        )
        self.pipeDiameterEnry.grid_forget()

        self.pitchLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Flat die"
        )
        self.pitchUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.pitchUnitLabel.grid_forget()
        self.pitchEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70, state="disabled"
        )
        self.pitchEntry.grid_forget()

        self.pitchEntry.bind("<FocusOut>", command=self.calcPitch)

        self.pitchFactorLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Flat Die Factor"
        )
        self.pitchFactorUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.pitchFactorUnitLabel.grid_forget()
        self.pitchFactorEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70, state="disabled"
        )
        self.pitchFactorEntry.grid_forget()

        self.pitchFactorEntry.bind("<FocusOut>", command=self.calcPitch)

        self.finalPitchLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Pitch"
        )
        self.finalPitchUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.finalPitchUnitLabel.grid_forget()
        self.finalPitchEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70, state="disabled"
        )
        self.finalPitchEntry.grid_forget()

        self.WallThicknessLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="Wall Thickness"
        )
        self.WallThicknessLabel.grid_forget()
        self.WallThicknessUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.WallThicknessEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70, state="disabled"
        )
        self.WallThicknessEntry.grid_forget()

        self.PPDiameterLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="PP Diameter"
        )
        self.PPDiameterLabel.grid_forget()
        self.PPDiameterUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.PPDiameterEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70
        )
        self.PPDiameterEntry.grid_forget()

        self.PPFilmThicknessLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="PP Film Thickness"
        )
        self.PPFilmThicknessLabel.grid_forget()
        self.PPFilmThicknessUnitLabel = ctk.CTkLabel(
            self.productionFrame, fg_color="transparent", text="(mm)"
        )
        self.PPFilmThicknessEntry = ctk.CTkEntry(
            self.productionFrame, placeholder_text="", width=70
        )
        self.PPFilmThicknessEntry.grid_forget()

        #

        #

        #

        #

        #

        # machine limits
        self.machineLimitsError = ctk.CTkLabel(
            self.machineLimitsFrame, text="", text_color="red"
        )
        self.machineLimitsError.grid(
            row=1, column=0, padx=10, pady=5, sticky="nw", rowspan=2
        )
        self.machineLimitsFrame.grid_rowconfigure(0, weight=1)
        # self.machineLimitsFrame.grid_columnconfigure(0, weight=1)

        self.machineName = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Machine: "
        )
        self.machineName.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        self.MouthEndLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Mouth End"
        )
        self.MouthEndUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )
        self.MouthEndLabel.grid_forget()
        self.MouthEndEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.MouthEndEntry.grid_forget()

        self.MouthStartLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Mouth Start"
        )
        self.MouthStartUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )

        self.MouthStartLabel.grid_forget()
        self.MouthStartEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.MouthStartEntry.grid_forget()

        self.CarriageReturnPositionLabel = ctk.CTkLabel(
            self.machineLimitsFrame,
            fg_color="transparent",
            text="Carriage Return Position",
        )
        self.CarriageReturnPositionUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame,
            fg_color="transparent",
            text="(mm)",
        )
        self.CarriageReturnPositionLabel.grid_forget()
        self.CarriageReturnPositionEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.CarriageReturnPositionEntry.grid_forget()

        self.CarriageReturnDelayLabel = ctk.CTkLabel(
            self.machineLimitsFrame,
            fg_color="transparent",
            text="Carriage Return Delay",
        )
        self.CarriageReturnDelayUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame,
            fg_color="transparent",
            text="(mm)",
        )
        self.CarriageReturnDelayLabel.grid_forget()
        self.CarriageReturnDelayEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.CarriageReturnDelayEntry.grid_forget()

        self.PPStartLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="PP Start"
        )
        self.PPStartUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )
        self.PPStartLabel.grid_forget()
        self.PPStartEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.PPStartEntry.grid_forget()

        self.PPEndLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="PP End"
        )
        self.PPEndUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )
        self.PPEndLabel.grid_forget()
        self.PPEndEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.PPEndEntry.grid_forget()

        self.SocketStartLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Socket Start"
        )
        self.SocketStartUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )
        self.SocketStartLabel.grid_forget()
        self.SocketStartEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.SocketStartEntry.grid_forget()

        self.SocketEndLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Socket End"
        )
        self.SocketEndUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm)"
        )
        self.SocketEndLabel.grid_forget()
        self.SocketEndEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.SocketEndEntry.grid_forget()

        self.MoldSpeedLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Mold Speed"
        )
        self.MoldSpeedUnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(mm/min)"
        )
        self.MoldSpeedLabel.grid_forget()

        self.MoldSpeedEntry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.MoldSpeedEntry.grid_forget()

        self.FlatExtruder75Label = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Flat Extruder 75"
        )
        self.FlatExtruder75UnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(kg/hr)"
        )
        self.FlatExtruder75Label.grid_forget()
        self.FlatExtruder75Entry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.FlatExtruder75Entry.grid_forget()

        self.CladdingExtruder75Label = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="Cladding Extruder 75"
        )
        self.CladdingExtruder75UnitLabel = ctk.CTkLabel(
            self.machineLimitsFrame, fg_color="transparent", text="(kg/hr)"
        )
        self.CladdingExtruder75Label.grid_forget()
        self.CladdingExtruder75Entry = ctk.CTkEntry(
            self.machineLimitsFrame, placeholder_text="", width=70
        )
        self.CladdingExtruder75Entry.grid_forget()

        #

        #

        #

        #

        #

        # Results
        self.SnLabel = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="Sn:      ", anchor="w"
        )
        self.SnLabel.grid_forget()

        self.W1Label = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W1:      ", anchor="w"
        )
        self.W1Label.grid_forget()

        self.W2Label = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W2:      ", anchor="w"
        )
        self.W2Label.grid_forget()

        self.W3Label = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W3:      ", anchor="w"
        )
        self.W3Label.grid_forget()

        self.W4Label = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W4:      ", anchor="w"
        )
        self.W4Label.grid_forget()

        self.WLabel = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W:      ", anchor="w"
        )
        self.WLabel.grid_forget()

        self.WkLabel = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="Wk:      ", anchor="w"
        )
        self.WkLabel.grid_forget()

        self.WpLabel = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="Wp:      ", anchor="w"
        )
        self.WpLabel.grid_forget()

        self.WzLabel = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="Wz:      ", anchor="w"
        )
        self.WzLabel.grid_forget()

        self.W0Label = ctk.CTkLabel(
            self.resultsFrame, fg_color="transparent", text="W0:      ", anchor="w"
        )
        self.W0Label.grid_forget()

        #

        #

        # labels

        self.tablesLabel = ctk.CTkLabel(
            self.menuBar, fg_color="transparent", text="Tables"
        )
        self.tablesLabel.grid(row=1, column=0, pady=5)

        self.profilesLabel = ctk.CTkLabel(
            self.menuBar, fg_color="transparent", text="Profiles"
        )
        self.profilesLabel.grid(row=6, column=0, pady=5)

        #

        #

        # buttons

        self.ppwtTable = ctk.CTkButton(
            self.menuBar,
            text="ppwt",
            command=lambda: self.openData("limits.db", "ppwt"),
        )
        self.ppwtTable.grid(row=2, column=0, pady=5)
        self.diameterTable = ctk.CTkButton(
            self.menuBar,
            text="Diameter",
            command=lambda: self.openData("limits.db", "diameter"),
        )
        self.diameterTable.grid(row=3, column=0, pady=5)
        self.moldSizeTable = ctk.CTkButton(
            self.menuBar,
            text="mold size",
            command=lambda: self.openData("limits.db", "moldSize"),
        )
        self.moldSizeTable.grid(row=4, column=0, pady=5)
        self.moldDiameterTable = ctk.CTkButton(
            self.menuBar,
            text="mold diameter",
            command=lambda: self.openData("limits.db", "moldDiameter"),
        )
        self.moldDiameterTable.grid(row=5, column=0, pady=5)
        self.materialProfileB = ctk.CTkButton(
            self.menuBar,
            text="material",
            command=lambda: self.openData("profiles.db", "rawMaterial"),
        )

        self.materialProfileB.grid(row=7, column=0, pady=5)
        self.flatDiaProfileB = ctk.CTkButton(
            self.menuBar,
            text="flat die",
            command=lambda: self.openData("profiles.db", "flatDie"),
        )
        self.flatDiaProfileB.grid(row=8, column=0, pady=5)
        self.claddingDieProfileB = ctk.CTkButton(
            self.menuBar,
            text="cladding die",
            command=lambda: self.openData("profiles.db", "claddingDie"),
        )
        self.claddingDieProfileB.grid(row=9, column=0, pady=5)

        self.saveMaterialB = ctk.CTkButton(
            self.rawMaterialFrame, text="Save", command=self.saveMaterial, width=100
        )

        self.saveDieB = ctk.CTkButton(
            self.productionFrame, text="Save", command=self.saveDie, width=100
        )
        self.saveCladdingB = ctk.CTkButton(
            self.productionFrame, text="Save", command=self.saveCladding, width=100
        )

        self.calculateButton = ctk.CTkButton(
            self.menuBar, text="calculate", command=self.calculatePR
        )
        self.menuBar.grid_rowconfigure(20, weight=1)
        self.calculateButton.grid(row=20, column=0, pady=5, sticky="s")

        #

        #

        #
        # self.setResize(False)
        self.resizable(False, False)
        #

        #

    def calcPitch(self, event):
        print("calcPitch: " + str(event))
        if self.pitchEntry.get() != "" and self.pitchFactorEntry.get() != "":
            self.finalPitchEntry.configure(state="normal")
            self.finalPitchEntry.delete(0, ctk.END)
            self.finalPitchEntry.insert(
                0,
                str(
                    round(
                        float(self.pitchEntry.get())
                        - float(self.pitchFactorEntry.get()),
                        2,
                    )
                ),
            )
            self.finalPitchEntry.configure(state="disabled")

    def Error(self, entryType, errorType, number):
        error = ctk.CTkInputDialog(
            text=(str(entryType) + " must be " + str(errorType) + ": " + str(number)),
            title="Error",
        )
        error.geometry(
            "350x200"
            + "+"
            + str(int((self.winfo_screenwidth() - 350) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - 200) / 2))
        )

        flag = False

        inputNumber = error.get_input()

        if errorType.lower() == "at least":
            if float(inputNumber) >= float(number):
                flag = True
        elif errorType.lower() == "at most":
            if float(inputNumber) <= float(number):
                flag = True
        elif errorType.lower() == "equal to":
            if float(inputNumber) == float(number):
                flag = True
        elif errorType.lower() == "not equal to":
            if float(inputNumber) != float(number):
                flag = True
        else:
            error.destroy()
            return

        if flag:
            return inputNumber

        error.destroy()
        input = self.Error(entryType, errorType, number)
        return input

    def Error(self, Frame, entryName, entryType, errorType, number):
        flag = False
        if Frame == self.rawMaterialFrame:
            self.rawMaterialError.configure(
                text=(
                    str(entryType) + " must be " + str(errorType) + ": " + str(number)
                )
            )
        elif Frame == self.productionFrame:
            self.productionError.configure(
                text=(
                    str(entryType) + " must be " + str(errorType) + ": " + str(number)
                )
            )
        elif Frame == self.machineLimitsFrame:
            self.machineLimitsError.configure(
                text=(
                    str(entryType) + " must be " + str(errorType) + ": " + str(number)
                )
            )

        inputNumber = entryName.get()

        if errorType.lower() == "at least":
            if float(inputNumber) >= float(number):
                flag = True
        elif errorType.lower() == "at most":
            if float(inputNumber) <= float(number):
                flag = True
        elif errorType.lower() == "equal to":
            if float(inputNumber) == float(number):
                flag = True
        elif errorType.lower() == "not equal to":
            if float(inputNumber) != float(number):
                flag = True
        else:
            return

        if flag:
            if Frame == self.rawMaterialFrame:
                self.rawMaterialError.configure(text="")
            elif Frame == self.productionFrame:
                self.productionError.configure(text="")
            elif Frame == self.machineLimitsFrame:
                self.machineLimitsError.configure(text="")

    def openData(self, file, table):
        data = dataLib(file, table)
        data.mainloop()

        #

        #

        #

        #

        #

    def materialCommand(self, material):
        if material != "select profile":
            items = self.profilesCur.execute(
                "SELECT profile FROM rawMaterial"
            ).fetchall()
            items = [item[0] for item in items]
            self.materialprofile.configure(values=list(items) + ["New profile"])

        if material != "New profile" and material != "select profile":
            self.saveMaterialB.grid_forget()
            self.materialNameLabel.grid_forget()
            self.materialNameEntry.grid_forget()

            self.densityEntry.configure(state="normal")
            self.elasticEntry.configure(state="normal")
            self.shrinkageEntry.configure(state="normal")

            self.elasticEntry.delete(0, ctk.END)
            self.densityEntry.delete(0, ctk.END)
            self.shrinkageEntry.delete(0, ctk.END)
            self.elasticEntry.insert(
                0,
                str(
                    self.profilesCur.execute(
                        "SELECT elastic_modulus FROM rawMaterial WHERE profile=?",
                        (material,),
                    ).fetchone()[0]
                ),
            )
            self.densityEntry.insert(
                0,
                str(
                    self.profilesCur.execute(
                        "SELECT density FROM rawMaterial WHERE profile=?", (material,)
                    ).fetchone()[0]
                ),
            )
            self.shrinkageEntry.insert(
                0,
                str(
                    self.profilesCur.execute(
                        "SELECT shrinkage FROM rawMaterial WHERE profile=?", (material,)
                    ).fetchone()[0]
                ),
            )
            self.densityEntry.configure(state="disabled")
            self.elasticEntry.configure(state="disabled")
            self.shrinkageEntry.configure(state="disabled")
        elif material == "New profile":
            self.densityEntry.configure(state="normal")
            self.elasticEntry.configure(state="normal")
            self.shrinkageEntry.configure(state="normal")
            self.materialNameLabel.grid(row=0, column=17, padx=5, pady=5, columnspan=2)
            self.materialNameEntry.grid(
                row=0, column=19, padx=5, pady=5, sticky="w", columnspan=2
            )
            self.saveMaterialB.grid(
                row=0, column=21, padx=5, pady=5, sticky="w", columnspan=2
            )

    def dieCommand(self, die):
        if die != "select profile":
            items = self.profilesCur.execute("SELECT profile FROM flatDie").fetchall()
            items = [item[0] for item in items]
            self.flatDieProfile.configure(values=list(items) + ["New profile"])
        if die != "New profile" and die != "select profile":
            self.saveDieB.grid_forget()
            self.dieNameLabel.grid_forget()
            self.dieNameEntry.grid_forget()
            self.pitchEntry.configure(state="normal")
            self.pitchFactorEntry.configure(state="normal")
            self.WallThicknessEntry.configure(state="normal")
            flatdie = self.profilesCur.execute(
                "SELECT pitch FROM flatDie WHERE profile=?", (die,)
            ).fetchone()[0]
            factor = self.profilesCur.execute(
                "SELECT pitch_factor FROM flatDie WHERE profile=?", (die,)
            ).fetchone()[0]
            thickness = self.profilesCur.execute(
                "SELECT thickness FROM flatDie WHERE profile=?", (die,)
            ).fetchone()[0]
            self.pitchEntry.delete(0, ctk.END)
            self.pitchFactorEntry.delete(0, ctk.END)
            self.WallThicknessEntry.delete(0, ctk.END)
            self.WallThicknessEntry.insert(
                0,
                str(thickness),
            )
            self.pitchEntry.insert(
                0,
                str(flatdie),
            )
            self.pitchFactorEntry.insert(
                0,
                str(factor),
            )
            self.calcPitch("")
            self.pitchEntry.configure(state="disabled")
            self.pitchFactorEntry.configure(state="disabled")
            self.WallThicknessEntry.configure(state="disabled")

        elif die == "New profile":
            self.pitchEntry.configure(state="normal")
            self.pitchFactorEntry.configure(state="normal")
            self.WallThicknessEntry.configure(state="normal")
            self.dieNameLabel.grid(
                row=0, column=17, padx=5, pady=5, sticky="w", columnspan=2
            )
            self.dieNameEntry.grid(
                row=0, column=19, padx=5, pady=6, sticky="w", columnspan=2
            )
            self.saveDieB.grid(
                row=0, column=21, padx=5, pady=5, sticky="w", columnspan=2
            )

        # create same function as dieCommand but use ppd and ppfilmthickness entries

    def claddingCommand(self, die):
        if die != "select profile":
            items = self.profilesCur.execute(
                "SELECT profile FROM claddingDie"
            ).fetchall()
            items = [item[0] for item in items]
            self.claddingDieProfile.configure(values=list(items) + ["New profile"])
        if die != "New profile" and die != "select profile":
            self.saveCladdingB.grid_forget()
            self.claddingNameLabel.grid_forget()
            self.claddingNameEntry.grid_forget()
            self.PPDiameterEntry.configure(state="normal")
            self.PPFilmThicknessEntry.configure(state="normal")
            ppd = self.profilesCur.execute(
                "SELECT ppd FROM claddingDie WHERE profile=?", (die,)
            ).fetchone()[0]
            ppfilmthickness = self.profilesCur.execute(
                "SELECT pp_thickness FROM claddingDie WHERE profile=?", (die,)
            ).fetchone()[0]
            self.PPDiameterEntry.delete(0, ctk.END)
            self.PPFilmThicknessEntry.delete(0, ctk.END)
            self.PPDiameterEntry.insert(
                0,
                str(ppd),
            )
            self.PPFilmThicknessEntry.insert(
                0,
                str(ppfilmthickness),
            )
            self.PPDiameterEntry.configure(state="disabled")
            self.PPFilmThicknessEntry.configure(state="disabled")

        elif die == "New profile":
            self.PPDiameterEntry.configure(state="normal")
            self.PPFilmThicknessEntry.configure(state="normal")
            self.claddingNameLabel.grid(
                row=1, column=17, padx=5, pady=5, sticky="w", columnspan=2
            )
            self.claddingNameEntry.grid(
                row=1, column=19, padx=5, pady=6, sticky="w", columnspan=2
            )
            self.saveCladdingB.grid(
                row=1, column=21, padx=5, pady=5, sticky="w", columnspan=2
            )

    def saveMaterial(self):
        try:
            if self.materialNameEntry.get() == "":
                raise Exception("please enter profile name")
            if self.elasticEntry.get() == "":
                raise Exception("please enter elastic modulus")
            if self.densityEntry.get() == "":
                raise Exception("please enter density")
            if self.shrinkageEntry.get() == "":
                raise Exception("please enter shrinkage rate")
            self.profilesCur.execute(
                "INSERT INTO rawMaterial (profile, elastic_modulus, density, shrinkage) VALUES (?, ?, ?, ?)",
                (
                    self.materialNameEntry.get(),
                    self.elasticEntry.get(),
                    self.densityEntry.get(),
                    self.shrinkageEntry.get(),
                ),
            )
            self.profilesConn.commit()
            items = self.profilesCur.execute(
                "SELECT profile FROM rawMaterial"
            ).fetchall()
            items = [item[0] for item in items]
            self.materialprofile.configure(values=list(items) + ["New profile"])
            self.materialprofile.set(self.materialNameEntry.get())
            self.materialNameEntry.delete(0, ctk.END)
            self.materialNameLabel.grid_forget()
            self.materialNameEntry.grid_forget()
            self.saveMaterialB.grid_forget()
        except Exception as e:
            print("error: " + str(e))

    def saveDie(self):
        try:
            if self.dieNameEntry.get() == "":
                raise Exception("please enter profile name")
            if self.pitchEntry.get() == "":
                raise Exception("please enter flat die")
            if self.pitchFactorEntry.get() == "":
                raise Exception("please enter flat die factor")
            if self.WallThicknessEntry.get() == "":
                raise Exception("please enter wall thickness")
            self.profilesCur.execute(
                "INSERT INTO flatDie (profile, pitch, pitch_factor, thickness) VALUES (?, ?, ?, ?)",
                (
                    self.dieNameEntry.get(),
                    self.pitchEntry.get(),
                    self.pitchFactorEntry.get(),
                    float(self.WallThicknessEntry.get()),
                ),
            )
            self.profilesConn.commit()
            items = self.profilesCur.execute("SELECT profile FROM flatDie").fetchall()
            items = [item[0] for item in items]
            self.flatDieProfile.configure(values=list(items) + ["New profile"])
            self.flatDieProfile.set(self.dieNameEntry.get())
            self.dieNameEntry.delete(0, ctk.END)
            self.dieNameLabel.grid_forget()
            self.dieNameEntry.grid_forget()
            self.saveDieB.grid_forget()
            self.dieCommand(self.dieNameEntry.get())
        except Exception as e:
            print("error: " + str(e))

    def saveCladding(self):
        try:
            if self.claddingNameEntry.get() == "":
                raise Exception("please enter profile name")
            if self.PPDiameterEntry.get() == "":
                raise Exception("please enter pp diameter")
            if self.PPFilmThicknessEntry.get() == "":
                raise Exception("please enter pp film thickness")
            self.profilesCur.execute(
                "INSERT INTO claddingDie (profile, ppd, pp_thickness) VALUES (?, ?, ?)",
                (
                    self.claddingNameEntry.get(),
                    self.PPDiameterEntry.get(),
                    self.PPFilmThicknessEntry.get(),
                ),
            )
            self.profilesConn.commit()
            items = self.profilesCur.execute(
                "SELECT profile FROM claddingDie"
            ).fetchall()
            items = [item[0] for item in items]
            self.claddingDieProfile.configure(values=list(items) + ["New profile"])
            self.claddingDieProfile.set(self.claddingNameEntry.get())
            self.claddingNameEntry.delete(0, ctk.END)
            self.claddingNameLabel.grid_forget()
            self.claddingNameEntry.grid_forget()
            self.saveCladdingB.grid_forget()
            self.claddingCommand(self.claddingNameEntry.get())
        except Exception as e:
            print("error: " + str(e))

    def modeCommand(self, mode):
        if mode == "PR":
            self.PR()
        else:  # hide widgets related to PR
            self.materialprofile.grid_forget()
            self.densityLabel.grid_forget()
            self.densityEntry.grid_forget()
            self.densityUnitLabel.grid_forget()
            self.elasticLabel.grid_forget()
            self.elasticEntry.grid_forget()
            self.elasticUnitLabel.grid_forget()
            self.shrinkageLabel.grid_forget()
            self.shrinkageEntry.grid_forget()
            self.shrinkageUnitLabel.grid_forget()

            self.flatDieProfile.grid_forget()
            self.claddingDieProfile.grid_forget()
            self.pipeLengthLabel.grid_forget()
            self.pipeLengthUnitLabel.grid_forget()
            self.pipeLengthEnry.grid_forget()
            self.pipeDiameterLabel.grid_forget()
            self.pipeDiameterUnitLabel.grid_forget()
            self.pipeDiameterEnry.grid_forget()
            self.pitchLabel.grid_forget()
            self.pitchEntry.grid_forget()
            self.pitchUnitLabel.grid_forget()
            self.pitchFactorLabel.grid_forget()
            self.pitchFactorEntry.grid_forget()
            self.pitchFactorUnitLabel.grid_forget()
            self.WallThicknessLabel.grid_forget()
            self.WallThicknessEntry.grid_forget()
            self.WallThicknessUnitLabel.grid_forget()
            self.finalPitchLabel.grid_forget()
            self.finalPitchEntry.grid_forget()
            self.finalPitchUnitLabel.grid_forget()
            self.PPDiameterLabel.grid_forget()
            self.PPDiameterEntry.grid_forget()
            self.PPDiameterUnitLabel.grid_forget()
            self.PPFilmThicknessLabel.grid_forget()
            self.PPFilmThicknessEntry.grid_forget()
            self.PPFilmThicknessUnitLabel.grid_forget()

            self.SocketStartLabel.grid_forget()
            self.SocketStartEntry.grid_forget()
            self.SocketStartUnitLabel.grid_forget()
            self.SocketEndLabel.grid_forget()
            self.SocketEndEntry.grid_forget()
            self.SocketEndUnitLabel.grid_forget()
            self.MouthStartLabel.grid_forget()
            self.MouthStartEntry.grid_forget()
            self.MouthStartUnitLabel.grid_forget()
            self.MouthEndLabel.grid_forget()
            self.MouthEndEntry.grid_forget()
            self.MouthEndUnitLabel.grid_forget()
            self.CarriageReturnPositionLabel.grid_forget()
            self.CarriageReturnPositionEntry.grid_forget()
            self.CarriageReturnPositionUnitLabel.grid_forget()
            self.CarriageReturnDelayLabel.grid_forget()
            self.CarriageReturnDelayEntry.grid_forget()
            self.CarriageReturnDelayUnitLabel.grid_forget()
            self.PPStartLabel.grid_forget()
            self.PPStartEntry.grid_forget()
            self.PPStartUnitLabel.grid_forget()
            self.PPEndLabel.grid_forget()
            self.PPEndEntry.grid_forget()
            self.PPEndUnitLabel.grid_forget()
            self.FlatExtruder75Label.grid_forget()
            self.FlatExtruder75Entry.grid_forget()
            self.FlatExtruder75UnitLabel.grid_forget()
            self.CladdingExtruder75Label.grid_forget()
            self.CladdingExtruder75Entry.grid_forget()
            self.CladdingExtruder75UnitLabel.grid_forget()
            self.MoldSpeedLabel.grid_forget()
            self.MoldSpeedEntry.grid_forget()
            self.MoldSpeedUnitLabel.grid_forget()

        #

        #

        #

        #

        #

    def PR(self):  # show widgets related to PR
        self.materialprofile.grid(row=0, column=15, columnspan=2, sticky="w", padx=5)
        self.flatDieProfile.grid(row=0, column=15, columnspan=2, sticky="w", padx=5)
        self.claddingDieProfile.grid(row=1, column=15, columnspan=2, sticky="w", padx=5)

        self.densityLabel.grid(row=1, column=0, padx=5, pady=5)
        self.densityEntry.grid(row=1, column=1, padx=5, pady=5)
        self.densityUnitLabel.grid(row=1, column=2, padx=1, pady=5)
        self.elasticLabel.grid(row=1, column=3, padx=20, pady=5, columnspan=2)
        self.elasticEntry.grid(row=1, column=5, padx=2, pady=5, sticky="w")
        self.elasticUnitLabel.grid(row=1, column=6, padx=1, pady=5)
        self.shrinkageLabel.grid(row=1, column=7, padx=20, pady=5, columnspan=2)
        self.shrinkageEntry.grid(row=1, column=9, padx=2, pady=5, sticky="w")
        self.shrinkageUnitLabel.grid(row=1, column=10, padx=1, pady=5)

        self.pipeLengthLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pipeLengthUnitLabel.grid(row=1, column=2, padx=1, pady=5)
        self.pipeLengthEnry.grid(row=1, column=1, padx=6, pady=5)
        self.pipeDiameterLabel.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.pipeDiameterUnitLabel.grid(row=1, column=5, padx=1, pady=5)
        self.pipeDiameterEnry.grid(row=1, column=4, padx=6, pady=5)
        self.pitchLabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.pitchEntry.grid(row=2, column=1, padx=6, pady=5)
        self.pitchUnitLabel.grid(
            row=2,
            column=2,
            padx=1,
            pady=5,
        )
        self.pitchFactorLabel.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.pitchFactorEntry.grid(row=2, column=4, padx=6, pady=5)
        self.pitchFactorUnitLabel.grid(
            row=2,
            column=5,
            padx=1,
            pady=5,
        )
        self.WallThicknessLabel.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.WallThicknessEntry.grid(row=3, column=4, padx=6, pady=5)
        self.WallThicknessUnitLabel.grid(row=3, column=5, padx=1, pady=5, sticky="w")
        self.finalPitchLabel.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.finalPitchEntry.grid(row=3, column=1, padx=6, pady=5)
        self.finalPitchUnitLabel.grid(row=3, column=2, padx=1, pady=5, sticky="w")
        self.PPDiameterLabel.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.PPDiameterEntry.grid(row=4, column=1, padx=6, pady=5)
        self.PPDiameterUnitLabel.grid(row=4, column=2, padx=1, pady=5, sticky="w")
        self.PPFilmThicknessLabel.grid(row=4, column=3, padx=10, pady=5, sticky="w")
        self.PPFilmThicknessEntry.grid(row=4, column=4, padx=6, pady=5)
        self.PPFilmThicknessUnitLabel.grid(row=4, column=5, padx=1, pady=5, sticky="w")

        self.SocketStartLabel.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.SocketStartEntry.grid(row=0, column=2, padx=10, pady=5)
        self.SocketStartUnitLabel.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.SocketEndLabel.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.SocketEndEntry.grid(row=0, column=5, padx=10, pady=5)
        self.SocketEndUnitLabel.grid(row=0, column=6, padx=10, pady=5, sticky="w")
        self.MouthStartLabel.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.MouthStartEntry.grid(row=1, column=2, padx=10, pady=5)
        self.MouthStartUnitLabel.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.MouthEndLabel.grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.MouthEndEntry.grid(row=1, column=5, padx=10, pady=5)
        self.MouthEndUnitLabel.grid(row=1, column=6, padx=10, pady=5, sticky="w")
        self.CarriageReturnPositionLabel.grid(
            row=2, column=1, padx=10, pady=5, sticky="w"
        )
        self.CarriageReturnPositionEntry.grid(row=2, column=2, padx=10, pady=5)
        self.CarriageReturnPositionUnitLabel.grid(
            row=2, column=3, padx=10, pady=5, sticky="w"
        )
        self.CarriageReturnDelayLabel.grid(row=2, column=4, padx=10, pady=5, sticky="w")
        self.CarriageReturnDelayEntry.grid(row=2, column=5, padx=10, pady=5)
        self.CarriageReturnDelayUnitLabel.grid(
            row=2, column=6, padx=10, pady=5, sticky="w"
        )
        self.PPStartLabel.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.PPStartEntry.grid(row=4, column=2, padx=10, pady=5)
        self.PPStartUnitLabel.grid(row=4, column=3, padx=10, pady=5, sticky="w")
        self.PPEndLabel.grid(row=4, column=4, padx=10, pady=5, sticky="w")
        self.PPEndEntry.grid(row=4, column=5, padx=10, pady=5)
        self.PPEndUnitLabel.grid(row=4, column=6, padx=10, pady=5, sticky="w")
        self.FlatExtruder75Label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.FlatExtruder75Entry.grid(row=5, column=2, padx=10, pady=5)
        self.FlatExtruder75UnitLabel.grid(row=5, column=3, padx=10, pady=5, sticky="w")
        self.CladdingExtruder75Label.grid(row=5, column=4, padx=10, pady=5, sticky="w")
        self.CladdingExtruder75Entry.grid(row=5, column=5, padx=10, pady=5)
        self.CladdingExtruder75UnitLabel.grid(
            row=5, column=6, padx=10, pady=5, sticky="w"
        )
        self.MoldSpeedLabel.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.MoldSpeedEntry.grid(row=6, column=2, padx=10, pady=5)
        self.MoldSpeedUnitLabel.grid(row=6, column=3, padx=10, pady=5, sticky="w")

        #

        #

        #

        #

        #

    def VW(self):
        
        pass

    def calculateVW(self):
        pass
    
    def calculatePR(self):
        self.density = float(self.densityEntry.get())
        self.elastic_modulus = float(self.elasticEntry.get())
        self.shrinkage = float(self.shrinkageEntry.get())

        self.pipe_length = float(self.pipeLengthEnry.get())
        self.pd = float(self.pipeDiameterEnry.get())
        self.p = float(self.pitchEntry.get()) - float(self.pitchFactorEntry.get())
        self.limitsCur.execute(
            "SELECT min_wall_thickness FROM diameter WHERE diameter="
            + str(int(self.pd))
        )
        minWallThickness = self.limitsCur.fetchall()
        self.limitsCur.execute(
            "SELECT body_diameter3 FROM moldSize WHERE mold_size=" + str(int(self.pd))
        )
        newPd = self.limitsCur.fetchall()
        try:
            newPd = newPd[0]
        except:
            print("error: No data for this pipe diameter in mold size")
            self.pd = [0]
        print(newPd[0])
        self.pd = float(newPd[0])
        print(self.pd)
        print(minWallThickness)
        try:
            minWallThickness = minWallThickness[0]
        except:
            print("error: No data for this pipe diameter in  wall thickness")
            minWallThickness = [0]
        print(minWallThickness)
        minWallThickness = float(minWallThickness[0])
        print(minWallThickness)
        while minWallThickness > float(self.WallThicknessEntry.get()):
            self.WallThicknessEntry.configure(
                fg_color="#6e4441", border_color="#f51505"
            )
            self.WallThicknessEntry.insert(
                0,
                self.Error(
                    self.productionFrame,
                    self.WallThicknessEntry,
                    "Wall thickness",
                    "at least",
                    str(minWallThickness),
                ),
            )
        self.productionError.configure(text="")
        self.WallThicknessEntry.configure(fg_color="grey20", border_color="grey30")
        self.s1 = (
            float(self.WallThicknessEntry.get()) * float(100 - self.shrinkage) / 100.0
        )
        self.ppd = float(self.PPDiameterEntry.get())
        self.s4 = (
            float(self.PPFilmThicknessEntry.get()) * float(100 - self.shrinkage) / 100.0
        )

        required_Sn = [2, 4, 6, 8, 12, 16]
        Y1 = self.s1 / 2.0
        Y2 = self.s1 + self.s4 + 0.9 * self.ppd / 2.0
        A1 = self.s1 * self.p
        A2 = (0.9 * self.ppd / 2.0 + self.s4) ** 2 * math.pi - (
            0.9 * self.ppd / 2.0
        ) ** 2 * math.pi
        H = (Y1 * A1 + Y2 * A2) / (A1 + A2)
        Y11 = abs(H - Y1)
        Y21 = abs(Y2 - H)
        J1 = self.p * (self.s1) ** 3 / 12.0
        J2 = (
            math.pi
            / 64.0
            * ((0.9 * self.ppd + 2.0 * self.s4) ** 4 - (0.9 * self.ppd) ** 4)
        )
        J = (J1 + A1 * Y11**2 + J2 + A2 * Y21**2) / self.p
        Sn = 1000.0 * J * self.elastic_modulus / self.pd**3

        # Equations for Pipe Weight
        V1 = self.pd * math.pi * 20.0 * 150.0
        V2 = self.pd * math.pi * 20.0 * 150.0
        V3 = (
            ((self.pd / 2.0 + self.s1) ** 2 - (self.pd / 2.0) ** 2)
            * math.pi
            * self.pipe_length
        )
        Sbf = ((self.ppd / 2.0 + self.s4) ** 2 - (self.ppd / 2.0) ** 2) * math.pi
        Lpp = self.pipe_length / self.p * (self.pd + self.s1 * 2) * math.pi
        V4 = Sbf * Lpp
        W1 = V1 * self.density / 1000000.0
        W2 = V2 * self.density / 1000000.0
        W3 = V3 * self.density / 1000000.0
        W4 = V4 * self.density / 1000000.0
        W = W1 + W2 + W3 + W4
        self.limitsCur.execute(
            "SELECT weight FROM ppwt WHERE pp_weight=" + str(int(self.ppd))
        )
        tempWk = self.limitsCur.fetchall()
        try:
            tempWk = tempWk[0]
        except:
            print("error: No data for this pp weight in ppwt")
            tempWk = [0]
        tempWk = float(tempWk[0])
        Wk = tempWk / 1000.0
        Wp = Lpp * Wk / 1000.0
        Wz = W1 + W2 + W3 + W4 + Wp
        W0 = Wz - W2 / 2.0
        pp_dist = self.p - self.ppd - self.s4 * 2.0

        self.SnLabel.configure(text="Stiffness: " + str(round(Sn, 2)) + " kN/m2")
        self.W1Label.configure(
            text="Socket pipe body weight: " + str(round(W1, 2)) + " kg"
        )
        self.W2Label.configure(
            text="Socket pipe body weight: "
            + str(round(W2, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.W3Label.configure(
            text="Flat film tube weight: "
            + str(round(W3, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.W4Label.configure(
            text="Coated film body weight: "
            + str(round(W4, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.WLabel.configure(
            text="Pipe weight excluding pp pipe: "
            + str(round(W, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.WkLabel.configure(text="PP pipe weight: " + str(round(Wk, 2)) + " kg/m")
        self.WpLabel.configure(
            text="PP pipe weight: "
            + str(round(Wp, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.WzLabel.configure(
            text="Pipe weight: "
            + str(round(Wz, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )
        self.W0Label.configure(
            text="Pipe body weight: "
            + str(round(W0, 2))
            + " kg/"
            + str(self.pipe_length / 1000.0)
            + "m"
        )

        self.SnLabel.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.W1Label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.W2Label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.W3Label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.W4Label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.WLabel.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.WkLabel.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.WpLabel.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.WzLabel.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.W0Label.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    def setResize(self, flag):
        self.resizable(flag, flag)


main = main()
main.mainloop()
