# Starting the APP

To run the Django project after cloning it, follow these steps:

## Requirements

1. Install [Python](https://www.python.org/downloads/)
2. Create a Virtual Enviroment (Optional):

Navigate to the project directory and create a virtual environment to isolate the project's dependencies. Run the following command:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On Windows: `.venv\Scripts\activate`
- On macOS and Linux: `source .venv/bin/activate`

install django

```bash
python pip install django
```

3. Install Dependencies:

With the virtual environment activated, install the project dependencies listed in the requirements.txt file. Run the following command:

```bash
pip install -r requirements.txt
```

4. Set Up Database:

To set up the database (SQLite) run the following commands:

```bash
python manage.py makemigrations movie_api

python manage.py migrate
```

5. Run the Development Server:

```bash
python manage.py runserver
```

6. Access the Project:

Open your web browser and go to the address provided by the development server (usually http://127.0.0.1:8000/ or http://localhost:8000/). You should see the running Django project.
