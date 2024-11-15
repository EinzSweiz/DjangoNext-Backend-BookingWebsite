# #!/bin/sh
# echo "Starting entrypoint script..."

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for PostgreSQL..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# echo "Running migrations..."
# python manage.py migrate

# echo "Starting server..."
# python manage.py runserver 0.0.0.0:8000
