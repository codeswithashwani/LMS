# Library Management System (LMS) API

---


## Authentication

* User registration
* JWT login
* JWT refresh token

## Roles

* Librarian
* Student

## Books

* Add/update/delete books (Librarian only)
* List/search/filter/order books

## Authors & Genres

* Create authors
* Create genres
* Public listing for authenticated users

## Borrow System

* Students can request books
* Librarians can approve/reject requests
* Book return workflow
* Automatic inventory management using signals

## Reviews

* Users can review books
* One review per user per book

## API Documentation

* Swagger UI
* Redoc UI

---

# Tech Stack

* Python
* Django
* Django REST Framework
* JWT Authentication
* SQLite
* drf-yasg (Swagger)

---

# Project Structure

```text
lms/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── library/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── signals.py
│   ├── urls.py
│
├── lms/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <https://github.com/codeswithashwani/LMS.git>
cd lms
```

---

## 2. Create Virtual Environment

### Windows

```bash
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv env
source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
---
## 5. Run Server

```bash
python manage.py runserver
```

---

# API Base URL

```text
http://127.0.0.1:8000/api/
```

---

# Authentication APIs

## Register

```http
POST /api/register/
```

### Request Body

```json
{
  "username": "ashwani",
  "email": "ashwani@example.com",
  "password": "test1234",
  "role": "STUDENT"
}
```

---

## Login

```http
POST /api/token/
```

### Request Body

```json
{
  "username": "ashwani",
  "password": "test1234"
}
```

---

## Refresh Token

```http
POST /api/token/refresh/
```

---

# Books APIs
## List Books

```http
GET /api/books/
```

---

## Create Book

```http
POST /api/books/
```

### Headers

```text
Authorization: Bearer access_token
```

### Request Body

```json
{
  "title": "Django REST",
  "author": 1,
  "genres": [1, 2],
  "isbn": "123456",
  "available_copies": 5,
  "total_copies": 5
}
```

---

## Search Books

```http
GET /api/books/?search=django
```

---

## Filter Books

```http
GET /api/books/?author=1
```

---

## Order Books

```http
GET /api/books/?ordering=title
```
---

# Borrow APIs

## Create Borrow Request

```http
POST /api/borrow/
```

### Request Body

```json
{
  "book": 1
}
```

---

## Approve Borrow Request

```http
PATCH /api/borrow/1/approve/
```

---

## Reject Borrow Request

```http
PATCH /api/borrow/1/reject/
```

---

## Return Book

```http
PATCH /api/borrow/1/return_book/
```

---

# Reviews APIs

## Add Review

```http
POST /api/books/1/reviews/
```

### Request Body

```json
{
  "rating": 5,
  "comment": "Excellent book"
}
```

---

## List Reviews

```http
GET /api/books/1/reviews/
```

---

# Swagger Documentation

## Swagger UI

```text
http://127.0.0.1:8000/swagger/
```

---

## Redoc

```text
http://127.0.0.1:8000/redoc/
```
---

# Author

Ashwani Sharma
`