# Generated by Django 3.0.4 on 2020-03-27 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Mevcut mu?'),
            preserve_default=False,
        ),
    ]