# Generated by Django 3.1.2 on 2020-10-28 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacaptureapp', '0004_project_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='users',
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='account.account'),
            preserve_default=False,
        ),
    ]
