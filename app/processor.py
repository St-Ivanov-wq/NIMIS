
import os
import time
import logging
from datetime import datetime
import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv


"""
	Code is written by S. Ivanov.
Monitors a directory for new files, processes machine data into
PostgreSQL, and archives files with logging 
"""

# Load environment variables from .env file
load_dotenv()

# Configure directories
INPUT_DIR = os.path.expanduser('~/machine_app/input')
OUTPUT_DIR = os.path.expanduser('~/machine_app/output')
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'sslmode': 'prefer',
    'connect_timeout': 5  # Added connection timeout
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(OUTPUT_DIR, 'logs.txt')),
        logging.StreamHandler()
    ]
)

def init_db(max_retries=5, initial_wait=2):
    """Initialize database connection with retry logic"""
    conn = None
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS processed_data (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    machine_status VARCHAR(255) NOT NULL,
                    terminal VARCHAR(50) NOT NULL,
                    machine VARCHAR(50) NOT NULL,
                    operator VARCHAR(100) NOT NULL,
                    event_date DATE NOT NULL,
                    unix_timestamp BIGINT NOT NULL,
                    processed_at TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()
            logging.info("Database initialization completed")
            return True
        except psycopg2.OperationalError as e:
            wait_time = initial_wait ** (attempt + 1)
            logging.warning(f"Connection attempt {attempt+1}/{max_retries} failed. Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"Database initialization error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    logging.error("Max database connection retries exceeded")
    raise RuntimeError("Failed to connect to database after multiple attempts")

def get_db_connection():
    """Get a new database connection with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise

def process_file(file_path):
    """Process a single file with enhanced error handling"""
    filename = os.path.basename(file_path)
    conn = None
    try:
        logging.info(f"Processing file: {filename}")

        # Read file with encoding detection
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='windows-1251') as f:
                content = f.read()

        records = []
        for line_number, line in enumerate(content.split('\n'), 1):
            line = line.strip().rstrip(';')
            if not line:
                continue
            
            # Skip header lines
            if any(keyword in line.lower() for keyword in ['machine_status', 'terminaл', 'работник']):
                logging.info(f"Skipping header: {line}")
                continue

            parts = [part.strip() for part in line.split(';')]
            if len(parts) != 6:
                logging.warning(f"Skipping invalid line {line_number}")
                continue

            try:
                records.append({
                    'filename': filename,
                    'machine_status': parts[0],
                    'terminal': parts[1],
                    'machine': parts[2],
                    'operator': parts[3],
                    'event_date': datetime.strptime(parts[4], '%d.%m.%Y').date(),
                    'unix_timestamp': int(parts[5])
                })
            except (ValueError, TypeError) as e:
                logging.error(f"Line {line_number} error: {str(e)}")

        if records:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.executemany("""
                INSERT INTO processed_data
                (filename, machine_status, terminal, machine, operator, event_date, unix_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [(r['filename'], r['machine_status'], r['terminal'],
                   r['machine'], r['operator'], r['event_date'],
                   r['unix_timestamp']) for r in records])
            conn.commit()
            logging.info(f"Inserted {len(records)} records from {filename}")

        os.rename(file_path, os.path.join(OUTPUT_DIR, filename))
        logging.info(f"Moved {filename} to output")

    except Exception as e:
        logging.error(f"Error processing {filename}: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

class FileHandler(FileSystemEventHandler):
    """Enhanced file handler with write completion check"""
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            try:
                # Verify file is closed before processing
                with open(event.src_path, 'r') as f:
                    f.read(1)
                process_file(event.src_path)
            except IOError as e:
                logging.warning(f"File not ready: {os.path.basename(event.src_path)}")

if __name__ == "__main__":
    if init_db():
        observer = Observer()
        observer.schedule(FileHandler(), INPUT_DIR, recursive=False)
        observer.start()
        
        logging.info(f"Monitoring {INPUT_DIR}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
