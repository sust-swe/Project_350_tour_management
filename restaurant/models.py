from django.db import models
from django.contrib.auth.models import User
from homepage.models import City

# Create your models here.


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    restaurant_name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return '%s at %s in ' % (self.restaurant_name, self.address) + self.city.__str__()


class Food(models.Model):
    available_times = [
        ('b', 'Breakfast'), ('l', 'Lunch'), ('d', 'Dinner')
    ]
    food_name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='FoodPhoto', null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.FloatField()
    person = models.IntegerField(default=1)
    available_at_time = models.CharField(max_length=1, choices=available_times)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'food_name'], name='unique food in restaurant')
        ]

    def __str__(self):
        return '%s in -> ' % self.food_name + self.restaurant.__str__()


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    order_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'customer', 'order_time'], name='primary constraint')
        ]

    def __str__(self):
        return self.restaurant.__str__() + ' serves %s at time %s' % (self.customer.username, str(self.order_time))


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'food'], name='primary constraint')
        ]

    def __str__(self):
        return self.order.__str__() + ' item %s ' % self.food.food_name


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
