RoozMozd is a RESTful Django backend application for single day jobs.
---

##  Features

Appending...

---

##  Requirements

Make sure you have Python 3.10+ installed. Then install dependencies:

```bash
pip install -r requirements.txt
Contents of requirements.txt:

ini
Copy
Edit
asgiref==3.9.1
Django==5.2.4
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
pillow==11.3.0
PyJWT==2.9.0
sqlparse==0.5.3
timedelta==2020.12.3
tzdata==2025.2
🚀 Getting Started
Clone the repository:

bash
Copy
Edit
git clone https://github.com/ArsalanAmiri1381/RoozMozd.git
cd RoozMozd
Create a virtual environment and activate it:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate        # Linux / MacOS
venv\Scripts\activate           # Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run migrations:

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Create a superuser (optional but recommended for admin access):

bash
Copy
Edit
python manage.py createsuperuser
Run the development server:

bash
Copy
Edit
python manage.py runserver
Visit: http://localhost:8000

 API Endpoints (Sample)
POST /api/accounts/otp/request/ → Send OTP to phone number

POST /api/accounts/otp/verify/ → Verify OTP

POST /api/accounts/register/complete/ → Complete profile after OTP

POST /api/token/ → Get JWT tokens

POST /api/token/refresh/ → Refresh JWT token

 Technologies Used
Django 5.2

Django REST Framework

SimpleJWT

SQLite (default, you can use PostgreSQL in production)

🧑‍💻 Author
Arsalan Amiri
GitHub: @ArsalanAmiri1381
