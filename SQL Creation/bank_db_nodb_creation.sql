-- Connect to the database
\c bank_db;

-- =========================================
-- USERS TABLE
-- Stores basic user information
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- =========================================
-- ACCOUNTS TABLE
-- Stores account info for each user
-- =========================================
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    balance NUMERIC CHECK (balance >= 0) DEFAULT 0
);

-- =========================================
-- TRANSACTIONS TABLE
-- Tracks deposits/withdrawals
-- =========================================
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    amount NUMERIC NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- Create Indexes for Performance
-- =========================================
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account_created_at ON transactions(account_id, created_at DESC);
