import sqlite3, pandas

conn = sqlite3.connect("limits.db")  # change to 'sqlite:///your_filename.db'

csvfile = "moldDiameter.csv"

df = pandas.read_csv(csvfile)
df.to_sql("moldDiameter", conn, if_exists="append", index=False)
