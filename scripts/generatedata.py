"""
BAYUT MARKETPLACE DATA GENERATOR
=================================
This script generates synthetic data for a 2-sided marketplace dashboard.

What it creates:
- Users (buyers, sellers, agents)
- Listings (properties for sale/rent)
- Leads (user interest in listings)
- Transactions (revenue from subscriptions)

Author: Your Name
Date: January 2026
"""


# ============================================
# STEP 1: IMPORT LIBRARIES
# ============================================
# These are tools we need to generate and store data

import pandas as pd              # For working with data tables
import numpy as np               # For mathematical operations
from faker import Faker          # For generating fake but realistic data
from datetime import datetime, timedelta  # For working with dates
import random                    # For random selections
from sqlalchemy import create_engine      # For connecting to PostgreSQL

# ============================================
# STEP 2: INITIALIZE TOOLS
# ============================================

# Create a Faker object (generates fake names, dates, etc.)
fake = Faker()

# Set random seeds for reproducibility (same data each time you run)
random.seed(42)
np.random.seed(42)

# ============================================
# STEP 3: CONFIGURATION
# ============================================
# How much data to generate (you can change these numbers)

NUM_USERS = 5000          # Total users in the system
NUM_LISTINGS = 8000       # Total property listings
NUM_LEADS = 15000         # Total lead inquiries
NUM_TRANSACTIONS = 2000   # Total paid transactions

# ============================================
# STEP 4: BUSINESS LOGIC SETUP
# ============================================

# UAE Emirates (weighted by population/market size)
EMIRATES = [
    'Dubai',           # Biggest market
    'Abu Dhabi',       # Second biggest
    'Sharjah',         # Third
    'Ajman',           # Smaller
    'Ras Al Khaimah',  # Smaller
    'Fujairah',        # Smaller
    'Umm Al Quwain'    # Smallest
]

# Property categories (what people can list)
CATEGORIES = [
    'Apartments',   # Most common
    'Villas',       # Common
    'Townhouses',   # Less common
    'Penthouses',   # Premium
    'Commercial',   # Business properties
    'Land'          # Least common
]

# Types of users in the marketplace
USER_TYPES = ['buyer', 'seller', 'agent']

# Date range for historical data (last 2 years)
START_DATE = datetime.now() - timedelta(days=730)
END_DATE = datetime.now()

print("🚀 Starting Bayut Marketplace Data Generation")
print("=" * 70)

# ============================================
# STEP 5: GENERATE USERS TABLE
# ============================================
print("\n📊 STEP 1/4: Generating Users...")

users_data = []  # Empty list to store user records

# Loop to create each user
for i in range(1, NUM_USERS + 1):
    
    # Generate random signup date within our date range
    signup_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    
    # Choose emirate (Dubai gets 40% probability, others less)
    # This simulates real market distribution
    emirate = random.choices(
        EMIRATES, 
        weights=[40, 25, 15, 5, 5, 5, 5]  # Weighted probabilities
    )[0]
    
    # Choose user type (more buyers than sellers/agents)
    user_type = random.choices(
        USER_TYPES, 
        weights=[50, 30, 20]  # 50% buyers, 30% sellers, 20% agents
    )[0]
    
    # Add this user to our list
    users_data.append({
        'user_id': i,
        'signup_date': signup_date,
        'emirate': emirate,
        'user_type': user_type
    })

# Convert list to pandas DataFrame (like an Excel table)
users_df = pd.DataFrame(users_data)
print(f"✅ Generated {len(users_df):,} users")

# ============================================
# STEP 6: GENERATE LISTINGS TABLE
# ============================================
print("\n📊 STEP 2/4: Generating Listings...")

listings_data = []

for i in range(1, NUM_LISTINGS + 1):
    
    # Each listing belongs to a user (random user_id)
    user_id = random.randint(1, NUM_USERS)
    
    # Choose property category (apartments most common)
    category = random.choices(
        CATEGORIES, 
        weights=[35, 25, 15, 10, 10, 5]
    )[0]
    
    # Choose emirate
    emirate = random.choices(
        EMIRATES, 
        weights=[40, 25, 15, 5, 5, 5, 5]
    )[0]
    
    # REALISTIC PRICING LOGIC
    # Different property types have different base prices
    base_price = {
        'Apartments': 800000,      # AED 800k average
        'Villas': 2500000,         # AED 2.5M average
        'Townhouses': 1800000,     # AED 1.8M
        'Penthouses': 5000000,     # AED 5M (premium)
        'Commercial': 1500000,     # AED 1.5M
        'Land': 1000000            # AED 1M
    }[category]
    
    # Adjust price based on emirate (Dubai is more expensive)
    emirate_multiplier = {
        'Dubai': 1.3,              # 30% more expensive
        'Abu Dhabi': 1.2,          # 20% more expensive
        'Sharjah': 0.8,            # 20% cheaper
        'Ajman': 0.6,              # 40% cheaper
        'Ras Al Khaimah': 0.7,
        'Fujairah': 0.6,
        'Umm Al Quwain': 0.5       # 50% cheaper
    }[emirate]
    
    # Final price with some randomness (±30%)
    price = base_price * emirate_multiplier * random.uniform(0.7, 1.5)
    
    # Random creation date
    created_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    
    # Listing status (most are active, some sold/expired)
    status = random.choices(
        ['active', 'sold', 'expired'], 
        weights=[60, 25, 15]  # 60% active, 25% sold, 15% expired
    )[0]
    
    listings_data.append({
        'listing_id': i,
        'user_id': user_id,
        'category': category,
        'emirate': emirate,
        'price': round(price, 2),
        'created_date': created_date,
        'status': status
    })

listings_df = pd.DataFrame(listings_data)
print(f"✅ Generated {len(listings_df):,} listings")

# ============================================
# STEP 7: GENERATE LEADS TABLE
# ============================================
print("\n📊 STEP 3/4: Generating Leads...")

leads_data = []

for i in range(1, NUM_LEADS + 1):
    
    # Pick a random listing
    listing_id = random.randint(1, NUM_LISTINGS)
    
    # Pick a random user (the interested buyer)
    user_id = random.randint(1, NUM_USERS)
    
    # IMPORTANT: Lead date must be AFTER listing was created
    # Get the listing's creation date
    listing_created = listings_df[listings_df['listing_id'] == listing_id]['created_date'].values[0]
    
    # Generate lead date (between listing creation and now)
    lead_date = fake.date_between(
        start_date=pd.to_datetime(listing_created),
        end_date=END_DATE
    )
    
    leads_data.append({
        'lead_id': i,
        'listing_id': listing_id,
        'user_id': user_id,
        'lead_date': lead_date
    })

leads_df = pd.DataFrame(leads_data)
print(f"✅ Generated {len(leads_df):,} leads")

# ============================================
# STEP 8: GENERATE TRANSACTIONS TABLE
# ============================================
print("\n📊 STEP 4/4: Generating Transactions...")

transactions_data = []

for i in range(1, NUM_TRANSACTIONS + 1):
    
    # Pick a random user who made a purchase
    user_id = random.randint(1, NUM_USERS)
    
    # Type of transaction (subscription vs featured listing)
    transaction_type = random.choices(
        ['subscription', 'featured_listing'],
        weights=[60, 40]  # 60% subscriptions, 40% featured listings
    )[0]
    
    # Amount depends on transaction type
    if transaction_type == 'subscription':
        # Different subscription tiers
        amount = random.choice([500, 1000, 2000, 5000])  # AED monthly/quarterly/annual
    else:
        # Featured listing promotion cost
        amount = random.uniform(100, 500)
    
    # Random transaction date
    transaction_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    
    transactions_data.append({
        'transaction_id': i,
        'user_id': user_id,
        'amount': round(amount, 2),
        'transaction_date': transaction_date,
        'transaction_type': transaction_type
    })

transactions_df = pd.DataFrame(transactions_data)
print(f"✅ Generated {len(transactions_df):,} transactions")

# ============================================
# STEP 9: SAVE TO CSV (BACKUP FILES)
# ============================================
print("\n💾 Saving backup CSV files...")

users_df.to_csv('users.csv', index=False)
listings_df.to_csv('listings.csv', index=False)
leads_df.to_csv('leads.csv', index=False)
transactions_df.to_csv('transactions.csv', index=False)

print("✅ CSV files saved successfully")

# ============================================
# STEP 10: LOAD TO POSTGRESQL
# ============================================
print("\n📤 Connecting to PostgreSQL and loading data...")

# ⚠️ UPDATE THESE WITH YOUR CREDENTIALS
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "bayut_marketplace"
DB_USER = "postgres"
DB_PASSWORD = "admin"

try:
    # Create database connection
    connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_string)
    
    print(f"🔌 Connecting to: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Load each table to PostgreSQL
    # if_exists='append' means add to existing data (not replace)
    
    users_df.to_sql('users', engine, if_exists='append', index=False)
    print("✅ Users table loaded")
    
    listings_df.to_sql('listings', engine, if_exists='append', index=False)
    print("✅ Listings table loaded")
    
    leads_df.to_sql('leads', engine, if_exists='append', index=False)
    print("✅ Leads table loaded")
    
    transactions_df.to_sql('transactions', engine, if_exists='append', index=False)
    print("✅ Transactions table loaded")
    
    # ============================================
    # SUCCESS MESSAGE
    # ============================================
    print("\n" + "=" * 70)
    print("🎉 SUCCESS! All data loaded to PostgreSQL")
    print("=" * 70)
    
    print("\n📊 Data Summary:")
    print(f"   Users:        {len(users_df):,} records")
    print(f"   Listings:     {len(listings_df):,} records")
    print(f"   Leads:        {len(leads_df):,} records")
    print(f"   Transactions: {len(transactions_df):,} records")
    
    print("\n📁 Files Created:")
    print("   ✅ users.csv")
    print("   ✅ listings.csv")
    print("   ✅ leads.csv")
    print("   ✅ transactions.csv")
    
    print("\n💡 Next Steps:")
    print("   1. Open pgAdmin and verify data")
    print("   2. Run SQL queries to analyze data")
    print("   3. Connect Power BI to PostgreSQL")
    print("   4. Build your dashboard!")
    
except Exception as e:
    # If something goes wrong, show the error
    print("\n" + "=" * 70)
    print("❌ Error connecting to PostgreSQL")
    print("=" * 70)
    print(f"\nError message: {str(e)}")
    
    print("\n💡 Possible issues:")
    print("   1. Wrong password - update DB_PASSWORD in the script")
    print("   2. Database doesn't exist - create 'bayut_marketplace' first")
    print("   3. PostgreSQL not running - check if service is running")
    
    print("\n✅ Good news: CSV files are still saved!")
    print("   You can import them manually into PostgreSQL")