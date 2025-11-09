from models import Author, Book, Library, Librarian

def sample_queries():
    my_author = Author.objects.create(name="George Orwell")
    my_book = Book.objects.create(title="1984", author=my_author)
    my_library = Library.objects.create(name="City Library")
    my_library.books.add(my_book)
    my_librarian = Librarian.objects.create(name="Alice", library=my_library)

    # Fetch all books by a specific author`
    books_by_orwell = Book.objects.filter(author__name="George Orwell")
    print("Books by George Orwell:", books_by_orwell)

    # Fetch all books in a specific library
    books_in_city_library = my_library.books.all()
    print("Books in City Library:", books_in_city_library)
    # Fetch the librarian of a specific librarian
    librarian_of_city_library = my_library.librarian
    print("Librarian of City Library:", librarian_of_city_library.name)