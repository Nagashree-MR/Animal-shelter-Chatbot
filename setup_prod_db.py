# setup_prod_db.py 
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import text

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise Exception("This script is for production only. DATABASE_URL not set.")

engine = sqlalchemy.create_engine(db_url)

try:
    with engine.connect() as conn:
        print("--- Database connection successful. Starting setup... ---")
        
        # Start a transaction
        trans = conn.begin()
        
        # --- Create Users Table ---
        print("STEP 1: Creating 'users' table...")
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        '''))

        # --- Load Animal Data in Chunks ---
        print("\nSTEP 2: Loading animal data from CSV in chunks...")
        
        # Define a chunk size
        chunk_size = 10000
        
        # Use a for loop with pandas chunking ability
        for i, chunk in enumerate(pd.read_csv('austin_animal_shelter_cleaned_data.csv', chunksize=chunk_size, low_memory=False)):
            print(f"   -> Writing chunk {i+1}...")
            # Use if_exists='append'. The first chunk will create the table.
            # Clear the table beforehand to ensure a clean slate.
            if i == 0:
                # Drop the table if it exists to ensure a fresh import
                conn.execute(text('DROP TABLE IF EXISTS animal_data'))
                chunk.to_sql('animal_data', conn, if_exists='replace', index=False)
            else:
                chunk.to_sql('animal_data', conn, if_exists='append', index=False)
        
        print("... Data loading complete.")

        # --- Create Indexes for Performance ---
        print("\nSTEP 3: Creating performance indexes...")
        columns_to_index = ["Outcome Type", "Animal Type", "OutcomeYear", "Sterilization", "AgeCategory", "PrimaryBreed"]
        for column in columns_to_index:
            index_name = f"idx_animal_data_{column.replace(' ', '_')}"
            conn.execute(text(f'CREATE INDEX IF NOT EXISTS "{index_name}" ON "animal_data" ("{column}")'))
        print("... Indexes created successfully.")
        
        # Commit the transaction to save all changes
        trans.commit()
    
    print("\n--- ✅ SUCCESS: Production database setup is complete! ---")

except Exception as e:
    print(f"\n--- ❌ ERROR: An error occurred during setup. ---")
    print(e)
    # The transaction will be rolled back automatically if an error occurs.