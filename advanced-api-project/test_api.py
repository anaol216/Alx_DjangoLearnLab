"""
Simple Python script to test the API using requests library.

This script tests all CRUD operations on the Book API endpoints.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("API Testing Script")
print("=" * 60)
print("\nMake sure the Django development server is running:")
print("  python manage.py runserver")
print("\n" + "=" * 60)

def test_list_books():
    """Test GET /api/books/"""
    print("\n1. Testing GET /api/books/ (List all books)")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Found {len(books)} books")
        for book in books[:3]:  # Show first 3
            print(f"   - {book['title']} ({book['publication_year']})")
    return response

def test_get_book_detail(book_id=1):
    """Test GET /api/books/<id>/"""
    print(f"\n2. Testing GET /api/books/{book_id}/ (Get book detail)")
    response = requests.get(f"{BASE_URL}/books/{book_id}/")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        book = response.json()
        print(f"   Book: {book['title']}")
    return response

def test_create_book():
    """Test POST /api/books/create/"""
    print("\n3. Testing POST /api/books/create/ (Create new book)")
    data = {
        "title": "Test Book via API",
        "publication_year": 2023,
        "author": 1
    }
    response = requests.post(f"{BASE_URL}/books/create/", json=data)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 201:
        book = response.json()
        print(f"   Created: {book['title']} (ID: {book['id']})")
        return book['id']
    elif response.status_code == 403:
        print("   ✗ Authentication required (expected for write operations)")
    else:
        print(f"   Error: {response.json()}")
    return None

def test_update_book(book_id):
    """Test PUT /api/books/<id>/update/"""
    print(f"\n4. Testing PATCH /api/books/{book_id}/update/ (Update book)")
    data = {
        "title": "Updated Test Book"
    }
    response = requests.patch(f"{BASE_URL}/books/{book_id}/update/", json=data)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        book = response.json()
        print(f"   Updated: {book['title']}")
    elif response.status_code == 403:
        print("   ✗ Authentication required (expected for write operations)")
    return response

def test_delete_book(book_id):
    """Test DELETE /api/books/<id>/delete/"""
    print(f"\n5. Testing DELETE /api/books/{book_id}/delete/ (Delete book)")
    response = requests.delete(f"{BASE_URL}/books/{book_id}/delete/")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 204:
        print("   ✓ Book deleted successfully")
    elif response.status_code == 403:
        print("   ✗ Authentication required (expected for write operations)")
    return response

def test_filtering():
    """Test filtering functionality"""
    print("\n6. Testing Filtering (/api/books/?publication_year=1997)")
    response = requests.get(f"{BASE_URL}/books/?publication_year=1997")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Found {len(books)} books from 1997")
    return response

def test_searching():
    """Test search functionality"""
    print("\n7. Testing Search (/api/books/?search=Harry)")
    response = requests.get(f"{BASE_URL}/books/?search=Harry")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Found {len(books)} books matching 'Harry'")
    return response

if __name__ == "__main__":
    try:
        # Test read operations (should work without authentication)
        test_list_books()
        test_get_book_detail(1)
        test_filtering()
        test_searching()
        
        # Test write operations (will require authentication)
        print("\n" + "=" * 60)
        print("Testing Write Operations (Authentication Required)")
        print("=" * 60)
        new_book_id = test_create_book()
        if new_book_id:
            test_update_book(new_book_id)
            test_delete_book(new_book_id)
        
        print("\n" + "=" * 60)
        print("✓ API Testing Complete!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the server.")
        print("   Make sure Django development server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n✗ Error: {e}")
