# Purchase Order Project

## Overview

This Django project provides a CRUD API for managing purchase orders, suppliers, and line items. The API is built using Django, Django Rest Framework (DRF), and PostgreSQL.


## Database Models

### Supplier

- **Fields:**
  - `name`: String
  - `email`: Email field

### LineItem

- **Fields:**
  - `item_name`: String
  - `quantity`: Positive integer
  - `price_without_tax`: Decimal field
  - `tax_name`: String
  - `tax_amount`: Decimal field
  - `line_total`: Calculated field (quantity * price_without_tax).

### PurchaseOrder

- **Fields:**
  - `supplier`: Foreign key to Supplier.
  - `order_time`: Date and time
  - `order_number`: Positive integer
  - `total_quantity`: Calculated field (sum of quantities of line items).
  - `total_amount`: Calculated field (sum of line_total of line items).
  - `total_tax`: Calculated field (sum of tax_amount of line items).





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
		
    You can create a free tier postgresql instance from https://neon.tech/ 
    OR 
    use a local postgresql installation

2. **Update the database settings in `purchase_order_project/settings.py`:**

    -   For local PostgreSQL installation
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
    -   For neon.tech PostgreSQL instance
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'your_database_name',
                'USER': 'your_database_user',
                'PASSWORD': 'your_database_password',
                'HOST': '******.aws.neon.tech',
                'PORT': '5432',
                'OPTIONS': {'sslmode': 'require'},
            }
        }
        ```

### Migrations

Apply the initial database migrations:

```bash
python manage.py makemigrations
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


### Testing API Endpoints

    Import the PurchaseOrderProject.postman_collection.json in Postman