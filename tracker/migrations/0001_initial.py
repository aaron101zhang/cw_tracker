# Generated by Django 3.1.8 on 2021-04-11 01:25

from django.db import migrations, models
import django.db.models.deletion
import tracker.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedUser',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlayDate',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cells', models.PositiveIntegerField()),
                ('alias', models.ForeignKey(default=tracker.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to='tracker.authorizeduser')),
                ('date', models.ForeignKey(default=tracker.models.get_default_date, on_delete=django.db.models.deletion.CASCADE, to='tracker.playdate')),
            ],
        ),
        migrations.CreateModel(
            name='DailyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=50)),
                ('duration', models.DurationField()),
                ('date', models.ForeignKey(default=tracker.models.get_default_date, on_delete=django.db.models.deletion.CASCADE, to='tracker.playdate')),
            ],
        ),
    ]