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

Apache 2.0 License - See LICENSE for details.

*Developed by S. Ivanov - Part of NIMIS Industry 4.0 Initiative*


