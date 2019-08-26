from django.db import models
from homepage.models import UserDetail, City
# Create your models here.


class Topic(models.Model):
    MyTopic = [
        ('res', 'Restaurants'), ('h&r', 'Hotels & Residences'), ('gui', 'Guides'),
        ('tra', 'Transports'), ('sit', 'Sites')
    ]
    topic = models.CharField(max_length=3, choices=MyTopic)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['topic'], name='unique topic')
        ]

    def __str__(self):
        return self.topic


class Blog(models.Model):
    owner = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, default=None, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name='unique blog of the owner')
        ]

    def __str__(self):
        return '%s %s' % (self.owner, self.name)


class Article(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    writer = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    topic = models.ManyToManyField(Topic)
    city = models.ManyToManyField(City)
    description = models.CharField(max_length=100, default=None, null=True, blank=True)
    written_time = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'name'], name='unique article in blog')
        ]

    def __str__(self):
        return '%s %s %s' % (self.blog.__str__(), self.writer.__str__(), self.name)
