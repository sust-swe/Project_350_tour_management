from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from homepage.models import City
from homepage.models import City, UserDetail

# Create your models here.


class Guide(models.Model):
    user_detail = models.OneToOneField(UserDetail, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.user_detail.__str__()


class GuideAvailable(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()
    rent_per_day = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['guide', 'avail_from'], name='unique from'),
            models.UniqueConstraint(fields=['guide', 'avail_to'], name='unique to'),
            models.CheckConstraint(check=Q(rent_per_day__gte=0), name='positive rent')
        ]

    def __str__(self):
        return '%s %s %s' % (self.guide.__str__(), str(self.avail_from), str(self.avail_to))


class GuideBooking(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()
    total_rent = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['guide', 'book_from'], name='uc1'),
            models.UniqueConstraint(fields=['guide', 'book_to'], name='uc2'),
            models.CheckConstraint(check=Q(total_rent__gte=0), name='positive total')
        ]

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
