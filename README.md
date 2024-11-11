# Library Management API with Django and DRF 📚

This project is a backend API for managing a library system, built with Django and Django REST Framework (DRF). It supports user authentication, role-based access, and CRUD operations for books. Members can view and borrow available books, while admins can manage the library's book collection and access library statistics via a dedicated dashboard.

## Table of Contents
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Key Features

1. **Authentication and Authorization**
   - **JWT Authentication**: Secure login via JSON Web Tokens.
   - **Role-Based Access Control**:
     - **Admin**: Full access to manage books and view the library dashboard.
     - **Member**: Access to view and borrow books, and to view personal borrowing details.

2. **Book Management (Admin Only)**
   - **CRUD Operations**: 
     - **Create**: Add books to the library.
     - **Read**: View details of all books.
     - **Update**: Modify book information, including availability.
     - **Delete**: Remove books from the library.

3. **Book Borrowing and Returning (Members Only)**
   - **Borrowing**: Members can borrow books if available and track return deadlines.
   - **Returning**: Return books and automatically calculate overdue fines.
   - **Borrowing Limits**: Each member can borrow up to a set limit (e.g., 5 books).
   - **Overdue Fines**: Automatically calculates fines for late returns (e.g., 5 BDT/day).

4. **Admin Dashboard**
   - **/admin-dashboard/**: Provides library stats and a list of borrowed books, grouped by user with total fines for each user.

5. **Member-Specific Borrowing Details**
   - **/borrowed-books/**: Allows each member to view their currently borrowed books, return deadlines, and any fines due.

## Technology Stack

- **Django**: Core backend framework.
- **Django REST Framework (DRF)**: Provides powerful API features and tools.
- **JWT**: Secure token-based authentication for accessing API endpoints.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/library-management-api.git
cd library-management-api
```

### 2. Set Up a Virtual Environment and Install Dependencies

```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following keys:

```
SECRET_KEY=your_django_secret_key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)

You have two options to create an admin user:

#### Option 1: Using Django’s Built-in Superuser Command

Run the following command and follow the prompts to create a superuser:

```bash
python3 manage.py createsuperuser
```

#### Option 2: Using the Custom Admin Creation Command(Recommended)

Alternatively, you can create an admin user with a single command by specifying the username, email, and password:

```bash
python3 manage.py create_admin <username> <email> <password>
```

Replace `<username>`, `<email>`, and `<password>` with your desired credentials. This command automatically assigns the admin role to the new user.
 

### 6. Run the Server

```bash
python manage.py runserver
```

The server will be accessible at `http://127.0.0.1:8000/`.

## Project Structure

- **User Management**: Role-based access (Admin and Member).
- **Book Management**: CRUD operations for admins, borrowing functionality for members.
- **Admin Dashboard**: Displays total users, books, available books, and a detailed list of borrowed books by user.
- **Borrowing System**: Manages borrowing limits, return deadlines, and fine calculations.

## API Endpoints

### Authentication Endpoints
- **POST** `/register/` – Register a new user.
- **POST** `/login/` – Log in and obtain a JWT token.

### Admin-Only Endpoints
- **GET** `/admin-dashboard/` – View overall library statistics and borrowed book details by user.
- **POST** `/books/` – Add a new book.
- **PUT** `/books/{id}/` – Update book details.
- **DELETE** `/books/{id}/` – Delete a book.

### Member-Specific Endpoints
- **GET** `/my-borrowed-books/` – View a member's current borrowed books and fines.
- **GET** `/books/available/` – View a list of available books for borrowing.

### General Endpoints (Accessible by All Authenticated Users)
- **GET** `/books/` – View all books.
- **GET** `/books/{title}/` – View details of a specific book.
- **POST** `/books/{title}/borrow/` – Borrow a book.
- **POST** `/books/{title}/return/` – Return a borrowed book.

## Usage

1. **Register or Login**: Register as a new user, or log in to obtain a JWT token.
2. **Authenticate Requests**: Use the JWT token in the `Authorization` header for accessing authenticated endpoints.
3. **Admin Tasks**: Admins can access `/admin-dashboard/` and perform CRUD operations on books.
4. **Member Tasks**: Members can view available books, borrow and return books, and check their borrowed books and fines at `/my-borrowed-books/`.

### Sample Request (Using CURL)

#### 1. Log in to Get a JWT Token
```bash
curl -X POST http://127.0.0.1:8000/login/ -d "username=myuser&password=mypassword"
```

#### 2. Use the Token to View Available Books
```bash
curl -H "Authorization: Bearer <your_jwt_access_token>" http://127.0.0.1:8000/books/available/
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
