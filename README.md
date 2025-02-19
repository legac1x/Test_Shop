# Legac1x Test Shop 🛒

Legac1x Test Shop is a learning project for an online store built using Django.
The project is designed to demonstrate working with product catalog browsing, user registration and email confirmation, authentication, and cart management.
Modern technologies such as Celery, Redis, and PostgreSQL are used.


## Main Features
```
✅ User registration and authentication
✅ Email verification for registration confirmation
✅ Adding products to the shopping cart
✅ Full-text search
✅ Caching of the product catalog using Redis
✅ Admin panel for managing products
✅ Background task support with Celery and Redis
✅ PostgreSQL as the main database
```

## Technologies used

```
🔹 Django
🔹 PostgreSQL
🔹 Redis
🔹 Celery
🔹 MPTT
🔹 Pillow
🔹 dotenv
```

## Installation

Set all the requirements using the command:

```python
pip install -r requirements.txt
```

## PostgreSQL DB

Run SQL Shell (psql) and create your database, then enter your database data in ```.env```, if you have database just enter enter your database data in ```.env```.

## Environment Variables

Create a `.env` file in the root directory and add following variables:

```python
SECRET_KEY=your_secret_key
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=your_database_host
DATABASE_PORT=your_database_port
```

## Database Migrations

Apply migrations before running the project:

```python
python manage.py migrate
```

## Running Celery and Redis

Start Redis server first:

```
redis-server
```

Start Celery worker:

```
celery -A your_project_name worker --loglevel=info
```

If your OC is windows:

```
celery -A your_project_name worker --loglevel=info --pool=eventlet
```
## Running server

To run your server enter

```python
python manage.py runserver
```

## Project Structure

```
┣ 📂 apps/
┃ ┣ 📂 accounts/ (User authentication & profiles)
┃ ┣ 📂 mysite/ (Main shop functionality)
┃ ┗ 📂 services/ (Background tasks)
┣ 📂 media/ (User-uploaded files)
┣ 📂 static/ (CSS)
┣ 📂 templates/ (HTML templates)
┣ 📜 manage.py (Django management script)
┣ 📜 .env (Environment variables)
┣ 📜 requirements.txt (Project dependencies)
```
