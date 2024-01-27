import sqlite3

conn = sqlite3.connect("limits.db")
cur = conn.cursor()


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
#         cur.execute('INSERT INTO ppwt (pp_weight, weight) VALUES (?, ?)', (p, w))


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



conn.commit()
