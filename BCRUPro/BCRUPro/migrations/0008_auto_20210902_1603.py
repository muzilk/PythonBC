# Generated by Django 3.0 on 2021-09-02 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BCRUPro', '0007_auto_20210902_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BCRUPro.Vendor'),
        ),
    ]
