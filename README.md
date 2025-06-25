# Animal Shelter Analytics Dashboard & Chatbot

A Flask-based web application for analyzing data from the Austin Animal Center, featuring an interactive dashboard with dynamic charts and a chatbot for querying the dataset in natural language.

---

## Live Demo

**(This link will be added after deployment on Render)**

---

## Key Features

*   **Secure User Authentication:** Users can sign up and sign in to access the dashboard.
*   **Interactive Data Dashboard:** Visualizes key metrics with several charts:
    *   Adoptions by Year
    *   Sterilization Status
    *   Top 5 Animal Types
    *   Top 5 Age Demographics
    *   Overall Outcomes by Type
*   **Natural Language Chatbot:**
    *   Understands complex, combined questions (e.g., "how many adult dogs were adopted in 2018?").
    *   Handles questions about specific breeds not explicitly programmed in its vocabulary.
*   **Optimized & Deployable:** Built with a production-ready structure using a cloud database (PostgreSQL) and optimized with database indexes for fast query performance.

---

## Technology Stack

*   **Backend:** Python, Flask, SQLAlchemy
*   **Database:** PostgreSQL (for production), SQLite (for local development)
*   **Frontend:** HTML, CSS, JavaScript
*   **Data Visualization:** Chart.js
*   **Deployment:** Render, Gunicorn

---

## How to Run Locally

To set up and run this project on your local machine, follow these steps.

**Prerequisites:**
*   Python 3 & Git
*   An Anaconda distribution is recommended.

**1. Clone the repository:**
```bash
git clone https://github.com/Nagashree-MR/Animal-shelter-Chatbot.git
cd Animal-shelter-Chatbot
