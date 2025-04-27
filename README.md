# NIMIS: Industrial IoT Data Processor

[![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Production-Ready Machine Data Pipeline for Predictive Maintenance**

---

## 🌟 Features
- **Real-Time File Monitoring** - Watchdog-based detection of new data files
- **Multi-Encoding Support** - Auto-detects UTF-8/Windows-1251 encodings
- **Smart Data Validation** - Skips invalid lines & multilingual headers
- **PostgreSQL Integration** - Connection pooling with retry logic
- **Audit-Ready Logging** - Structured logs with severity levels
- **AWS Optimized** - Pre-configured for EC2 + RDS deployment

```mermaid
graph LR
A[Shop Floor Machines] --> B(Input Directory)
B --> C{Processor}
C --> D[(PostgreSQL DB)]
C --> E[Output Archive]
D --> F[Analytics Dashboard]
E --> G[Long-Term Storage]
AWS Deployment
1. Infrastructure Setup

EC2 Instance (Ubuntu 22.04):
bash

- AMI: Ubuntu Server 22.04 LTS
- Security Group: SSH (22), PostgreSQL (5432)

RDS PostgreSQL:
ini

DB Engine: PostgreSQL 14
Instance Class: db.t3.micro
Storage: 20GB GP2

2. Server Configuration
bash

# Clone repository
git clone https://github.com/St-Ivanov-wq/NIMIS.git
cd NIMIS-main

# Create data directories
mkdir -p ~/machine_app/{input,output}

3. Database Setup

Create .env file:
bash

nano .env

ini

DB_NAME=nimis_prod
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=your-rds-endpoint
DB_PORT=5432

4. Installation
bash

# System dependencies
sudo apt update && sudo apt install python3-pip python3-venv -y

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

5. Run Service
bash

cd app
python processor.py

Production Daemon (systemd):
bash

sudo nano /etc/systemd/system/nimis.service

ini

[Unit]
Description=NIMIS Data Processor
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/NIMIS-main/app
ExecStart=/home/ubuntu/NIMIS-main/venv/bin/python processor.py
Restart=always

[Install]
WantedBy=multi-user.target

bash

sudo systemctl daemon-reload
sudo systemctl enable --now nimis

🐳 Docker Deployment
bash

docker compose -f docker/docker-compose.yml up --build

🔧 Configuration
Database Schema
sql

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

File Formats
text

Operational;TerminalA;CNC-01;Ivanov I.I.;25.04.2024;1714060800;
Maintenance;TerminalB;Lathe-03;Petrov P.P.;26.04.2024;1714147200;

🔒 Security

    Credentials Protection - Never commit .env files

    Network Security - VPC peering for EC2-RDS communication

    Input Sanitization - Strict field validation rules

    Access Control - IAM roles for AWS services

🛠️ Troubleshooting
Common Issues

Database Connection Failed
bash

psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;"

File Processing Stuck
bash

tail -f ~/machine_app/output/logs.txt

Permission Denied
bash

chmod -R 755 ~/machine_app

Missing Dependencies
bash

source venv/bin/activate && pip install -r requirements.txt

📂 Repository Structure

NIMIS-main/
├── app/
│   └── processor.py           # Core processing logic
├── AnomalyDetection/          # ML models directory
│   └── anomaly_detection.ipynb
├── TestData/                  # Sample input files
│   ├── production/
│   └── test/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── backup_db.sh               # PostgreSQL backup script
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
└── LICENSE

📜 License

Apache 2.0 License - See LICENSE for details.

*Developed by S. Ivanov - Part of NIMIS Industry 4.0 Initiative*


