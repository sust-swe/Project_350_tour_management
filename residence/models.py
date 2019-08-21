from django.db import models
from django.contrib.auth.models import User
from homepage.models import City

# Create your models here.


class Space(models.Model):
    # name = models.CharField(max_length=10)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    space_name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    rent = models.FloatField()
    person = models.IntegerField(default=1)
    shared = models.BooleanField(default=False)
    img = models.ImageField(upload_to='residence_photos', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'space_name'], name='pc')
        ]

    def __str__(self):
        return '%s\'s %s' % (self.owner.username, self.space_name)


class AvailableSpace(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['space', 'avail_from'], name='unique from'),
            models.UniqueConstraint(fields=['space', 'avail_to'], name='unique_to')
        ]

    def __str__(self):
        return '%s from %s to %s' % (self.space.__str__(), str(self.avail_from), str(self.avail_to))


class SpaceBookings(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['space', 'book_from'], name='pc1'),
            models.UniqueConstraint(fields=['space', 'book_to'], name='pc2')
        ]

    def __str__(self):
        return '%s by %s from %s to %s' % (self.space.__str__(), self.guest.username, str(self.book_from),
                                           str(self.book_to))


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
