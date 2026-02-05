# Mini-Detail-Library-App

📘 Mini Detail Library — Assignment Submission
Overview

This project demonstrates PostgreSQL Row-Level Security (RLS) using Supabase and FastAPI.
Access to architectural detail records is restricted based on user roles and ownership.

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone <repo_url>
cd mini-detail-library-app

2️⃣ Install Backend Dependencies
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Environment Configuration

Create .env

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key


4️⃣ Run Backend
uvicorn main:app --reload

Open API docs:

http://127.0.0.1:8000/docs

🔐 How to Switch Users / Roles

RLS testing uses request headers:

x-role: architect
x-user-id: 22222222-2222-2222-2222-222222222222
Admin Example
x-role: admin
x-user-id: any_value
Call endpoint:

GET /secure/details
Different headers return different rows based on policy.

🛡️ RLS Policy Explanation

Row-Level Security is enabled on the details table to enforce database-level access control.

Admin Policy

Admins can view all records.

current_setting('app.role', true) = 'admin'

Architect Standard Policy

Architects can view shared standard details.

role = architect AND source = standard


Architect Ownership Policy

Architects can view project details created by themselves.

role = architect
AND source = user_project
AND user_id matches header identity


🧠 Security Design Principle

The application does not filter records in Python.
All access control is enforced by PostgreSQL policies, ensuring separation between application logic and database security.
