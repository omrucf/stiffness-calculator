import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

# cur.execute(
#     """CREATE TABLE IF NOT EXISTS diameter (
#                 id INTEGER PRIMARY KEY,
#                 pipe_diameter REAL NOT NULL,
#                 min_wall_thickness REAL NOT NULL,
#                 mold_diameter REAL NOT NULL,
#                 mold_optimal_temperature REAL);"""
# )

# cur.execute(
#     """CREATE TABLE IF NOT EXISTS ppwt (
#                                         id integer PRIMARY KEY,
#                                         pp_diameter REAL NOT NULL,
#                                         weight REAL NOT NULL
#                                     );"""
# )


# ppwt = {27:[90],
# 29:[100],
# 30:[108],
# 34:[130],
# 36:[135],
# 42:[170],
# 45:[195],
# 54:[230],
# 56:[260],
# 60:[310],
# 65:[380],
# 70:[390],
# 75:[400],
# 80:[440],
# 85:[500],
# 90:[620],
# 100:[650],
# 105:[715],
# 110:[840],
# 120:[960]}

# for p in ppwt:
#     for w in ppwt[p]:
#         cur.execute('INSERT INTO ppwt (pp_diameter, weight) VALUES (?, ?)', (p, w))


# moldDiameter = {
#     800: [150],
#     900: [150],
#     1000: [150],
#     1200: [160],
#     1400: [160],
#     2000: [170],
# }

# for m in moldDiameter:
#     for d in moldDiameter[m]:
#         cur.execute(
#             "INSERT INTO moldDiameter (mold_diameter, mold_optimal_temperature) VALUES (?, ?)",
#             (m, d),
#         )


# pipe_diameter	mold_diameter	min_wall_thickness	mold_optimal_temprature
# diameter = [(600,611.15,3.5, None),
# (700, 710.47, 4, None),
# (800, 813.60, 4.5, 150),
# (1000, 1015.41, 5, 150),
# (1200, 1218.49, 5, 160),
# (1600, 1625.93, 5.5, None),
# (2000, 2027.63, 6, 170)]

# for d in diameter:
#     cur.execute(
#         "INSERT INTO diameter (pipe_diameter, mold_diameter, min_wall_thickness, mold_optimal_temperature) VALUES (?, ?, ?, ?)",
#         d,
# )



cur.execute("""ALTER TABLE claddingDie 
RENAME COLUMN ppd TO pp_diameter;""")
conn.commit()
temp = cur.fetchall()
# all = []
# for tup in temp:
#     all.append((tup[1], tup[3]))
print(temp)
