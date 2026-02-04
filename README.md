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

## Installation

1. Clone the repository
2. Navigate into project folder
3. Install dependencies (if any)

```bash
git clone https://github.com/CrazyHayz02/Bank_CLI_SQL
cd Bank_CLI_SQL
pip install -r requirements.txt
python main.py
```
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

### Example
```bash
=== Bank System Menu ===
1. Create user
2. Create account
3. Deposit
4. Withdraw
5. Check balance
6. List transactions
7. Transfers
0. Exit

Select an option: 1
Enter name: James
Enter email: james@test.com

User created with ID: 1
```

---

💡 Indexes

To improve performance on common queries and joins, you have the following indexes in the `.sql` files, or you could add them yourself:

```
-- Users table
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Accounts table
CREATE INDEX idx_accounts_user_id ON accounts(user_id);

-- Transactions table
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_account_created_at ON transactions(account_id, created_at DESC);
```
⚡ These indexes are especially useful for:
- Looking up users by email
- Retrieving all accounts for a specific user
- Retrieving transactions for an account, sorted by most recent

---

## 🛠️ Index Maintenance (Optional)

To keep queries fast, especially on the `transactions` table, you may occasionally **rebuild or refresh indexes**:

```sql
-- Rebuild all indexes on a table
REINDEX TABLE transactions;

-- Update table statistics for the query planner
ANALYZE transactions;
```
💡 Tips:

- Do this after large inserts, updates, or deletes
- For high-activity tables, consider weekly maintenance
- For smaller tables like users or accounts, monthly is usually enough

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
│   ├── exceptions.py
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

