# NIMIS: Industrial IoT Data Processor  
[![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  

**Production-Ready Machine Data Pipeline for Predictive Maintenance**  

---

## 🌟 Key Features  
- 🕵️ **Real-Time Monitoring**: Directory watcher for instant file processing  
- 📁 **Smart File Handling**: Supports UTF-8 & Windows-1251 encodings  
- ✅ **Data Validation**: Skips invalid lines and multilingual headers  
- 🗄️ **PostgreSQL Integration**: Connection pooling with retry logic  
- 📊 **Structured Logging**: Audit-ready logs with severity levels  
- ☁️ **AWS Optimized**: Pre-configured for EC2 + RDS deployment  

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- AWS Account (for cloud deployment)

```bash
# Clone repository
git clone https://github.com/St-Ivanov-wq/NIMIS.git
cd NIMIS-main

# Create data directories
mkdir -p ~/machine_app/{input,output}
```
---

## ☁️ AWS Deployment Guide
1. Infrastructure Setup

EC2 Instance (Ubuntu 22.04):
```bash
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t3.medium
- Security Group Rules:
- SSH (Port 22) - Restricted to your IP
- PostgreSQL (Port 5432) - Open to EC2 security group
```
RDS PostgreSQL:
```ini
DB Engine: PostgreSQL 14
Instance Class: db.t3.micro
Storage: 20GB GP2
Allocated Storage: 20GB
Public Accessibility: No
```

**2. Configuration**
```bash
nano .env
```
```ini
DB_NAME=nimis_prod
DB_USER=postgres //or some name
DB_PASSWORD=your_password_here
DB_HOST=your-rds-endpoint
DB_PORT=5432
```

**3. Service Installation**
```bash
sudo apt update && sudo apt install python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**4. Launch Application**
```bash
cd app
python processor.py
```

**5. Production Deployment (systemd)**
```bash
sudo nano /etc/systemd/system/nimis.service
```
```ini
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
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now nimis
```
---
## 🐳 Docker Deployment
---
**1. Build Containers**
```bash
docker compose -f docker/docker-compose.yml build
```

**2. Start Services**
```bash
docker compose -f docker/docker-compose.yml up -d
```
**3. Monitor Logs**
```bash
docker compose -f docker/docker-compose.yml logs -f
```

## 📄 Database Schema
---
```sql
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
```

## 📂 Repository Structure
---

NIMIS-main/
├── app/
│   └── processor.py           # Core processing logic
├── AnomalyDetection/          # Machine learning models
│   └── anomaly_detection.ipynb
├── TestData/                  # Sample datasets
│   ├── production/
│   └── test/
├── docker/
│   ├── Dockerfile             # Container configuration
│   └── docker-compose.yml     # Service orchestration
├── backup_db.sh               # Database backup script
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
└── LICENSE                    # Apache 2.0 License
