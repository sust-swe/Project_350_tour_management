from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from homepage.models import City, UserDetail, Address, MyChoice

# Create your models here.


class Restaurant(Address):
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    mobile = models.IntegerField(default=None, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to='RestaurantPhoto', null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_detail', 'name', 'city'], name='user\'s unique restaurant in city')
        ]

    def __str__(self):
        return '%s\'s %s in %s' % (self.user_detail, self.name, self.city.__str__())


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='FoodPhoto', null=True, blank=True, default=None)
    price = models.FloatField()
    person = models.PositiveIntegerField(default=1, blank=True)
    available_at_time = models.CharField(max_length=1, choices=MyChoice.Eating_time)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'name'], name='unique food in restaurant'),
            models.CheckConstraint(check=Q(price__gte=0), name='non-negative food price')
        ]

    def __str__(self):
        return '%s serves %s' % (self.restaurant.__str__(), self.name)


class Orders(models.Model):
    customer = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    order_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'order_time'], name='order primary constraint')
        ]
        ordering = ['-order_time']

    def __str__(self):
        return '%s at %s' % (self.customer.__str__(), str(self.order_time))


class OrderDetail(models.Model):
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['orders', 'food'], name='order has unique food')
        ]

    def __str__(self):
        return '%s contains %s' % (self.orders, self.food)


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
