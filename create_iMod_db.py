import os
import mysql.connector
import getpass
from dotenv import load_dotenv

load_dotenv()

# Database schema
TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name VARCHAR(100),
            phone_number VARCHAR(20) UNIQUE,
            avatar_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """,
    "profiles": """
        CREATE TABLE IF NOT EXISTS profiles (
            user_id CHAR(36) PRIMARY KEY,
            bio TEXT,
            website VARCHAR(255),
            location VARCHAR(100),
            birthdate DATE,
            gender ENUM('male', 'female', 'non-binary', 'other'),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "user_settings": """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id CHAR(36) PRIMARY KEY,
            theme ENUM('light', 'dark') DEFAULT 'light',
            notifications_enabled BOOLEAN DEFAULT TRUE,
            language VARCHAR(10) DEFAULT 'en',
            privacy ENUM('public', 'friends-only', 'private') DEFAULT 'public',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "friendships": """
        CREATE TABLE IF NOT EXISTS friendships (
            id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            user_id CHAR(36),
            friend_id CHAR(36),
            status ENUM('pending', 'accepted', 'blocked') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "block_list": """
        CREATE TABLE IF NOT EXISTS block_list (
            id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            user_id CHAR(36),
            blocked_user_id CHAR(36),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, blocked_user_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (blocked_user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
}

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "database": os.getenv("DB_NAME"),
    "password": None,
    "port": 3306
}

def create_database(password):
    """Connects to MySQL, creates the database, and returns the connection and cursor."""
    db_config["password"] = password 
    try:
        db_conn = mysql.connector.connect(**db_config)
        if db_conn.is_connected():
            print("✅ Connected to MySQL!")
            return {"connection": db_conn, "cursor": db_conn.cursor()} 
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

def create_tables(conn,cursor):
    try:
        for table_name, table_sql in TABLES.items():
            cursor.execute(table_sql)
            print(f"🛠️ Created/verified table: {table_name}")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database setup complete.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    password = getpass.getpass("Enter the database password: ")
    db = create_database(password)
    print("1️⃣ Create Table\n")
    if db["cursor"] is not None:
        choice = input("Select an option: ")
        if choice == "1":
            create_tables(db["connection"],db["cursor"])
        else:
            print("❌ Invalid choice.")
