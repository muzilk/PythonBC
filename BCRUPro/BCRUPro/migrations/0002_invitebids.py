# Generated by Django 3.0 on 2020-11-03 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BCRUPro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteBids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_id', models.TextField(unique=True)),
                ('network_type', models.TextField()),
                ('area', models.TextField()),
                ('time', models.TextField()),
                ('number', models.TextField()),
                ('data', models.TextField()),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BCRUPro.Node')),
            ],
        ),
    ]
