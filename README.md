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
