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

# Create directories
INPUT_DIR = os.path.expanduser('~/machine_app/input')
OUTPUT_DIR = os.path.expanduser('~/machine_app/output')
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(OUTPUT_DIR, 'logs.txt')),
        logging.StreamHandler()
    ]
)

# Database configuration from environment variables
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'sslmode': 'prefer'
}

def init_db():
    """Initialize database connection and create tables"""
    conn = None
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
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def process_file(file_path):
    """Process a single file and insert records into database"""
    conn = None
    try:
        filename = os.path.basename(file_path)
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
            # Clean and validate line
            line = line.strip().rstrip(';')
            if not line:
                continue
            
            # Skip header lines (Russian or English)
            if any(keyword in line.lower() for keyword in ['machine_status', 'terminaл', 'работник']):
                logging.info(f"Skipping header line: {line}")
                continue

            parts = [part.strip() for part in line.split(';')]
            if len(parts) != 6:
                logging.warning(f"Skipping invalid line {line_number} in {filename}")
                continue

            try:
                # Parse according to sample data structure
                record = {
                    'filename': filename,
                    'machine_status': parts[0],    # First field
                    'terminal': parts[1],          # Second field
                    'machine': parts[2],           # Third field
                    'operator': parts[3],          # Fourth field
                    'event_date': datetime.strptime(parts[4], '%d.%m.%Y').date(),
                    'unix_timestamp': int(parts[5])
                }
                records.append(record)
            except (ValueError, TypeError) as e:
                logging.error(f"Error parsing line {line_number}: {str(e)}")

        if records:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            for record in records:
                cur.execute("""
                    INSERT INTO processed_data
                    (filename, machine_status, terminal, machine, operator, event_date, unix_timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    record['filename'],
                    record['machine_status'],
                    record['terminal'],
                    record['machine'],
                    record['operator'],
                    record['event_date'],
                    record['unix_timestamp']
                ))
            conn.commit()
            logging.info(f"Inserted {len(records)} records from {filename}")

        # Move processed file
        os.rename(file_path, os.path.join(OUTPUT_DIR, filename))
        logging.info(f"Moved {filename} to output directory")

    except Exception as e:
        logging.error(f"Error processing {filename}: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

class FileHandler(FileSystemEventHandler):
    """Watchdog event handler for new files"""
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)  # Allow file write to complete
            process_file(event.src_path)

if __name__ == "__main__":
    init_db()
    observer = Observer()
    observer.schedule(FileHandler(), INPUT_DIR, recursive=False)
    observer.start()
    
    logging.info(f"Started monitoring {INPUT_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
