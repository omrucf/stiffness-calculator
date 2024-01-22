import sqlite3

conn = sqlite3.connect("limits.db")
cur = conn.cursor()

# cur.execute(
#     """
#             CREATE TABLE IF NOT EXISTS diameter (
#                 id INTEGER PRIMARY KEY,
#                 diameter REAL NOT NULL,
#                 min_wall_thickness REAL NOT NULL,
#                 body_diameter3 REAL NOT NULL)
#             """
# )

# cur.execute(
#     """
#             ALTER TABLE temp RENAME TO flatDie
#             """
# )

# cur.execute(
#     """
#             INSERT INTO diameter (diameter, min_wall_thickness, body_diameter3) VALUES (1200, 5, 1218.49)
#             """
# )

# cur.execute(
#     """
#             DELETE FROM claddingDie WHERE id >= 0
#             """
# )

# flat_die = {
#     27: [3],
#     34: [3, 4],
#     42: [4, 5, 6],
#     54: [4, 5, 6],
#     65: [5, 6, 7],
#     75: [5, 6, 7, 8],
#     90: [6, 7, 8, 10],
#     110: [6, 7, 8, 10],
# }

flat_die = {800: [150], 900: [150], 1000: [150], 1200: [160], 1400: [160], 2000: [170]}


for pitch, other in flat_die.items():
    for wall_thickness in other:
        cur.execute(
            """
                    INSERT INTO moldDiameter ( mold_diameter, mold_optimal_temperature) VALUES (?, ?)
                    """,
            (pitch, wall_thickness),
        )

conn.commit()
