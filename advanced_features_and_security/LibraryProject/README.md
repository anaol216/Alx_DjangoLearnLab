## **Django Development Environment Setup**

This task is the essential starting point for your Django journey. The objective is to **set up a working Django development environment** and create the foundation of your project, which will be named **`LibraryProject`**.

-----

### 🎯 Objective

To gain familiarity with Django by setting up the development environment, creating a basic Django project (`LibraryProject`), and understanding the initial project structure and workflow.

### 📝 Task Description

You will install Django, create a new project, run the built-in development server, and explore the core configuration files that make up a Django project. This initial setup is crucial for all subsequent development.

### 🛠️ Prerequisites

  * **Python:** Ensure Python is installed on your system (Python 3.x is recommended).
  * **pip:** The Python package installer, which usually comes bundled with Python.

-----

### ➡️ Steps

Follow these steps to complete the setup and run your first Django server:

#### 1\. Install Django

Use `pip` to install the Django framework globally or, preferably, within a virtual environment (though not strictly required for this initial step).

```bash
# Install Django using pip
pip install django
```

#### 2\. Create Your Django Project

Use the `django-admin` command-line utility to scaffold a new project named `LibraryProject`.

```bash
# Create the project structure
django-admin startproject LibraryProject
```

#### 3\. Navigate and Create README

Move into the newly created project directory and create this `README.md` file within it.

```bash
# Change directory into the project folder
cd LibraryProject

# (Assuming you are creating this README.md file now)
touch README.md
```

#### 4\. Run the Development Server

The `manage.py` file is a command-line utility for interacting with your Django project. Use it to start the development server.

```bash
# Start the development server
python manage.py runserver
```

#### 5\. Verify Installation

Once the server is running, open your web browser and navigate to the specified address:

  * **URL:** `http://127.0.0.1:8000/`

You should see the default **"The install worked successfully\! Congratulations\!"** Django welcome page.

-----

### 📂 Explore the Project Structure

After running `django-admin startproject LibraryProject`, the following structure is created. Familiarize yourself with these core components:

```
LibraryProject/
├── manage.py
└── LibraryProject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

| File/Directory | Role |
| :--- | :--- |
| **`manage.py`** | A command-line utility for administering your Django project (e.g., running the server, migrations, or tests). |
| **`LibraryProject/`** (Inner Dir) | The actual Python package for your project. Its name is the Python import path used to import things inside of it (e.g., `LibraryProject.settings`). |
| **`settings.py`** | **Configuration** for your entire Django project. This includes database settings, installed apps, middleware, and static file locations. |
| **`urls.py`** | The **URL declarations** for this Django project. This acts as the "table of contents" for your site, mapping URLs to views (functions/classes that handle requests). |
| **`wsgi.py`** | An entry point for **WSGI** (Web Server Gateway Interface) compatible web servers to serve your project. |

-----

### 📍 Repository Details

  * **GitHub Repository:** `Alx_DjangoLearnLab`
  * **Directory for this Task:** `Introduction_to_Django`

---

## 🔐 **Permissions and Groups Configuration**

This project implements a comprehensive permission-based access control system for managing books in the library system.

### 📋 **Custom Permissions**

The `Book` model in `bookshelf/models.py` defines four custom permissions:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]
```

**Permission Codes:**
- `bookshelf.can_view` - Allows users to view book lists and details
- `bookshelf.can_create` - Allows users to create new books
- `bookshelf.can_edit` - Allows users to edit existing books
- `bookshelf.can_delete` - Allows users to delete books

### 👥 **User Groups**

The project includes a management command that automatically creates three user groups with predefined permissions:

#### **1. Viewers Group**
- **Permissions:** `can_view`
- **Access Level:** Read-only access to books
- **Use Case:** Regular library members who can browse the catalog

#### **2. Editors Group**
- **Permissions:** `can_view`, `can_create`, `can_edit`
- **Access Level:** Can view, create, and edit books (but cannot delete)
- **Use Case:** Librarians who manage the book collection

#### **3. Admins Group**
- **Permissions:** `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access Level:** Full CRUD access to all books
- **Use Case:** Library administrators with complete control

### 🚀 **Setting Up Groups**

Run the management command to create and configure groups:

```bash
python manage.py setup_groups
```

This command will:
1. Create the three groups (Viewers, Editors, Admins) if they don't exist
2. Assign appropriate permissions to each group
3. Display a summary of created/updated groups

**Output Example:**
```
✓ Created group: Viewers
  ✓ Assigned permissions to Viewers: can_view
✓ Created group: Editors
  ✓ Assigned permissions to Editors: can_create, can_edit, can_view
✓ Created group: Admins
  ✓ Assigned permissions to Admins: can_view, can_create, can_edit, can_delete

✓ Groups setup completed successfully!
```

### 🔒 **Permission Checks in Views**

All views in `bookshelf/views.py` implement permission-based access control using Django decorators:

#### **View List** (`book_list`)
```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Displays all books
```

#### **Create Book** (`book_create`)
```python
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # Creates a new book
```

#### **Edit Book** (`book_edit`)
```python
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # Edits an existing book
```

#### **Delete Book** (`book_delete`)
```python
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # Deletes a book
```

### 📍 **URL Endpoints**

The bookshelf app provides the following URL patterns (prefixed with `/bookshelf/`):

| URL Pattern | View | Permission Required |
|------------|------|-------------------|
| `/bookshelf/books/` | List all books | `can_view` |
| `/bookshelf/books/<id>/` | Book details | `can_view` |
| `/bookshelf/books/create/` | Create book | `can_create` |
| `/bookshelf/books/<id>/edit/` | Edit book | `can_edit` |
| `/bookshelf/books/<id>/delete/` | Delete book | `can_delete` |
| `/bookshelf/permissions/` | View user permissions | None (login required) |

### 👤 **Assigning Users to Groups**

#### **Via Django Admin:**
1. Navigate to `/admin/auth/group/`
2. Select a group (Viewers, Editors, or Admins)
3. Add users to the "Users" section
4. Save changes

#### **Via Python Shell:**
```python
from django.contrib.auth.models import Group, User
from bookshelf.models import CustomUser

# Get a user
user = CustomUser.objects.get(email='user@example.com')

# Get a group
viewers_group = Group.objects.get(name='Viewers')

# Add user to group
user.groups.add(viewers_group)
```

#### **Via Management Command (Programmatic):**
You can extend the `setup_groups` command or create a custom command to assign users to groups automatically.

### ✅ **Testing Permissions**

#### **Check User Permissions in Views:**
```python
# In a view or template
if request.user.has_perm('bookshelf.can_create'):
    # Show create button
    pass

if request.user.has_perm('bookshelf.can_delete'):
    # Show delete button
    pass
```

#### **Check User Groups:**
```python
# Check if user is in a specific group
if request.user.groups.filter(name='Admins').exists():
    # User is an admin
    pass
```

### 📝 **Best Practices**

1. **Always use decorators:** Use `@permission_required` decorator for permission checks in views
2. **Check in templates:** Use `{% if perms.bookshelf.can_create %}` in templates to conditionally show UI elements
3. **Group-based permissions:** Assign permissions to groups rather than individual users for easier management
4. **Superuser access:** Superusers automatically have all permissions
5. **Error handling:** Use `raise_exception=True` in `@permission_required` to return 403 Forbidden instead of redirecting

### 🔍 **Verifying Setup**

1. **Check permissions exist:**
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import Permission
   >>> Permission.objects.filter(codename__startswith='can_')
   ```

2. **Check groups exist:**
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import Group
   >>> Group.objects.all()
   ```

3. **Test access:** Log in as different users with different group memberships and verify access restrictions work correctly.

### 📚 **Additional Resources**

- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions)
- [Django Groups Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)
- [Custom Permissions](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions)

