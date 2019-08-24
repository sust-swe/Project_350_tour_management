from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from homepage.models import City, UserDetail, Contact

# Create your models here.


########################################################################################################################
class ResidenceOwner(models.Model):
    user_detail = models.OneToOneField(UserDetail, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.user_detail.__str__()


########################################################################################################################
class Residence(Contact):
    residence_owner = models.ForeignKey(ResidenceOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)
    img = models.ImageField(upload_to='ResidencePhoto', null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'city'], name='unique residence in city')
        ]

    def __str__(self):
        return '%s\'s %s at %s' % (self.residence_owner.__str__(), self.name, self.city.__str__())


########################################################################################################################
class Space(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    space_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True, default=None)
    rent = models.FloatField(default=0)
    person = models.PositiveIntegerField(default=1)
    shared = models.BooleanField(default=False)
    img = models.ImageField(upload_to='ResidenceSpacePhoto', null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['residence', 'space_name'], name='residence\'s unique place'),
            models.CheckConstraint(check=Q(rent__gte=0), name='non-negative rent')
        ]

    def __str__(self):
        return '%s Space-> %s' % (self.residence.__str__(), self.space_name)


########################################################################################################################
class SpaceAvailable(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    avail_from = models.DateField()
    avail_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['space', 'avail_from'], name='Space avail unique from'),
            models.UniqueConstraint(fields=['space', 'avail_to'], name='Space avail unique to')
        ]

    def __str__(self):
        return '%s from %s to %s' % (self.space.__str__(), str(self.avail_from), str(self.avail_to))


########################################################################################################################
class SpaceBooking(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    book_from = models.DateField()
    book_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['space', 'book_from'], name='SpaceBooking unq from'),
            models.UniqueConstraint(fields=['space', 'book_to'], name='SpaceBooking unq to')
        ]

    def __str__(self):
        return '%s by %s from %s to %s' % (self.space.__str__(), self.guest.__str__(), str(self.book_from),
                                           str(self.book_to))


########################################################################################################################
# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
