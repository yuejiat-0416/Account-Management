FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app to the container
COPY . /app/

# make migration
# looks not working, have to use start.sh at docker-compos.yml
# update: start.sh not work as well, use
# docker-compose run web python manage.py makemigrations
# docker-compose run web python manage.py migrate
# after running the docker-compose up
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]