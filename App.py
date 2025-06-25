from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import re
import math
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlalchemy
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = '!@#$%^&*()_+='

basedir = os.path.abspath(os.path.dirname(__file__))
ANIMAL_TABLE_NAME = 'animal_data' 

def get_engine():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        db_url = f"sqlite:///{os.path.join(basedir, 'users.db')}"
    return sqlalchemy.create_engine(db_url)

# --- User Authentication Routes (already SQLAlchemy compliant) ---
@app.route('/')
def index(): return render_template('index07.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name, last_name, email, password = request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password']
        if request.form['password'] != request.form['confirm_password']:
            flash('Passwords do not match', 'danger'); return redirect(url_for('sign_up'))
        hashed_password = generate_password_hash(password)
        engine = get_engine()
        try:
            with engine.connect() as conn:
                query = text("INSERT INTO users (first_name, last_name, email, password) VALUES (:fn, :ln, :email, :pwd)")
                conn.execute(query, {"fn": first_name, "ln": last_name, "email": email, "pwd": hashed_password})
                conn.commit()
        except Exception:
            flash('Email already registered.', 'danger'); return redirect(url_for('sign_up'))
        flash('Sign up successful! Please sign in.', 'success')
        return redirect(url_for('sign_in'))
    return render_template('sign_up07.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        engine = get_engine()
        with engine.connect() as conn:
            query = text("SELECT * FROM users WHERE email = :email")
            result = conn.execute(query, {"email": email}).fetchone()
        if result and check_password_hash(result.password, password):
            session['user_id'] = result.id
            return redirect(url_for('dashboard')) 
        else:
            flash('Invalid credentials', 'danger')
    return render_template('sign_in07.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('sign_in'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('sign_in'))
    return render_template('dashboard.html')

# --- API Routes - All queries are now explicitly case-sensitive using quotes ---
@app.route('/api/outcome-summary')
def outcome_summary():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    engine = get_engine()
    with engine.connect() as conn:
        query = text(f'SELECT "Outcome Type" as outcome_type, COUNT(*) as count FROM {ANIMAL_TABLE_NAME} GROUP BY "Outcome Type" ORDER BY count DESC')
        results = conn.execute(query).mappings().all()
    return jsonify({"labels": [row['outcome_type'] for row in results], "data": [row['count'] for row in results]})

@app.route('/api/animal-types')
def animal_types():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    engine = get_engine()
    with engine.connect() as conn:
        query = text('SELECT "Animal Type", COUNT(*) as count FROM animal_data GROUP BY "Animal Type" ORDER BY count DESC LIMIT 5')
        results = conn.execute(query).mappings().all()
    return jsonify({"labels": [row['Animal Type'] for row in results], "data": [row['count'] for row in results]})

@app.route('/api/adoptions-by-year')
def adoptions_by_year():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    engine = get_engine()
    with engine.connect() as conn:
        query = text('SELECT "OutcomeYear" as year, COUNT(*) as count FROM animal_data WHERE "Outcome Type" = \'Adoption\' AND "OutcomeYear" IS NOT NULL GROUP BY "OutcomeYear" ORDER BY "OutcomeYear"')
        results = conn.execute(query).mappings().all()
    labels = [str(row['year']) for row in results]
    data = [row['count'] for row in results]
    max_val = 0
    if data: max_val = math.ceil((max(data) + 1000) / 1000) * 1000
    return jsonify({"labels": labels, "data": data, "maxValue": max_val})

@app.route('/api/sterilization-summary')
def sterilization_summary():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    engine = get_engine()
    with engine.connect() as conn:
        query = text('SELECT "Sterilization", COUNT(*) as count FROM animal_data WHERE "Sterilization" != \'Unknown\' GROUP BY "Sterilization"')
        results = conn.execute(query).mappings().all()
    return jsonify({"labels": [row['Sterilization'] for row in results], "data": [row['count'] for row in results]})

@app.route('/api/age-demographics')
def age_demographics():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    engine = get_engine()
    with engine.connect() as conn:
        query = text('SELECT "AgeCategory", COUNT(*) as count FROM animal_data GROUP BY "AgeCategory" ORDER BY count DESC LIMIT 5')
        results = conn.execute(query).mappings().all()
    return jsonify({"labels": [row['AgeCategory'] for row in results], "data": [row['count'] for row in results]})

# --- Chatbot API Route  ---
@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    user_message = request.json['message'].lower()
    engine = get_engine()
    with engine.connect() as conn:
        
        parsing_order = [
            ("Outcome Type", { "adoption": "Adoption", "adopted": "Adoption", "transfer": "Transfer", "transferred": "Transfer", "return to owner": "Return to Owner", "rto": "Return to Owner", "euthanasia": "Euthanasia", "euthanized": "Euthanasia", "euthanised": "Euthanasia", "died": "Died", "rto-adopt": "Rto-Adopt", "disposal": "Disposal", "missing": "Missing", "relocate": "Relocate", "relocated": "Relocate", "stolen": "Stolen", "lost": "Lost" }),
            ("Sterilization", { "sterilized": "Sterilized", "neutered": "Sterilized", "spayed": "Sterilized", "intact": "Intact" }),
            ("AgeCategory", { "adult": "Adult", "adults": "Adult", "young": "Young", "puppy": "Puppy/Kitten", "puppies": "Puppy/Kitten", "kitten": "Puppy/Kitten", "kittens": "Puppy/Kitten", "baby": "Puppy/Kitten", "senior": "Senior", "seniors": "Senior", "old": "Senior" }),
            ("Animal Type", { "dog": "Dog", "dogs": "Dog", "cat": "Cat", "cats": "Cat", "bird": "Bird", "birds": "Bird", "other": "Other" }),
        ]
        action = "list"
        if "how many" in user_message or "count" in user_message or "total" in user_message: action = "count"
        params = {}
        where_clauses = []
        description_parts = []
        def find_keyword(text, keyword): return re.search(r'\b' + re.escape(keyword) + r'\b', text)
        for i, (db_column, keywords_map) in enumerate(parsing_order):
            for keyword, db_value in keywords_map.items():
                if find_keyword(user_message, keyword):
                    param_name = f"p{i}"
                    where_clauses.append(f'"{db_column}" = :{param_name}')
                    params[param_name] = db_value
                    description_parts.append(keyword)
                    break
        year_match = re.search(r'\b(20\d{2})\b', user_message)
        if year_match:
            where_clauses.append('"OutcomeYear" = :year')
            params["year"] = year_match.group(1)
            description_parts.append(f"in {year_match.group(1)}")
        response_text = "I'm sorry, I couldn't understand that."
        if where_clauses:
            query_filter_string = " AND ".join(where_clauses)
            description = ' '.join(description_parts)
            if action == "count":
                sql = text(f'SELECT COUNT(*) FROM animal_data WHERE {query_filter_string}')
                count = conn.execute(sql, params).scalar()
                response_text = f"There are {count} {description} in the dataset."
            elif action == "list":
                sql = text(f'SELECT Name, "PrimaryBreed" FROM animal_data WHERE {query_filter_string} AND Name IS NOT \'Unknown\' LIMIT 5')
                results = conn.execute(sql, params).mappings().all()
                if results:
                    response_text = f"Here are the first 5 {description} I found: "
                    animals_info = [f"{row['Name']} (a {row['PrimaryBreed']})" for row in results]
                    response_text += ", ".join(animals_info) + "."
                else:
                    response_text = f"Sorry, I couldn't find any {description}."
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)