from homepage.base import *
from django.utils.translation import gettext_lazy as _
from .views_1 import is_space_booked, make_space_unavailable, create_avail_space, is_space_available
from homepage.models import UserDetail, City, Country, Address, MyChoice, Cart


#####################################         Models           ########################################################

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


class SpaceType(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    person = models.PositiveIntegerField()
    rent = models.FloatField()
    pic = models.ImageField(upload_to="SpaceTypePhoto",
                            null=True, blank=True, default=None)
    description = models.CharField(
        max_length=255, null=True, blank=True, default=None)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if exclude and 'residence' in exclude:
            pass
        else:
            if SpaceType.objects.filter(residence=self.residence, name=self.name):
                raise ValidationError(
                    "This Residence has alreday a same named space type")

    def __str__(self):
        return self.name


class Space(models.Model):
    name = models.CharField(max_length=255)
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    space_type = models.ForeignKey(
        SpaceType, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return '%s Space-> %s' % (self.residence.__str__(), self.space_type)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if exclude and 'residence' in exclude:
            pass
        else:
            if Space.objects.filter(residence=self.residence, name=self.name).exists():
                raise ValidationError(
                    "This Residence has already a same named space")


class SpaceAvailable(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        ordering = ['avail_from', '-avail_to']

    def __str__(self):
        return '%s from %s to %s' % (self.space.__str__(), str(self.avail_from), str(self.avail_to))

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)


class SpaceBooking(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
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

    def clean(self):
        if not is_space_available(SpaceAvailable, self.space, self.book_from, self.book_to):
            raise ValidationError(_("Not Available"))


def is_space_booked_tricky(space, from_date, to_date):
    return is_space_booked(SpaceBooking, space, from_date, to_date)


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
