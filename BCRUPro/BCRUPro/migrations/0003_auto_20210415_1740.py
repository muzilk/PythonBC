# Generated by Django 3.0.7 on 2021-04-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BCRUPro', '0002_auto_20210401_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]