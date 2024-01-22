import sqlite3

conn = sqlite3.connect("profiles.db")
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

cur.execute(
    """
            DELETE FROM claddingDie WHERE id >= 0
            """
)

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


# for pitch, other in flat_die.items():
#     for wall_thickness in other:
#         cur.execute(
#             """
#                     INSERT INTO claddingDie (profile, ppd, pp_thickness) VALUES (?, ?, ?)
#                     """,
#             (str(pitch) + "-S" + str(wall_thickness), pitch, wall_thickness),
#         )

conn.commit()
