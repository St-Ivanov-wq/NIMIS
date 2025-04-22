What It Does
Watches for New Files
Uses watchdog to monitor a folder and kick off processing whenever a new file shows up.

Process Machine Data
Parses and validates raw machine sensor files

Stores clean, structured data into PostgreSQL

Keeps a log of what was processed and archives the original files

Feeds into the Bigger System
Acts as the edge layer for the NIMIS Pipeline, prepping data for AI-based monitoring and analysis.

Getting Started
Requirements
Python 3.10 or newer

PostgreSQL 14+

Setup
bash
Copy
Edit
cp .env.example .env
# Edit the .env file to match your database settings
