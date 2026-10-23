
---

```markdown
# 🚀 TaskSphere

**TaskSphere** is a robust, role-secured full-stack project management and task-tracking application built with Django, Django REST Framework (DRF), MySQL, and Tailwind CSS. It is designed to streamline collaboration between administrators, project managers, and team members with granular role-based access control and asynchronous updates.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django, Django REST Framework (DRF)
* **Database:** MySQL
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (`fetch` API)
* **Version Control:** Git

---

## 📋 Key Features

* **Multi-Tier Role-Based Access Control (RBAC):**
  * **Admin / Project Manager:** Full privileges to create/delete projects, add and edit tasks, and assign tasks to specific team members.
  * **Team Member:** Secure, filtered views displaying only the projects and tasks explicitly assigned to them.
* **Full CRUD Operations:** Complete server-side and API-driven create, read, update, and delete flows for projects and tasks.
* **Asynchronous Status Tracking:** Real-time task status updates (*To Do*, *In Progress*, *Done*) handled asynchronously via JavaScript fetch requests without full page reloads.
* **Granular Task Assignment:** Project managers can select and assign team members directly from a dynamic dropdown list.
* **Robust Error Handling:** Form validation feedback and database transaction error catching built into both views and API endpoints.

---

## 📁 Project Structure


tasksphere/
│
├── core/                  # Django project configuration (settings, URLs, wsgi)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/              # Custom user authentication and roles model
│   ├── models.py
│   ├── forms.py
│   └── views.py
│
├── tracker/               # Core project and task management app
│   ├── models.py          # Project and Task models
│   ├── serializers.py     # DRF Serializers
│   ├── views.py           # Template CRUD views & DRF ViewSets
│   └── urls.py
│
├── templates/             # HTML templates styled with Tailwind CSS
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_project.html
│   ├── create_task.html
│   └── update_task.html
│
├── manage.py              # Django project manager script
└── requirements.txt       # Project dependencies

```

---

## ⚙️ Getting Started & Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/tasksphere.git](https://github.com/your-username/tasksphere.git)
cd tasksphere

```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install django djangorestframework mysqlclient

```

### 4. Configure the MySQL Database

1. Open your MySQL client (MySQL Workbench or terminal) and create the database:
```sql
CREATE DATABASE tasksphere_db;

```


2. Update your database settings in `core/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tasksphere_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```



### 5. Run Database Migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations tracker
python manage.py migrate

```

### 6. Create a Superuser / Admin Account

```bash
python manage.py createsuperuser

```

### 7. Run the Development Server

```bash
python manage.py runserver

```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🔌 API Endpoints (DRF Router)

TaskSphere includes a built-in REST API powered by Django REST Framework:

* **Projects API:** `http://127.0.0.1:8000/api/projects/` (Supports CRUD operations with role permissions)
* **Tasks API:** `http://127.0.0.1:8000/api/tasks/` (Supports status updates and tracking)

---


```
