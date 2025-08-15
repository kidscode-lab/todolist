# To-Do List Web App

A simple **Flask** + **SQLite** web application for managing tasks.  
Supports adding, marking as done, and deleting tasks, with separation by **class code** and **student ID**.

## Features

- **Add** new tasks with a title and due date
- **Mark** tasks as completed
- **Delete** tasks
- **Separate task lists** per `class_code` and `student_id`
- **Responsive** HTML/CSS front-end
- API-style structure for easy integration with other systems
- Deployable to **Azure App Service** (Linux)

---

## Project Structure

.
├── app.py # Main Flask app
├── storage.py # Task storage (SQLite)
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # Main web UI template
└── static/
├── styles.css # UI styles
└── script.js # UI behavior

---

## Installation (Local)

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   Create & activate virtual environment
   ```

python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows

Install dependencies

pip install -r requirements.txt

Run locally

flask run

Visit: http://127.0.0.1:5000/?class_code=demo&student_id=student1

Deployment to Azure App Service (Linux)

Prerequisites

Azure CLI installed

Azure account

Azure App Service Plan (Linux)

Azure Web App created

Gunicorn startup command

In Azure Portal → Web App → Configuration → General Settings → Startup Command:

gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT} app:app

Deploy via VS Code Azure extension

Install Azure App Service extension in VS Code

Right-click your project folder → Deploy to Web App

Select your target Web App

Check your app

Visit https://<your-app-name>.azurewebsites.net

Ensure query parameters are provided:

https://<your-app-name>.azurewebsites.net/?class_code=demo&student_id=student1

API Endpoints
Method Endpoint Description
GET / HTML front-end (requires class_code & student_id in query)
POST /add Add a new task
GET /done/<task_id> Mark task as completed
GET /delete/<task_id> Delete task
GET /api/health Health check (optional endpoint)
Environment Variables
Variable Description Example
PORT Port for Gunicorn in Azure 8000
Notes

class_code and student_id are required to separate tasks per group/user.

If not provided in the URL, defaults are used (demo, student1).

For production, use persistent storage (PostgreSQL, MySQL, etc.) instead of SQLite.

License

MIT License
