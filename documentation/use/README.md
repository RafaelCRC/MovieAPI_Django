# Read the Postman Documentation to understand all endpoints and features

the file.json is available at repository root

## prerequisites

To create admin users is important to understand that the only way to create the first user with admin role is through Django admin page

To do that you need to create a superuser in terminal with command:

```bash
python manage.py createsuperuser
```

Insert a user and password.

Do the login in http://127.0.0.1:8000/admin/ and go to http://127.0.0.1:8000/admin/movie_api/user/

Select a user and change the role to administrator (you need to create a new regular user)
