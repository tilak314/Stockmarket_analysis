import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Delete rows based on a condition
ans = cursor.execute("SELECT * FROM stock_analyses")
conn.commit()
conn.close()

print(ans)

for i in ans:
    print(i.ticker)