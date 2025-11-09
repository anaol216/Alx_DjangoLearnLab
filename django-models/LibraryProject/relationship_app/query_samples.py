from relationship_app.models import Author, Book, Library, Librarian

# 1-Query all books by a specific author hmmmmm
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name: {author_name}")

# 2-List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} Library:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")

# 3-Retrieve the librarian for a library (required line used)
def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # REQUIRED LINE
        print(f"Librarian of {library_name} Library: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to the library: {library_name}")

# Sample usage
if __name__ == "__main__":
    books_by_author("John Doe")
    books_in_library("Central Library")
    librarian_for_library("Central Library")