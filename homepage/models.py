from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class City(models.Model):
    countries = [
        ('BGD', 'Bangladesh'), ('IND', 'India'), ('PAK', 'Pakistan'),
        ('NEP', 'Nepal'), ('BHU', 'Bhutan'), ('MYA', 'Myanmar')
    ]

    country = models.CharField(max_length=3, choices=countries)
    state = models.CharField(max_length=255, blank=True, default=None, null=True)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    img = models.ImageField(upload_to='CityPhoto', null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['country', 'state', 'district', 'city'], name='unique city')
        ]

    def __str__(self):
        return '%s %s %s %s' % (self.country, self.state, self.district, self.city)


class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, default=None, blank=True)
    address = models.CharField(max_length=255, null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s %s' % (self.city.__str__(), self.address.__str__())


class UserDetail(Address):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(max_length=15, default=None, null=True, blank=True)
    img = models.ImageField(upload_to='UserDetailPhoto', null=True, blank=True, default=None)
    description = models.TextField(max_length=255, default=None, null=True, blank=True)
    restaurant_description = models.CharField(max_length=255, default=None, null=True, blank=True)
    residence_description = models.CharField(max_length=255, default=None, null=True, blank=True)
    guide_description = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return '%s' % self.user.username


class MyChoice:
    MyDays = [
        ('mo', 'Monday'), ('tu', 'Tuesday'), ('we', 'Wednesday'), ('th', 'Thursday'),
        ('fr', 'Friday'), ('sa', 'Saturday'), ('su', 'Sunday')
    ]

    MyDayTime = [
        ('mo', 'Morning'), ('no', 'Noon'), ('af', 'Afternoon'), ('ev', 'Evening'), ('ni', 'Night')
    ]

    Eating_time = [
        ('b', 'Breakfast'), ('l', 'Lunch'), ('d', 'Dinner'), ('a', 'all time')
    ]


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
