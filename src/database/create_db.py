import psycopg2
from db_connection import connect_to_db

def create_jobs_table():
    """
    Creates the 'jobs' table in PostgreSQL if it doesn't already exist.
    """
    # Connect to the database
    conn = connect_to_db()
    if conn is None:
        print("❌ Database connection failed. Exiting.")
        return

    try:
        cursor = conn.cursor()

        # SQL query to create the jobs table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            industry TEXT,
            date_posted TEXT NOT NULL,
            job_description TEXT NOT NULL,
            skills TEXT,
            salary TEXT,
            source TEXT NOT NULL
        );
        """
        
        # Execute the query
        cursor.execute(create_table_query)
        conn.commit()

        print("✅ 'jobs' table created successfully (or already exists).")

    except Exception as e:
        print("❌ Error creating table:", e)
    
    finally:
        cursor.close()
        conn.close()
        print("🔄 Database connection closed.")

# Run the script
if __name__ == "__main__":
    create_jobs_table()
