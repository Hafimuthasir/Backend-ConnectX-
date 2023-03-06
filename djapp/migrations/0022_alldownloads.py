# Generated by Django 4.0.6 on 2023-01-02 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0021_posts_downloadscount'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllDownloads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djapp.posts')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
