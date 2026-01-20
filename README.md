# Parliame API Server (Django)

> Backend of [Parliame.com](https://parliame.com) (Migration is underway)

> Frontend: [@disfordave/parliame-client](https://github.com/disfordave/parliame-client)

A Django-based REST API designed to manage complex, hierarchical polling data. 
This project demonstrates scalable backend architecture, focusing on data integrity, relational modeling, and efficient backoffice tooling.

**Project Goal:** To prototype a high-concurrency data management system that can serve complex relational datasets (Country → Chamber → Poll → Result) to client applications with high reliability.

## Features

### 1. Complex Data Modeling & Integrity
Enforcing strict logical constraints at the database level:
- **Hierarchical Validation:** The `PollResult` model implements custom `clean()` logic to ensure that a Political Party can only receive votes in a Poll if they belong to the same Country.
- **Relational Consistency:** Designed a normalized schema handling `OneToMany` (Country -> Chamber) and `ManyToMany` concepts via intermediate tables.

### 2. Developer-Friendly API Design
- **Slug-Based Navigation:** utilized `SlugRelatedField` in serializers instead of raw Integer IDs. This improves readability for client developers and debugging (e.g., `/api/chambers/be-federal/` instead of `/api/chambers/5/`).
- **RESTful Architecture:** strict adherence to REST standards using Django Rest Framework's `ModelViewSet`.

### 3. Secure & Scalable Access
- **Role-Based Permissions:** Implemented custom permissions (`IsAdminOrReadOnly`) to ensure that public users can only fetch data, while only authorized Staff can modify the dataset via the Admin panel.
- **Scalable Filter System:** (If you added filters) integrated `django-filter` to allow granular queries without over-fetching data.

## Tech Stack

- **Language:** Python 3.12
- **Framework:** Django 6.0, Django REST Framework (DRF)
- **Database:** SQLite (Dev), configurable for PostgreSQL (Prod)
- **Tooling:** Ruff (Linting), pip (Dependency Management)

## Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/disfordave/parliame-django.git
   cd parliame-django
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run Migrations & Start Server**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # Create your admin account
   python manage.py runserver
   ```

## Explore the API
   * Admin Panel: http://localhost:8000/admin
   * API Root: http://localhost:8000/api/

## Testing
Run the test suite to verify data integrity rules:
`python manage.py test`
