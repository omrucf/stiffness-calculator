import sqlite3, pandas

conn = sqlite3.connect("limits.db")  # change to 'sqlite:///your_filename.db'

csvfile = "temp.csv"

# df = pandas.read_csv(csvfile)
# df.to_sql("ppwt", conn, if_exists="append", index=False)


cur = conn.cursor()


# cur.execute(
#     "UPDATE limits SET c4=30000 WHERE c1 = 'malek'"
# )
# # conn.commit()
# cur.execute("ALTER TABLE flatDie ADD COLUMN thickness REAL")

# cur.execute("DELETE FROM flatDie WHERE profile = 'ndhjbanshbdhsdasdashdjbadhjbas'")

# cur.execute("UPDATE flatDie SET thickness = 5 WHERE profile = 'test'")

# code = """ CREATE TABLE IF NOT EXISTS moldSize (
#                                         id INTEGER PRIMARY KEY,
#                                         mold_size REAL NOT NULL,
#                                         header_inner_circum REAL NOT NULL,
#                                         body_circum REAL NOT NULL,
#                                         head_diameter2 REAL NOT NULL,
#                                         body_diameter3 REAL NOT NULL
#                                     ); """

# code = "DROP TABLE IF EXISTS ppwt"


# code = """INSERT INTO diameter (diameter, min_ID, min_wall_thickness, socket_outer_circum_BD, socket_outer_circum_AD, header_inner_circum) VALUES (1200, 1185, 5, 3938, 3873, 3873)"""

# code = """INSERT INTO moldSize (mold_size, header_inner_circum, body_circum, head_diameter2, body_diameter3) VALUES (1200, 3958, 3828, 1259.87, 1218.49)"""
# """

# code = "UPDATE ppwt SET weight=450.0 WHERE pp_weight = 4;"

# code = """INSERT INTO ppwt (pp_weight, weight) VALUES (75, 400);"""

# cur.execute(code)

conn.commit()

# cur.execute("SELECT weight FROM ppwt WHERE pp_weight = 75")
cur.execute("SELECT * FROM ppwt")

rows = cur.fetchall()
# print(cur.description)
df = pandas.DataFrame(rows, columns=[description[0] for description in cur.description])
print(df)
