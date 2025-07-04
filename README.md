

![Screenshot (85)](https://github.com/user-attachments/assets/d0f34320-0e74-498b-be13-d142137f246c)


![Screenshot (89)](https://github.com/user-attachments/assets/7eb07ff4-c4a7-425d-81bf-433595122527)

![Screenshot (90)](https://github.com/user-attachments/assets/89a02e5e-bf84-45aa-acba-4edfe6b146cd)


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
