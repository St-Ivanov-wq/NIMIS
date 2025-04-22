# NIMIS Machine Data Processor

[![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Industrial IoT Data Pipeline Component**  
*Part of NIMIS Project - NebulOuS Horizon Europe Programme*

---

## 📖 Overview
Real-time directory monitoring system that processes industrial machine data files into PostgreSQL with automated archiving. Acts as the edge-layer data ingestion component for the NIMIS AI-driven IoT pipeline.

```python
# Core Workflow
1. Watches ~/machine_app/input for new files
2. Validates & parses machine sensor data
3. Stores structured records in PostgreSQL
4. Archives processed files to ~/machine_app/output
5. Maintains audit-ready logs

⚙️ Key Features
Smart File Handling
watchdog monitoring with 1-second write completion buffer

Encoding Detection
Auto-detects UTF-8/Windows-1251 encodings

Data Validation
Skips invalid lines and multilingual headers (EN/RU)

DB Integration
PostgreSQL connection pooling with env-based config

FAIR Compliance
Structured logging with timestamps and severity levels

🚀 Quick Start
Prerequisites
Python 3.10+

PostgreSQL 14+

.env file with DB credentials
# Installation
git clone https://github.com/St-Ivanov-wq/NIMIS.git
pip install -r requirements.txt

# Run
python app.py

🔧 Configuration

# .env.example
DB_NAME=nimis_prod
DB_USER=admin
DB_PASSWORD=securepass
DB_HOST=localhost
DB_PORT=5432

🐳 Docker Deployment

# Build and run
docker compose up --build

# Monitor logs
docker compose logs -f

📊 Database Schema

CREATE TABLE processed_data (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    machine_status VARCHAR(255) NOT NULL,
    terminal VARCHAR(50) NOT NULL,
    machine VARCHAR(50) NOT NULL,
    operator VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    unix_timestamp BIGINT NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW()
);


🔒 Security
Credentials stored in environment variables

Input sanitization for file parsing

PSQL connection with SSL mode preference



