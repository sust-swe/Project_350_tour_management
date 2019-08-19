from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Space(models.Model):
    # name = models.CharField(max_length=10)
    img = models.ImageField(upload_to='residence_photos', null=True)
    space_name = models.CharField(max_length=100)
    rent = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    person = models.ImageField(default=1)
    shared = models.BooleanField(default=False)


class AvailableSpace(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['space', 'avail_from'], name='unique from'),
            models.UniqueConstraint(fields=['space', 'avail_to'], name='unique_to')
        ]


class SpaceBookings(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
