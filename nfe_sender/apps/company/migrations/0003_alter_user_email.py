# Generated by Django 3.2.5 on 2021-07-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, unique=True, verbose_name='email address'),
        ),
    ]