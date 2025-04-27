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

---## ☁️ AWS Deployment Guide
