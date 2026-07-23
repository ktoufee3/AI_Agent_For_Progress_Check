# inspect_schema.py
from database.db_manager import get_connection

def inspect_schema():
    try:
        conn = get_connection()
        cur = conn.cursor()


        # List all tables
        cur.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
        """)
        
        tables = cur.fetchall()
        print(f"Found {len(tables)} tables:\n")
        
        for table in tables:
            table_name = table[0]
            print(f"\n{'='*60}")
            print(f"Table: {table_name}")
            print('='*60)
            
            # Get column information
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cur.fetchall()
            print("Columns:")
            for col in columns:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  - {col[0]}: {col[1]} ({nullable}){default}")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"\nTotal rows: {count}")
            
            # Show sample data (first 3 rows)
            if count > 0:
                cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_rows = cur.fetchall()
                
                # Get column names for display
                col_names = [desc[0] for desc in cur.description]
                print(f"\nSample data (first {len(sample_rows)} rows):")
                print("-" * 60)
                for row in sample_rows:
                    for i, col_name in enumerate(col_names):
                        value = row[i]
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 50:
                            value = value[:50] + "..."
                        print(f"  {col_name}: {value}")
                    print("-" * 40)
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def check_data_in_table():
    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='projects';
        """)

        columns_names = cur.fetchall()
        print(f"columns_names: {columns_names}")

        cur.execute("""
        SELECT * from project_commits;
        """)

        columns_data = cur.fetchall()

        print("commits data in project_commits: ", columns_data)


        cur.execute("""
            select * from project_git_status;
        """)


        git_status = cur.fetchall()
        print("git_status: ", git_status)


    except Exception as e:
        pass

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # inspect_schema()

    check_data_in_table()

