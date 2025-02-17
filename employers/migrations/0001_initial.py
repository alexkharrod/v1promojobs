# Generated by Django 4.2 on 2025-02-11 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employer_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=200)),
                ('company_description', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, upload_to='employer_logos/')),
            ],
        ),
    ]
