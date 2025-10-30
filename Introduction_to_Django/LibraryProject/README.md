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

