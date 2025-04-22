**Real-Time Directory Monitoring**  
Automatically detects and processes new files in `~/machine_app/input` using `watchdog`.

**Industrial Data Pipeline**  
- Validates/parses machine sensor data  
- Stores structured records in PostgreSQL  
- Archives processed files with audit logs

**Edge Layer Integration**  
Prepares data for AI-driven anomaly detection in the

# Edit the .env file to match your database settings
#Block Diagram

![NIMIS](https://github.com/user-attachments/assets/279cb028-98c4-411f-8ef1-d2de8f9583b0)


## Quick Start
1. **Prerequisites**  
   PostgreSQL 14+, Python 3.10+

2. **Configure Environment**  
   ```bash
   cp .env.example .env  # Update with your DB credentials
