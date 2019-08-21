from django.db import models
from django.contrib.auth.models import User
from homepage.models import City

# Create your models here.


class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    # name = models.CharField(max_length=10)
    # img = models.ImageField(upload_to='pics')


class AvailableGuide(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rent_per_day = models.FloatField()


class GuideBookings(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()
    total_rent = models.FloatField()


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

