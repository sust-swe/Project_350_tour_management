from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name="Unique Country")
        ]

    def __str__(self):
        return self.name


class City(models.Model):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    img = models.ImageField(upload_to='CityPhoto',
                            null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'city'], name='unique city')
        ]

    def __str__(self):
        return self.city


class Address(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, default=None, blank=True)
    address = models.CharField(
        max_length=255, null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s %s' % (self.city.__str__(), self.address.__str__())


class UserDetail(Address):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(
        max_length=15, default=None, null=True, blank=True)
    img = models.ImageField(upload_to='UserDetailPhoto',
                            null=True, blank=True, default=None)
    description = models.TextField(
        max_length=255, default=None, null=True, blank=True)
    restaurant_description = models.CharField(
        max_length=255, default=None, null=True, blank=True)
    residence_description = models.CharField(
        max_length=255, default=None, null=True, blank=True)
    guide_description = models.CharField(
        max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return '%s' % self.user.username


class MyChoice:
    MyDays = [
        ('mo', 'Monday'), ('tu', 'Tuesday'), ('we', 'Wednesday'), ('th', 'Thursday'),
        ('fr', 'Friday'), ('sa', 'Saturday'), ('su', 'Sunday')
    ]

    MyDayTime = [
        ('mo', 'Morning'), ('no', 'Noon'), ('af',
                                            'Afternoon'), ('ev', 'Evening'), ('ni', 'Night')
    ]

    Eating_time = [
        ('Breakfast', 'Breakfast'), ('Lunch',
                                     'Lunch'), ('Dinner', 'Dinner'), ('All Time', 'All Time')
    ]

    months = [
        (1, 'January'), (2, 'February'), (3,
                                          'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10,
                                                       'Octobor'), (11, 'November'), (12, 'December')
    ]


class Cart(models.Model):
    item_types = [('Space', 'Space'), ('Food', 'Food'), ('Guide', 'Guide')]
    owner = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=item_types)
    item_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(blank=True, null=True, default=None)
    from_date = models.DateField(blank=True, null=True, default=None)
    to_date = models.DateField(blank=True, null=True, default=None)
    price = models.FloatField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(price__gte=0),
                                   name='non-negative cart_item price'),
        ]
        ordering = ['owner']

    def __str__(self):
        return self.item_type


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
