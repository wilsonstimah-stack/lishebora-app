import sqlite3
import json
import datetime
from common_utils import hash_password, check_password

# --- CONFIG ---
SERVER_DB_FILE = "server_data.db"
CLIENT_DB_FILE = "client_data.db"

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_file)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users Table (Both Client & Server have this for Auth check/Sync)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password_hash TEXT,
                role TEXT,
                age_bracket TEXT,
                created_at TEXT,
                consent_given INTEGER DEFAULT 0
            )
        ''')
        
        # Migration for existing DBs
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN consent_given INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass


        # Profiles (Anthropometrics)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER,
                weight REAL,
                height REAL,
                age INTEGER,
                gender TEXT,
                condition TEXT,
                updated_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # Logs (Dietary Intake)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                food_items TEXT,
                analysis TEXT,
                synced INTEGER DEFAULT 0
            )
        ''')

        # Messages (AI/Nutritionist)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT,
                sender TEXT, 
                is_ai INTEGER,
                status TEXT, 
                timestamp TEXT,
                synced INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()

# --- SERVER API SIMULATION ---
class ServerBackend:
    def __init__(self):
        self.db = DatabaseManager(SERVER_DB_FILE)

    def register_user(self, email, phone, password, role, age_bracket):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            pwd_hash = hash_password(password)
            cursor.execute("INSERT INTO users (email, phone, password_hash, role, age_bracket, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                           (email, phone, pwd_hash, role, age_bracket, datetime.datetime.now().isoformat()))
            conn.commit()
            return {"status": "success", "message": "User registered successfully"}
        except sqlite3.IntegrityError:
            return {"status": "error", "message": "User already exists"}
        finally:
            conn.close()

    def login(self, identifier, password):
        # identifier can be email or phone
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash, role, age_bracket, consent_given FROM users WHERE email=? OR phone=?", (identifier, identifier))
        row = cursor.fetchone()
        conn.close()
        
        if row and check_password(row[1], password):
            return {
                "status": "success", 
                "user_id": row[0], 
                "role": row[2], 
                "age_bracket": row[3],
                "consent_given": row[4]
            }
        return {"status": "error", "message": "Invalid credentials"}

    def set_consent(self, user_id, consent_status=1):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET consent_given=? WHERE id=?", (consent_status, user_id))
        conn.commit()
        conn.close()
        return {"status": "success"}


    def sync_data(self, user_id, logs, messages, profile=None):
        # Receive data from client
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Sync Profile if provided
        if profile:
            # profile is specific keys: weight, height, condition, status, age
            # check if exists
            cursor.execute("SELECT user_id FROM profiles WHERE user_id=?", (user_id,))
            if cursor.fetchone():
                cursor.execute("UPDATE profiles SET weight=?, height=?, condition=?, nutritional_status=?, updated_at=? WHERE user_id=?",
                               (profile['weight'], profile['height'], profile['condition'], profile['status'], datetime.datetime.now().isoformat(), user_id))
            else:
                 cursor.execute("INSERT INTO profiles (user_id, weight, height, condition, nutritional_status, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                               (user_id, profile['weight'], profile['height'], profile['condition'], profile['status'], datetime.datetime.now().isoformat()))

        # In a real app, we'd upsert. Here we just insert simplified.
        count_logs = 0
        for log in logs:
            # Check if exists (rudimentary check)
            cursor.execute("SELECT id FROM food_logs WHERE user_id=? AND date=? AND food_items=?", (user_id, log[2], log[3]))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO food_logs (user_id, date, food_items, analysis, synced) VALUES (?, ?, ?, ?, 1)",
                               (user_id, log[2], log[3], log[4]))
                count_logs += 1

        count_msgs = 0
        for msg in messages:
            # Check duplicates by timestamp/content
            cursor.execute("SELECT id FROM messages WHERE user_id=? AND timestamp=?", (user_id, msg[6]))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO messages (user_id, content, sender, is_ai, status, timestamp, synced) VALUES (?, ?, ?, ?, ?, ?, 1)",
                               (user_id, msg[2], msg[3], msg[4], msg[5], msg[6]))
                count_msgs += 1
        
        conn.commit()
        conn.close()
        return {"status": "success", "synced_logs": count_logs, "synced_msgs": count_msgs}

    def get_dashboard_stats(self):
        # For Developer App
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='client'")
        total_clients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages WHERE status='pending'")
        pending_qs = cursor.fetchone()[0]
        
        conn.close()
        return {"total_clients": total_clients, "pending_questions": pending_qs}

    def get_pending_questions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT m.id, u.email, m.content, m.timestamp FROM messages m JOIN users u ON m.user_id = u.id WHERE m.status='pending'")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def answer_question(self, msg_id, response):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET status='answered', content=content || ' || RESPONSE: ' || ? WHERE id=?", (response, msg_id))
        conn.commit()
        conn.close()

# --- CLIENT LOCAL MANAGER ---
class ClientLocalManager:
    def __init__(self):
        self.db = DatabaseManager(CLIENT_DB_FILE)
        self.server = ServerBackend() # Simulating 'Online' connection
    
    def save_profile(self, user_id, weight, height, condition, status, age):
        # Save locally
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Upsert logic for sqlite
        cursor.execute("SELECT user_id FROM profiles WHERE user_id=?", (user_id,))
        if cursor.fetchone():
             cursor.execute("UPDATE profiles SET weight=?, height=?, condition=?, nutritional_status=?, updated_at=? WHERE user_id=?",
                            (weight, height, condition, status, datetime.datetime.now().isoformat(), user_id))
        else:
             cursor.execute("INSERT INTO profiles (user_id, weight, height, condition, nutritional_status, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, weight, height, condition, status, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO food_logs (user_id, date, food_items, analysis, synced) VALUES (?, ?, ?, ?, 0)",
                       (user_id, datetime.datetime.now().strftime("%Y-%m-%d"), food_items, analysis))
        conn.commit()
        conn.close()

    def add_message(self, user_id, content, sender="user", is_ai=0, status="pending"):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (user_id, content, sender, is_ai, status, timestamp, synced) VALUES (?, ?, ?, ?, ?, ?, 0)",
                       (user_id, content, sender, is_ai, status, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def sync_with_server(self, user_id):
        # Push unsynced data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM food_logs WHERE synced=0 AND user_id=?", (user_id,))
        unsynced_logs = cursor.fetchall()
        
        cursor.execute("SELECT * FROM messages WHERE synced=0 AND user_id=?", (user_id,))
        unsynced_msgs = cursor.fetchall()
        
        if unsynced_logs or unsynced_msgs:
            # Push to server
            # For this demo, we'll blindly sync the latest profile from local if it exists
            conn = self.db.get_connection() # Re-open for profile read
            pc = conn.cursor()
            pc.execute("SELECT weight, height, condition, nutritional_status FROM profiles WHERE user_id=?", (user_id,))
            p_row = pc.fetchone()
            conn.close()
            
            profile_payload = None
            if p_row:
                profile_payload = {
                    "weight": p_row[0],
                    "height": p_row[1],
                    "condition": p_row[2],
                    "status": p_row[3]
                }

            self.server.sync_data(user_id, unsynced_logs, unsynced_msgs, profile_payload)
            
            # Mark as synced locally
            cursor.execute("UPDATE food_logs SET synced=1 WHERE user_id=?", (user_id,))
            cursor.execute("UPDATE messages SET synced=1 WHERE user_id=?", (user_id,))
            conn.commit()
            return True
        else:
             # Even if logs/msgs empty, maybe profile changed? 
             # For simplicity in this demo, we always try sync profile if requested or modify logic slightly.
             # But let's stick to the structure.
             pass
             
        conn.close()
        return False
