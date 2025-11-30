# Advanced API Project - Book Management API

A comprehensive RESTful API built with Django REST Framework for managing books and authors.

## Features

- ✅ Complete CRUD operations for Book model
- ✅ Generic class-based views for efficient development
- ✅ Filtering, searching, and ordering capabilities
- ✅ Permission-based access control
- ✅ Custom validation for data integrity
- ✅ Nested serialization for related data
- ✅ Comprehensive documentation

---

## API Endpoints

### Book Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/books/` | List all books | Optional |
| GET | `/api/books/<id>/` | Get book details | Optional |
| POST | `/api/books/create/` | Create new book | Required |
| PUT/PATCH | `/api/books/update/<id>/` | Update book | Required |
| DELETE | `/api/books/delete/<id>/` | Delete book | Required |

---

## Request/Response Examples

### 1. List All Books

```http
GET /api/books/
```

**Response (200 OK):**

```json
[
    {
        "id": 1,
        "title": "Harry Potter and the Philosopher's Stone",
        "publication_year": 1997,
        "author": 1
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "publication_year": 1937,
        "author": 3
    }
]
```

### 2. Get Book Detail

```http
GET /api/books/1/
```

**Response (200 OK):**

```json
{
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
}
```

### 3. Create New Book

```http
POST /api/books/create/
Content-Type: application/json

{
    "title": "New Book Title",
    "publication_year": 2023,
    "author": 1
}
```

**Response (201 Created):**

```json
{
    "id": 6,
    "title": "New Book Title",
    "publication_year": 2023,
    "author": 1
}
```

**Error Response (400 Bad Request) - Future Year:**

```json
{
    "publication_year": [

## Filtering, Searching & Ordering

### Filter by Author
```http
GET /api/books/?author=1
```

### Filter by Publication Year

```http
GET /api/books/?publication_year=1997
```

### Filter by Title

```http
GET /api/books/?title=Harry%20Potter
```

### Search by Title or Author Name

```http
GET /api/books/?search=Rowling
```

### Order by Title

```http
GET /api/books/?ordering=title
```

### Order by Publication Year (Descending)

```http
GET /api/books/?ordering=-publication_year
```

### Combine Multiple Parameters

```http
GET /api/books/?author=1&ordering=-publication_year&search=Harry
```

---

## Permissions

The API uses two permission classes:

- **`IsAuthenticatedOrReadOnly`**: Applied to List and Detail views. Allows read-only access to unauthenticated users.
- **`IsAuthenticated`**: Applied to Create, Update, and Delete views. Strictly enforces authentication for all operations.

### Authentication Methods

1. **Session Authentication** (for browsable API)
2. **Token Authentication** (can be configured)

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install django djangorestframework django-filter
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Create Sample Data

```bash
python manage.py shell
>>> exec(open('create_sample_data.py').read())
```

### 5. Run Development Server

```bash
python manage.py runserver
```

### 6. Access the API

- **Browsable API**: <http://127.0.0.1:8000/api/books/>
- **Admin Panel**: <http://127.0.0.1:8000/admin/>

---

## Testing the API

### Using the Browsable API

1. Navigate to <http://127.0.0.1:8000/api/books/>
2. Use the built-in forms to test endpoints
3. Login via the admin panel to test write operations

### Using Django Test Suite

Run the comprehensive unit tests covering CRUD, permissions, and filtering:

```bash
python manage.py test api
```

### Using the Test Script

```bash
# First, start the server
python manage.py runserver

# In another terminal, run the test script
pip install requests
python test_api.py
```

### Using curl

```bash
# List all books
curl http://127.0.0.1:8000/api/books/

# Get book detail
curl http://127.0.0.1:8000/api/books/1/

# Create book (requires authentication)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New Book","publication_year":2023,"author":1}'
```

---

## Models

### Author Model

```python
class Author(models.Model):
    name = models.CharField(max_length=200)
```

### Book Model

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

**Relationship**: One Author can have many Books (One-to-Many)

---

## Serializers

### BookSerializer

- Serializes all Book fields
- Custom validation: `publication_year` cannot be in the future

### AuthorSerializer

- Serializes Author with nested books
- Uses `BookSerializer` for nested representation
- Read-only books field

---

## Views

All views use Django REST Framework's generic views:

| View | Base Class | Purpose |
|------|-----------|---------|
| `BookListView` | `ListAPIView` | List all books with filtering/searching |
| `BookDetailView` | `RetrieveAPIView` | Retrieve single book |
| `BookCreateView` | `CreateAPIView` | Create new book |
| `BookUpdateView` | `UpdateAPIView` | Update existing book |
| `BookDeleteView` | `DestroyAPIView` | Delete book |

### Custom Features

- **Filtering**: By author and publication_year
- **Searching**: By title
- **Ordering**: By title and publication_year
- **Permissions**:
  - `IsAuthenticatedOrReadOnly` for List and Detail views
  - `IsAuthenticated` for Create, Update, and Delete views

---

## Project Structure

```
advanced-api-project/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py          # Admin configuration
│   ├── models.py         # Author and Book models
│   ├── serializers.py    # BookSerializer and AuthorSerializer
│   ├── views.py          # Generic API views
│   └── urls.py           # API URL patterns
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
├── create_sample_data.py # Script to create test data
├── test_api.py           # API testing script
├── manage.py
└── README.md             # This file
```

---

## Validation Rules

1. **Title**: Required, max 200 characters
2. **Publication Year**:
   - Required
   - Must be an integer
   - Cannot be in the future
3. **Author**: Required, must reference existing Author

---

## Error Handling

### 400 Bad Request

Invalid data or validation errors

### 403 Forbidden

Authentication required for write operations

### 404 Not Found

Resource does not exist

### 405 Method Not Allowed

HTTP method not supported for endpoint

---

## Future Enhancements

- [ ] Pagination for large datasets
- [ ] Token-based authentication
- [ ] API versioning
- [ ] Rate limiting
- [ ] Automated tests
- [ ] API documentation with Swagger/OpenAPI
- [ ] Author CRUD endpoints

---

## License

This project is for educational purposes.
