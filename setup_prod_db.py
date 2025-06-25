# setup_prod_db.py
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import text

# This script will automatically read the DATABASE_URL from the Render environment
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise Exception("This script is for production only. DATABASE_URL not set.")

# Connect to the cloud database
engine = sqlalchemy.create_engine(db_url)
with engine.connect() as conn:
    print("Connection to cloud database successful.")

    # --- Create Users Table (for PostgreSQL) ---
    print("Creating users table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    '''))
    conn.commit()

    # --- Load Animal Data ---
    print("Loading animal data from CSV...")
    df = pd.read_csv('austin_animal_shelter_cleaned_data.csv', low_memory=False)

    print(f"Writing {len(df)} rows to the animal_data table... (This may take a few minutes)")
    df.to_sql('animal_data', conn, if_exists='replace', index=False)
    print("Data loading complete.")
    conn.commit()

    # --- Create Indexes for Performance ---
    print("Creating indexes...")
    columns_to_index = ["Outcome Type", "Animal Type", "OutcomeYear", "Sterilization", "AgeCategory", "PrimaryBreed"]
    for column in columns_to_index:
        # Use a transaction-safe method for creating indexes
        index_name = f"idx_animal_data_{column.replace(' ', '_')}"
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS "{index_name}" ON "animal_data" ("{column}")'))
    print("Indexes created.")
    conn.commit()

print("\nProduction database setup is complete!")