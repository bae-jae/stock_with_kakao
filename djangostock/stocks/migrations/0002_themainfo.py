# Generated by Django 3.2.16 on 2022-12-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemaInfo',
            fields=[
                ('thema_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('stocks', models.CharField(max_length=500)),
            ],
        ),
    ]