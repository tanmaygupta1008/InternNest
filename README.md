in terminal do cd internshala_clone 
then do python manage.py runserver  ( to close server click ctrl+c)
then go to the login button 
and then for tanmay and siddhant select employer
and for viraj and arshvir select candidate             ( dont forget to logout else thoda issues hoga )

also go in the settings.py and search for DATABASES
there give your own database details like password and name
then go in mysql and create a database internshala;
then in terminal do python manage.py makemigrations and then python manage.py migrate

(****** agar migrate karke bhi data nhi jaa rha hai like tumahara user ka dat while doing login **** to hi karna ye )
also adding a dump file Dump20250214.zip file , uske andar ek file hoga usko extract karlo 
aur phir sql workbench mai jaake create  database intershala likho
aur phir upar menu maina server likha hoga waha pe data import ka option ko click karo
aur phir yeh dump file ki location do  aur niche right mai ek start import button hoga woh click karo
phir try karke dekho