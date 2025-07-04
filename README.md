

![Screenshot (88)](https://github.com/user-attachments/assets/4c51d29b-4b46-4325-93d4-b29d81c6c405)


![Screenshot (89)](https://github.com/user-attachments/assets/c5323312-eb83-47a0-b3b6-1f09de61be9d)



![Screenshot (90)](https://github.com/user-attachments/assets/889c7137-0d99-489a-9eb1-17ac9785f7ad)


# 💸 Expenses Management System

A full-featured Django-based web application that helps users track and manage their personal **expenses** and **income** efficiently, with smart reporting tools and intuitive visual insights.

---

## 🌟 Features

✅ **User Authentication**
- Register, Login, Logout
- Email activation upon registration
- Password reset via email

✅ **Expense & Income Tracking**
- Full **CRUD** (Create, Read, Update, Delete) for Expenses and Income
- Categorize records by type, amount, and source

✅ **Search & Filter**
- Search functionality for both expenses and income
- Filter by date, category, or keyword

✅ **Currency Management**
- Choose and update your preferred currency for reports and entries

✅ **Export Reports**
- Download financial reports in **Excel**, **CSV**, and **PDF** formats

✅ **Data Visualization**
- Interactive **bar charts** showing summaries for the last 6 months
- View both **income** and **expense** category statistics

✅ **Security**
- Email confirmation to activate account
- Password reset with secure email token
- CSRF-protected forms and authentication

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap, HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Authentication**: Django's built-in auth with email confirmation
- **PDF Generation**: WeasyPrint / xhtml2pdf (or similar)
- **Email Services**: SMTP (Gmail or any configured provider)
- **Data Export**: Pandas, ReportLab (or equivalent)
- **Database**: SQLite (default), PostgreSQL ready

---

## 🚀 Getting Started

### 📦 Prerequisites

Make sure you have installed:
- Python 3.8+
- pip
- virtualenv (optional but recommended)

### 🖥️ Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/chancy-gondwe/Expenses-Tracking-System.git

# 2. Navigate to the project directory
cd Expenses-Tracking-System

# 3. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (admin)
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
http://127.0.0.1:8000

