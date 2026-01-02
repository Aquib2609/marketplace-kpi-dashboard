-- ============================================
-- BAYUT MARKETPLACE DATABASE SCHEMA
-- ============================================

-- Drop tables if they exist (for clean slate)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS leads CASCADE;
DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    signup_date DATE NOT NULL,
    emirate VARCHAR(50) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('buyer', 'seller', 'agent'))
);

-- Create listings table
CREATE TABLE listings (
    listing_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    emirate VARCHAR(50) NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    created_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'sold', 'expired')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create leads table
CREATE TABLE leads (
    lead_id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL,
    user_id INT NOT NULL,
    lead_date DATE NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('subscription', 'featured_listing')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_users_signup_date ON users(signup_date);
CREATE INDEX idx_users_emirate ON users(emirate);
CREATE INDEX idx_listings_created_date ON listings(created_date);
CREATE INDEX idx_listings_emirate ON listings(emirate);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_leads_lead_date ON leads(lead_date);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);

-- Verify tables created
SELECT 
    table_name, 
    table_type
FROM 
    information_schema.tables
WHERE 
    table_schema = 'public'
ORDER BY 
    table_name;

--show users table
select * fr

