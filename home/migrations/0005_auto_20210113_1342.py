# Generated by Django 3.1.5 on 2021-01-13 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.FileField(default='', null=True, upload_to=''),
        ),
    ]