from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F
from homepage.models import City, UserDetail, Address, Country

# Create your models here.


class Residence(models.Model):
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, default=None)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, default=None)
    mobile = models.IntegerField(default=None, null=True, blank=True)
    description = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    img = models.ImageField(upload_to='ResidencePhoto',
                            null=True, blank=True, default=None)

    class Meta:
        pass

    def __str__(self):
        return '%s\'s %s at %s' % (self.user_detail.__str__(), self.name, self.city.__str__())


class Space(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    space_type_name = models.CharField(max_length=100)
    description = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    rent = models.FloatField()
    person = models.PositiveIntegerField()
    shared = models.BooleanField(default=False, choices=[
                                 (False, 'No'), (True, 'Yes')])
    img = models.ImageField(upload_to='ResidenceSpacePhoto',
                            null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['residence', 'space_type_name'], name='residence\'s unique space'),
            models.CheckConstraint(check=Q(rent__gte=0),
                                   name='non-negative rent')
        ]

    def __str__(self):
        return '%s Space-> %s' % (self.residence.__str__(), self.space_type_name)


class SpaceAvailable(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    number_of_space = models.IntegerField(default=1)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['space', 'avail_from'], name='Space avail unique from'),
            models.UniqueConstraint(
                fields=['space', 'avail_to'], name='Space avail unique to'),
            models.CheckConstraint(check=Q(avail_from__lte=F(
                'avail_to')), name='sa valid date span ')
        ]
        ordering = ['avail_from', '-avail_to']

    def __str__(self):
        return '%s from %s to %s' % (self.space.__str__(), str(self.avail_from), str(self.avail_to))


class SpaceBooking(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    number_of_space = models.IntegerField(default=1)
    guest = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    total_rent = models.FloatField()
    book_from = models.DateField()
    book_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['space', 'book_from'], name='SpaceBooking unq from'),
            models.UniqueConstraint(
                fields=['space', 'book_to'], name='SpaceBooking unq to'),
            models.CheckConstraint(check=Q(book_from__lte=F(
                'book_to')), name='sb unique time span'),
            models.CheckConstraint(
                check=Q(total_rent__gte=0), name='sb non-negative total rent')
        ]
        ordering = ['-booking_time']

    def __str__(self):
        return '%s by %s from %s to %s' % (self.space.__str__(), self.guest.__str__(), str(self.book_from),
                                           str(self.book_to))


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
