# Generated by Django 2.2.4 on 2019-08-24 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('BGD', 'Bangladesh'), ('IND', 'India'), ('PAK', 'Pakistan'), ('NEP', 'Nepal'), ('BHU', 'Bhutan'), ('MYA', 'Myanmar')], max_length=3)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('img', models.ImageField(blank=True, null=True, upload_to='CityPhoto')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('address', models.CharField(max_length=255)),
                ('mobile', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('img', models.ImageField(blank=True, null=True, upload_to='UserDetailPhoto')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.City')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('country', 'state', 'district', 'city'), name='uniqcon'),
        ),
        migrations.AddConstraint(
            model_name='userdetail',
            constraint=models.UniqueConstraint(fields=('mobile',), name='unique mobile'),
        ),
    ]