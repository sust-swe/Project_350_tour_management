# Generated by Django 2.2.6 on 2019-11-18 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('guide', '0001_initial'),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidebooking',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail'),
        ),
        migrations.AddField(
            model_name='guidebooking',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guide.Guide'),
        ),
        migrations.AddField(
            model_name='guideavailable',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guide.Guide'),
        ),
        migrations.AddField(
            model_name='guide',
            name='city',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guide', to='homepage.City'),
        ),
        migrations.AddField(
            model_name='guide',
            name='country',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guide', to='homepage.Country'),
        ),
        migrations.AddField(
            model_name='guide',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='guide.Gender'),
        ),
        migrations.AddField(
            model_name='guide',
            name='user_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail'),
        ),
    ]
