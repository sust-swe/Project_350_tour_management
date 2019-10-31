# Generated by Django 2.2.6 on 2019-10-24 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0006_d18101902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.IntegerField(blank=True, default=None, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='ResidencePhoto')),
                ('city', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.City')),
                ('country', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Country')),
                ('user_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail')),
            ],
        ),
        migrations.CreateModel(
            name='ResidenceOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_space', models.IntegerField()),
                ('book_from', models.DateField()),
                ('book_to', models.DateField()),
                ('booking_time', models.DateTimeField()),
                ('bill', models.FloatField()),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Residence')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('person', models.PositiveIntegerField()),
                ('rent', models.FloatField()),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='SpaceTypePhoto')),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Residence')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_from', models.DateField()),
                ('book_to', models.DateField()),
                ('residence_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='space_booking', to='residence.ResidenceOrder')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space_booking', to='residence.Space')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avail_from', models.DateField()),
                ('avail_to', models.DateField()),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Space')),
            ],
            options={
                'ordering': ['space', 'avail_from'],
            },
        ),
        migrations.AddField(
            model_name='space',
            name='space_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='residence.SpaceType'),
        ),
        migrations.AddField(
            model_name='residenceorder',
            name='space_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.SpaceType'),
        ),
    ]