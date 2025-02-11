in terminal do cd internshala_clone 
then do python manage.py runserver  ( to close server click ctrl+c)
then go to the login button 
and then for tanmay and siddhant select employer
and for viraj and arshvir select candidate             ( dont forget to logout else thoda issues hoga )

also go in the settings.py and search for DATABASES
there give your own database details like password and name
then in terminal do python manage.py makemigrations and then python manage.py migrate
