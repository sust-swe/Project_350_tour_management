from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F
from homepage.models import City, UserDetail, Address, Country
from homepage.base import *

# Create your models here.


class Gender(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    

class Guide(models.Model):
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, default=None)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="guide", null=True, default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="guide", null=True, default=None)
    mobile = models.IntegerField()
    img = models.ImageField(upload_to='GuidePhoto', default=None, null=True, blank=True)
    description = models.CharField(max_length=255, default=None, null=True, blank=True)
    rent = models.FloatField(null=True)
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not (exclude and "user_detail" in exclude):
            if Guide.objects.filter(user_detail=self.user_detail, name=self.name).exists():
                if Guide.objects.get(user_detail=self.user_detail, name=self.name).id != self.id:
                    raise ValidationError("You have already a guide of the same name")
        if Guide.objects.filter(mobile=self.mobile).exists():
            if Guide.objects.get(mobile=self.mobile).id != self.id:
                raise ValidationError("This mobile number is already used")
            
    def __str__(self):
        return self.name


class GuideAvailable(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    def __str__(self):
        return '%s %s %s' % (self.guide.__str__(), str(self.avail_from), str(self.avail_to))


class GuideBooking(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()
    total_rent = models.FloatField()
    booking_time = models.DateTimeField(null=True)

    def __str__(self):
        return '%s hired by %s from %s to %s' % (self.guide.__str__(), self.customer.__str__(), str(self.book_from),
                                                 str(self.book_to))


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
