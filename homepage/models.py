from django.db import models
# from django.contrib.auth.models import User

# Create your models here.


class Place(models.Model):
    countries = [
        ('BGD', 'Bangladesh'), ('IND', 'India'), ('PAK', 'Pakistan'),
        ('NEP', 'Nepal'), ('BHU', 'Bhutan'), ('MYA', 'Myanmar')
    ]
    country = models.CharField(max_length=3, choices=countries)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # name = models.CharField(max_length=10)
    # img = models.ImageField(upload_to='pics')




'''
class BookManager(models.Manager):
    def create_book(self, title):
        book = self.create(title=title)
        # do something with the book
        return book

class Book(models.Model):
    title = models.CharField(max_length=100)

    objects = BookManager()

book = Book.objects.create_book("Pride and Prejudice")
'''


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h

