import sqlite3, pandas

conn = sqlite3.connect("profiles.db")  # change to 'sqlite:///your_filename.db'

csvfile = "temp.csv"

# df = pandas.read_csv(csvfile)
# df.to_sql("rawMaterial", conn, if_exists="append", index=False)


cur = conn.cursor()


# cur.execute(
#     "UPDATE limits SET c4=30000 WHERE c1 = 'malek'"
# )
# # conn.commit()
# cur.execute("DELETE FROM flatDie WHERE profile = 'test2' or profile = 'test3'")

# conn.commit()

cur.execute("SELECT * FROM flatDie")

rows = cur.fetchall()
df = pandas.DataFrame(rows, columns=[description[0] for description in cur.description])
print(df)
