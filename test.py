# import math


# wall_thickness = 5
# pd = 1218.49
# pipe_length = 6000
# elastic_modulus = 900
# density = 0.96
# shrinkage = 3


# H = (wall_thickness * ((100 - shrinkage) / 100)) / 2.0
# Sv = 2.0 * H
# J = math.pow(Sv, 3.0) / 12.0
# Sn = 1000.0 * J * elastic_modulus / math.pow(pd, 3.0)
# V1 = pd * math.pi * 20.0 * 150.0
# V2 = pd * math.pi * 20.0 * 150.0
# V3 = (
#     (
#         math.pow(pd / 2.0 + (wall_thickness * ((100 - shrinkage) / 100)), 2.0)
#         - math.pow(pd / 2.0, 2.0)
#     )
#     * math.pi
#     * pipe_length
# )
# W1 = V1 * density / 1000000.0
# W2 = V2 * density / 1000000.0
# W3 = V3 * density / 1000000.0
# W = W1 + W2 + W3
# W0 = W - W2 / 2.0


# print(["sn", "w1", "w2", "w3", "w", "w0"])
# print(
#     [round(Sn, 2), round(W1, 2), round(W2, 2), round(W3, 2), round(W, 2), round(W0, 2)]
# )

import sqlite3

conn = sqlite3.connect("limits.db")
cur = conn.cursor()

# cur.execute(
#     """
#             CREATE TABLE IF NOT EXISTS temp (
#                 id INTEGER PRIMARY KEY,
#                 profile TEXT NOT NULL,
#                 pitch REAL NOT NULL,
#                 thickness REAL NOT NULL)
#             """
# )

# cur.execute(
#     """
#             ALTER TABLE temp RENAME TO flatDie
#             """
# )

cur.execute(
    """
            DELETE FROM ppwt WHERE id >=7
            """
)

conn.commit()
