# Generated by Django 3.2.5 on 2021-07-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters', max_length=15, unique=True, verbose_name='username'),
        ),
    ]
