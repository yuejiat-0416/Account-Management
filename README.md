# Account-Management

Implementation of an Account Management System using Django.



# Step 0:
Install required packages such as celery, django-allauth, django-invitations, redis, etc...



# Step 1: 
docker compose build



# Step 2: 
docker compose up



# Step 3:
Then open another terminal and run the following command to create a superuser:

docker exec -it container_id python manage.py createsuperuser



# Step 4:
Open a browser and go to localhost:8000/admin
log-in with the superuser account your just created.



# Step 5:
Go to the "Role" table, and create the seven roles manually: admin, hiring_manager, ...



# Step 6:
You should be all set now. Log out from your superuser account.
Then go to localhost:8000/dashboard, and follow the user flow for a new user.



# Add-on:
You need to set up a smtp server on your own in settings.py