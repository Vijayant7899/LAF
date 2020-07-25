# Generated by Django 2.0.6 on 2020-07-24 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Userregister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=20)),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=20)),
                ('iteam', models.CharField(max_length=20)),
                ('landmark', models.CharField(max_length=20)),
                ('datetime', models.DateTimeField()),
                ('content', models.TextField()),
                ('iteam_pic', models.ImageField(upload_to='')),
                ('postuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
