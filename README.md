# 🏦 Banking CLI

A Python-based **command-line banking system** that allows you to manage users, accounts, and transactions with ease. The project uses **PostgreSQL** for persistent storage and provides a simple CLI interface for common banking operations.

---

## ✨ Features

* 👤 Create users
* 🏦 Create bank accounts
* 💰 Deposit funds into an account
* 💸 Withdraw funds from an account
* 🔁 Transfer money between accounts
* 📜 View transaction history

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure you have the following installed:

* Python 3.9+
* PostgreSQL
* `psql` CLI tool

---

## 🗄️ Database Setup (PostgreSQL)

### Option 1: Create a New Database

If you **do not already have** a database:

```bash
psql -U <your_username> -f bank_db.sql
```

### Option 2: Use an Existing Database

If you **already have** a database named `bank_db`:

```bash
psql -U <your_username> -d bank_db -f bank_db_nodb_creation.sql
```

> 💡 Replace `<your_username>` with your PostgreSQL username.

---

## 🔧 Database Configuration (`config.py`)

The application connects to PostgreSQL using the settings defined in `config.py`. If you are running PostgreSQL on a **different server**, or using **custom credentials**, you will need to update this file.

### Default Configuration

By default, the database connection is configured as follows:

* **Database name:** `bank_db`
* **Host:** `localhost`
* **Port:** `5432`
* **User & Password:** Loaded from environment variables

### Environment Variables

Create a `.env` file in the project root and define the following variables:

* `DB_USER` – your PostgreSQL username
* `DB_PASSWORD` – your PostgreSQL password

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Connecting to a Remote Server

If your PostgreSQL instance is running on another server:

1. Open `config.py`
2. Update the following values as needed:

   * `DB_HOST` (e.g. a server IP or domain)
   * `DB_PORT` (if not using the default `5432`)
   * `DB_NAME` (if your database name is different)

Make sure the PostgreSQL server allows remote connections and that your firewall settings permit access.

---

## 🗂️ Database Schema

The application uses three main tables: `users`, `accounts`, and `transactions`. Below is the SQL schema:

### Table Overview

#### Users Table

| Column | Type      | Description           |
| ------ | --------- | --------------------- |
| id     | SERIAL PK | Unique user ID        |
| name   | TEXT      | Full name of the user |
| email  | TEXT      | User email (unique)   |

#### Accounts Table

| Column  | Type       | Description             |
| ------- | ---------- | ----------------------- |
| id      | SERIAL PK  | Unique account ID       |
| user_id | INTEGER FK | References `users(id)`  |
| balance | NUMERIC    | Current account balance |

#### Transactions Table

| Column     | Type       | Description               |
| ---------- | ---------- | ------------------------- |
| id         | SERIAL PK  | Unique transaction ID     |
| account_id | INTEGER FK | References `accounts(id)` |
| amount     | NUMERIC    | Transaction amount        |
| created_at | TIMESTAMP  | Transaction timestamp     |

---

## ▶️ Running the Application

Once setup is complete, you can start the CLI banking application:

```bash
python main.py
```

Follow the on-screen prompts to manage users, accounts, and transactions.

---

## 📁 Project Structure (Example)

```
banking_system/
│
├── db/
│   ├── __init__.py
│   ├── config.py
│   ├── users.py
│   ├── accounts.py
│   └── transactions.py
│
├── services/
│   ├── __init__.py
│   └── banking_service.py
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## 📌 Notes

* Ensure your PostgreSQL service is running before starting the application
* Database credentials may need to be configured in the project settings

