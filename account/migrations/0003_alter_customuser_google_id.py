# Generated by Django 4.2.16 on 2024-09-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='google_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
