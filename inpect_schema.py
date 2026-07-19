# inspect_modules.py

from database.db_manager import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT module_name, status
    FROM project_modules
    WHERE project_id = 2
    ORDER BY id;
""")

modules = cur.fetchall()

for module in modules:
    print(module)

print("Total modules:", len(modules))

cur.close()
conn.close()