# Animal Shelter Analytics Dashboard & Chatbot

A Flask-based web application for analyzing data from the Austin Animal Center, featuring an interactive dashboard with dynamic charts and a chatbot for querying the dataset in natural language.

---

## Live Demo

**https://animal-analytics-dashboard-and-chatbot.onrender.com/**

---

## Showcase

Here's a look at the main analytics dashboard, which features a compact, multi-column layout with five dynamic charts.

![Main Dashboard View](Screenshots/Dashboard.png)

---
Here's how the landing page looks like!

![Landing Page](Screenshots/Landing-page1.png)
![Landing Page](Screenshots/Landing-page2.png)

---
## Key Features

*   **Secure User Authentication:** Modern, aesthetic, and secure sign-up and sign-in flows.
*   **Interactive Data Dashboard:** Visualizes key metrics with several dynamic charts including trends, distributions, and statuses.
*   **Natural Language Chatbot:** A floating widget that understands complex, combined questions (e.g., *"how many adult dogs were adopted in 2018?"*).
*   **Optimized & Deployable:** Built with a production-ready structure using a cloud database (PostgreSQL) and optimized with database indexes for fast query performance.

---

## More Screenshots

<table>
  <tr>
    <td align="left"><strong>AI-Powered Chatbot Examples</strong></td>
  </tr>
  <tr>
    <td><img src="Screenshots/Chat1.png" alt="Chatbot Demo 1" width="46%"></td>
    <td><img src="Screenshots/Chat2.png" alt="Chatbot Demo 2" width="50%"></td>
  </tr>
  <tr>
    <td align="left"><strong>Sign-Up Form</strong></td>
    <td align="left"><strong>Sign-In Form</strong></td>
  </tr>
    <tr>
    <td><img src="Screenshots/CreateAcct.png" alt="Sign In Page" width="40%"></td>
    <td><img src="Screenshots/Login.png" alt="Sign Up Page" width="50%"></td>
  </tr>
</table>

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
