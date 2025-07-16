💸 Finance Tracker App
A personal finance tracking web application built with Django. Users can register, log in, add income and expenses, view dashboards with visual analytics, and download their transaction history as a PDF.

🚀 Features
✅ User Registration & Login (Session-based auth)

💰 Add Income & Expenses with categories

📊 Dashboard with:

Total Income

Total Expenses

Available Balance

Last 5 Transactions

📈 Analytics:

Pie chart of expense distribution by category

Line chart comparing monthly income vs expenses

🧾 Full transaction history in tabular format

🖨️ PDF export of full transaction history

🌐 Responsive UI with Bootstrap 5

📸 Screenshots
<img width="1915" height="862" alt="image" src="https://github.com/user-attachments/assets/b7979daa-c391-4ad1-b99c-4b0cfe3f0fc8" />
<img width="1919" height="878" alt="image" src="https://github.com/user-attachments/assets/72f4dca1-6a09-4e32-b92d-8f47773db45a" />
<img width="1909" height="865" alt="image" src="https://github.com/user-attachments/assets/348a78c7-ba4b-4b63-84a8-a0ffc6ed3069" />



🛠️ Tech Stack
Backend: Django, PostgreSQL

Frontend: HTML, CSS, Bootstrap 5, Chart.js

PDF Generation: ReportLab

Session Management: Django sessions

📦 Installation
bash
Copy
Edit
git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate on Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Then open http://127.0.0.1:8000/ in your browser.

