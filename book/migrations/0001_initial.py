# Generated by Django 3.1.1 on 2020-09-09 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('is_vip', models.BooleanField(default=False)),
                ('room_number', models.PositiveSmallIntegerField(unique=True)),
                ('bed_count', models.PositiveSmallIntegerField(default=1)),
                ('size', models.PositiveSmallIntegerField(default=20)),
                ('has_good_view', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='book.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book_room', to='book.room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookedRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book_room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booked_room', to='book.bookroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booked_room', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
