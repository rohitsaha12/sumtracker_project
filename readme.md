# Purchase Order Project

## Overview

This Django project provides a CRUD API for managing purchase orders, suppliers, and line items. The API is built using Django, Django Rest Framework (DRF), and PostgreSQL.

## Setup Instructions

### Prerequisites

- Python 3.x
- Pip (Python package installer)
- PostgreSQL

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/purchase_order_project.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd purchase_order_project
    ```

3. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Database Configuration

1. **Create a PostgreSQL database for the project.**
		You can create a free tier postgresql instance from https://neon.tech/  or a local postgresql installation will also work 

2. **Update the database settings in `purchase_order_project/settings.py`:**

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

### Migrations

Apply the initial database migrations:

```bash
python manage.py migrate
```

### Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

### Accessing Swagger and ReDoc Documentation

-   **Swagger:** Open `http://127.0.0.1:8000/swagger/` in your web browser.
    
-   **ReDoc:** Open `http://127.0.0.1:8000/redoc/` in your web browser.
    

### Running Tests

To run the unit tests:

```bash
python manage.py test 
```

### Auto-generating OpenAPI Spec

To auto-generate the OpenAPI spec using Django Spectacular:

```bash
python manage.py spectacular --file schema.yml
```

This will create a file named `schema.yml` containing the OpenAPI spec.

## API Endpoints

### Purchase Orders

-   List and Create: `GET` and `POST` requests to `/api/purchase/orders/`
-   Retrieve, Update, and Delete: `GET`, `PUT`, and `DELETE` requests to `/api/purchase/orders/<int:id>/`