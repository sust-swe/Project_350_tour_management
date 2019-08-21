from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class City(models.Model):
    countries = [
        ('BGD', 'Bangladesh'), ('IND', 'India'), ('PAK', 'Pakistan'),
        ('NEP', 'Nepal'), ('BHU', 'Bhutan'), ('MYA', 'Myanmar')
    ]

    country = models.CharField(max_length=3, choices=countries)
    state = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    img = models.ImageField(upload_to='CityPhoto', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['country', 'state', 'district', 'city'], name='primary constraint')
        ]

    def __str__(self):
        return '%s %s %s %s' % (self.country, self.state, self.district, self.city)


class Contact(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.IntegerField(null=True)
    email = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mobile'], name='unique mobile'),
            models.UniqueConstraint(fields=['email'], name='unique email')
        ]

    def __str__(self):
        return '%s %s %s %s' % (self.city.__str__(), self.address.__str__(), str(self.mobile), self.email)

'''
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contact'], name='unique contact')
        ]

    def __str__(self):
        return 


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
