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

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if not (exclude and "user_detail" in exclude):
            if Residence.objects.filter(user_detail=self.user_detail, name=self.name).exists():
                if Residence.objects.get(user_detail=self.user_detail, name=self.name).id != self.id:
                    raise ValidationError(
                        "You have already a residence of that name -_-")

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
            if SpaceType.objects.filter(residence=self.residence, name=self.name).exists():
                if SpaceType.objects.get(residence=self.residence, name=self.name).id != self.id:
                    raise ValidationError(
                        "This Residence has alreday a TYPE of the same name -_-")

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
                # print(self.id)
                if Space.objects.get(residence=self.residence, name=self.name).id != self.id:
                    raise ValidationError(
                        "This Residence has already a space of this name")


class SpaceAvailable(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        ordering = ["space", "avail_from"]

    def __str__(self):
        return '%s from %s to %s' % (self.space.__str__(), str(self.avail_from), str(self.avail_to))

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)


class ResidenceOrder(models.Model):
    guest = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    space_type = models.ForeignKey(SpaceType, on_delete=models.CASCADE)
    n_space = models.IntegerField()
    book_from = models.DateField()
    book_to = models.DateField()
    booking_time = models.DateTimeField()
    bill = models.FloatField()


class SpaceBooking(models.Model):
    # while saving object of this model firstly the space is made unavailable
    residence_order = models.ForeignKey(
        ResidenceOrder, on_delete=models.CASCADE, related_name="space_booking", null=True)
    space = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="space_booking")
    book_from = models.DateField()
    book_to = models.DateField()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)


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
