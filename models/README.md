# Database Models and Local Development Guide

This directory contains the SQLAlchemy ORM model definitions used by the Flask backend. These models map to tables in the SQLite database used during development.

---

## 🛠️ Database Inspection via DB Browser for SQLite

This project uses SQLite during development. You may inspect or modify the local database file using **DB Browser for SQLite**, a free and open-source visual tool.

### ✅ Installation

- Download DB Browser from:  
  https://sqlitebrowser.org/dl/

- Install it according to your operating system.

---

## 📂 Locating the Database File

By default, the SQLite database is created in the backend directory /redback-fit-backend/instance/your_database_name.db

Your database name will be whatever you set DATABASE_URL to in your .env file. If no value is selected it defaults to database