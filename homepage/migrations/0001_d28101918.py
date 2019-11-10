# Generated by Django 2.2.6 on 2019-10-28 12:40

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
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('Space', 'Space'), ('Food', 'Food'), ('Guide', 'Guide')], max_length=20)),
                ('item_id', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('from_date', models.DateField(blank=True, default=None, null=True)),
                ('to_date', models.DateField(blank=True, default=None, null=True)),
                ('price', models.FloatField()),
            ],
            options={
                'ordering': ['owner'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='CityPhoto')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='UserDetailPhoto')),
                ('description', models.TextField(blank=True, default=None, max_length=255, null=True)),
                ('restaurant_description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('residence_description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('guide_description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('city', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.City')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='country',
            constraint=models.UniqueConstraint(fields=('name',), name='Unique Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Country'),
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail'),
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('country', 'city'), name='unique city'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.CheckConstraint(check=models.Q(price__gte=0), name='non-negative cart_item price'),
        ),
    ]