# Generated by Django 2.2.4 on 2019-08-26 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0001_d27081901'),
        ('blog', '0001_d27081901'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='article',
            name='city',
            field=models.ManyToManyField(to='homepage.City'),
        ),
        migrations.AddField(
            model_name='article',
            name='topic',
            field=models.ManyToManyField(to='blog.Topic'),
        ),
        migrations.AddField(
            model_name='article',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail'),
        ),
        migrations.AddConstraint(
            model_name='blog',
            constraint=models.UniqueConstraint(fields=('owner', 'name'), name='unique blog of the owner'),
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('blog', 'name'), name='unique article in blog'),
        ),
    ]