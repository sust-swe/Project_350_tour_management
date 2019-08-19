from django.db import models

# Create your models here.


class First(models.Model):
    name = models.CharField(max_length=10)
    img = models.ImageField(upload_to='pics')


#  pip install Pillow
#  python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
