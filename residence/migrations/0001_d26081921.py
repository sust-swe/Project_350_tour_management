# Generated by Django 2.2.4 on 2019-08-26 13:41

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0001_d26081905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.IntegerField(blank=True, default=None, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='ResidencePhoto')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.City')),
                ('user_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space_type_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('rent', models.FloatField()),
                ('person', models.PositiveIntegerField()),
                ('shared', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='ResidenceSpacePhoto')),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Residence')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_space', models.IntegerField(default=1)),
                ('booking_time', models.DateTimeField()),
                ('total_rent', models.FloatField()),
                ('book_from', models.DateField()),
                ('book_to', models.DateField()),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserDetail')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Space')),
            ],
            options={
                'ordering': ['-booking_time'],
            },
        ),
        migrations.CreateModel(
            name='SpaceAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_space', models.IntegerField(default=1)),
                ('avail_from', models.DateField()),
                ('avail_to', models.DateField()),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residence.Space')),
            ],
            options={
                'ordering': ['avail_from', '-avail_to'],
            },
        ),
        migrations.AddConstraint(
            model_name='spacebooking',
            constraint=models.UniqueConstraint(fields=('space', 'book_from'), name='SpaceBooking unq from'),
        ),
        migrations.AddConstraint(
            model_name='spacebooking',
            constraint=models.UniqueConstraint(fields=('space', 'book_to'), name='SpaceBooking unq to'),
        ),
        migrations.AddConstraint(
            model_name='spacebooking',
            constraint=models.CheckConstraint(check=models.Q(book_from__lte=django.db.models.expressions.F('book_to')), name='sb unique time span'),
        ),
        migrations.AddConstraint(
            model_name='spacebooking',
            constraint=models.CheckConstraint(check=models.Q(total_rent__gte=0), name='sb non-negative total rent'),
        ),
        migrations.AddConstraint(
            model_name='spaceavailable',
            constraint=models.UniqueConstraint(fields=('space', 'avail_from'), name='Space avail unique from'),
        ),
        migrations.AddConstraint(
            model_name='spaceavailable',
            constraint=models.UniqueConstraint(fields=('space', 'avail_to'), name='Space avail unique to'),
        ),
        migrations.AddConstraint(
            model_name='spaceavailable',
            constraint=models.CheckConstraint(check=models.Q(avail_from__lte=django.db.models.expressions.F('avail_to')), name='sa valid date span '),
        ),
        migrations.AddConstraint(
            model_name='space',
            constraint=models.UniqueConstraint(fields=('residence', 'space_type_name'), name="residence's unique space"),
        ),
        migrations.AddConstraint(
            model_name='space',
            constraint=models.CheckConstraint(check=models.Q(rent__gte=0), name='non-negative rent'),
        ),
        migrations.AddConstraint(
            model_name='residence',
            constraint=models.UniqueConstraint(fields=('user_detail', 'name', 'city'), name="user's unique residence in city"),
        ),
    ]
