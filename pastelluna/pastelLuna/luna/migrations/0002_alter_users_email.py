# Generated by Django 4.1.2 on 2022-11-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
