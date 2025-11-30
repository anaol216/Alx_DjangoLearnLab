# Create sample data using Django shell
from api.models import Author, Book

# Create authors
author1, _ = Author.objects.get_or_create(name="J.K. Rowling")
author2, _ = Author.objects.get_or_create(name="George R.R. Martin")
author3, _ = Author.objects.get_or_create(name="J.R.R. Tolkien")

# Create books
Book.objects.get_or_create(
    title="Harry Potter and the Philosopher's Stone",
    defaults={'publication_year': 1997, 'author': author1}
)
Book.objects.get_or_create(
    title="Harry Potter and the Chamber of Secrets",
    defaults={'publication_year': 1998, 'author': author1}
)
Book.objects.get_or_create(
    title="A Game of Thrones",
    defaults={'publication_year': 1996, 'author': author2}
)
Book.objects.get_or_create(
    title="The Hobbit",
    defaults={'publication_year': 1937, 'author': author3}
)
Book.objects.get_or_create(
    title="The Lord of the Rings",
    defaults={'publication_year': 1954, 'author': author3}
)

print(f"Created {Author.objects.count()} authors and {Book.objects.count()} books")
